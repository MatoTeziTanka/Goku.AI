```python
#!/usr/bin/env python3
"""
============================================================================
SHENRON v4.0 - Flask API Server
============================================================================
Exposes SHENRON orchestrator as HTTP API with:
- TRUE synthesis (7th AI call)
- SSH agent mode
- Command approval workflow
============================================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import threading
import uuid
import time
import json
import urllib.request
import urllib.error
import re

try:
    import psutil  # type: ignore
except ImportError:
    psutil = None  # type: ignore

try:
    import requests  # type: ignore
except ImportError:
    requests = None  # type: ignore

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Import the orchestrator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shenron_v4_orchestrator import ShenronOrchestrator, WishCancelled

app = Flask(__name__)
CORS(app)  # Enable CORS for web GUI

# Initialize SHENRON
print(" Initializing SHENRON API Server...")
shenron = ShenronOrchestrator()
print(" SHENRON is ready to grant wishes!\n")

# -------------------------------------------------------------------------
# Async job management for Cloudflare-safe long running requests
# -------------------------------------------------------------------------
jobs = {}
jobs_lock = threading.Lock()

JOB_EXPECTED_DURATIONS = {
    "lightning": 120,    # 2min
    "council": 600,      # 10min 
    "ultra": 1800        # 30min
}

# Dynamic timeout system based on query complexity
def calculate_dynamic_timeout(query, power_mode):
    base_timeout = JOB_EXPECTED_DURATIONS.get(power_mode, 600)
    query_complexity = len(query.split())  # Word count as complexity measure
    
    if power_mode == "lightning":
        return max(60, min(120, base_timeout + (query_complexity // 2)))
    elif power_mode == "council":
        return max(180, min(600, base_timeout + (query_complexity // 1)))
    elif power_mode == "ultra":
        return max(300, min(1800, base_timeout + (query_complexity * 2)))
    return base_timeout

def create_job_record(query, power_mode, agent_mode=False):
    job_id = str(uuid.uuid4())
    expected_duration = JOB_EXPECTED_DURATIONS.get(power_mode, 300)
    with jobs_lock:
        jobs[job_id] = {
            "status": "queued",
            "created_at": time.time(),
            "query_preview": query[:120],
            "power_mode": power_mode,
            "agent_mode": agent_mode,
            "progress": 0,
            "message": "Queued for processing",
            "events": [{
                "timestamp": time.time(),
                "type": "info",
                "message": "Wish queued for processing"
            }],
            "expected_duration": expected_duration,
            "pending_actions": [],
            "artifacts": []
        }
    return job_id

def update_job_record(job_id, **fields):
    with jobs_lock:
        if job_id in jobs:
            jobs[job_id].update(fields)

def get_job_record(job_id):
    # Deep copy to avoid thread-safety issues with nested mutable objects
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return None
        import copy
        return copy.deepcopy(job)

def append_job_event(job_id, message, event_type="info"):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return
        events = job.setdefault("events", [])
        events.append({
            "timestamp": time.time(),
            "type": event_type,
            "message": message
        })
        if len(events) > 100:
            del events[:-100]

def is_cancellation_requested(job_id: str) -> bool:
    with jobs_lock:
        job = jobs.get(job_id)
        return bool(job and job.get("cancel_requested"))

def finalize_cancelled_job(job_id: str, message: str = "Wish cancelled by user"):
    update_job_record(
        job_id,
        status="cancelled",
        completed_at=time.time(),
        progress=100,
        message=message,
        pending_actions=[],
        artifacts=[]
    )
    append_job_event(job_id, message, "warning")

def request_job_cancellation(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return False, "Job not found"

        status = job.get("status", "queued")
        if status in ("completed", "failed", "cancelled"):
            return False, f"Job already {status}"

        job["cancel_requested"] = True

        if status == "queued":
            job["status"] = "cancelled"
            job["completed_at"] = time.time()
            job["progress"] = 100
            job["message"] = "Cancelled before start"
            message = "Cancelled before start"
        else:
            job["message"] = "Cancellation requested... attempting to halt safely"
            message = "Cancellation requested during processing"

    append_job_event(job_id, message, "warning")
    return True, message

def fetch_lm_studio_status():
    url = "http://127.0.0.1:1234/v1/models"
    status = {
        "online": False,
        "model_count": 0,
        "models": []
    }
    try:
        if requests:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            data = response.json()
        else:
            with urllib.request.urlopen(url, timeout=2) as resp:
                payload = resp.read().decode("utf-8")
                data = json.loads(payload)
        models = data.get("data") or data.get("models") or []
        status["online"] = True
        status["model_count"] = len(models)
        status["models"] = [
            model.get("id") or model.get("name") or model for model in models
        ]
    except Exception as exc:
        status["error"] = str(exc)
    return status

def get_system_metrics():
    metrics = {
        "timestamp": time.time(),
        "api_version": "v4.0",
        "system": {
            "psutil_available": bool(psutil)
        },
        "jobs": {
            "total": 0,
            "status_counts": {},
            "running": [],
            "queued": [],
            "recent_completed": [],
            "action_required": []
        }
    }

    if psutil:
        try:
            metrics["system"]["cpu_percent"] = psutil.cpu_percent(interval=None)
            vm = psutil.virtual_memory()
            metrics["system"]["memory_percent"] = vm.percent
            metrics["system"]["memory_available_mb"] = round(vm.available / (1024 * 1024), 2)
            disk_path = "C:\\" if os.name == "nt" else "/"
            disk = psutil.disk_usage(disk_path)
            metrics["system"]["disk_percent"] = disk.percent
            metrics["system"]["disk_free_gb"] = round(disk.free / (1024**3), 2)
        except Exception as exc:
            metrics["system"]["error"] = str(exc)
    else:
        metrics["system"].update({
            "cpu_percent": None,
            "memory_percent": None,
            "memory_available_mb": None,
            "disk_percent": None,
            "disk_free_gb": None
        })

    recent_events = []
    now = time.time()
    with jobs_lock:
        metrics["jobs"]["total"] = len(jobs)
        for job_id, job in jobs.items():
            status = job.get("status", "queued")
            status_counts = metrics["jobs"]["status_counts"]
            status_counts[status] = status_counts.get(status, 0) + 1

            job_summary = {
                "job_id": job_id,
                "query_preview": job.get("query_preview", ""),
                "power_mode": job.get("power_mode"),
                "progress": job.get("progress"),
                "message": job.get("message"),
                "created_at": job.get("created_at"),
                "started_at": job.get("started_at"),
                "agent_mode": job.get("agent_mode", False)
            }

            if job.get("started_at"):
                job_summary["elapsed"] = now - job["started_at"]

            if status == "running":
                metrics["jobs"]["running"].append(job_summary)
            elif status == "queued":
                metrics["jobs"]["queued"].append(job_summary)
            elif status == "completed":
                metrics["jobs"]["recent_completed"].append(job_summary)
            elif status == "action_required":
                metrics["jobs"]["action_required"].append(job_summary)

            events = job.get("events") or []
            for event in events[-3:]:
                recent_events.append({
                    "job_id": job_id,
                    "message": event.get("message"),
                    "type": event.get("type", "info"),
                    "timestamp": event.get("timestamp"),
                    "power_mode": job.get("power_mode")
                })

    recent_events.sort(key=lambda e: e.get("timestamp") or 0, reverse=True)
    metrics["recent_events"] = recent_events[:10]
    metrics["jobs"]["timeout_settings"] = JOB_EXPECTED_DURATIONS
    metrics["jobs"]["recent_completed"] = metrics["jobs"]["recent_completed"][:5]
    metrics["lm_studio"] = fetch_lm_studio_status()

    return metrics

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "SHENRON v4.0",
        "dragon_awakened": True,
        "features": ["rag", "synthesis", "agent_mode"]
    })

def validate_query(query):
    """Basic input validation for queries (length, unsafe chars)."""
    if not isinstance(query, str):
        return False, "Query must be a string"
    query = query.strip()
    if not query:
        return False, "Query cannot be empty"
    if len(query) < 3 or len(query) > 4096:
        return False, "Query length must be between 3 and 4096 characters"
    # Add more checks if needed (e.g., disallow non-printable chars)
    return True, ""

def validate_power_mode(power_mode):
    if power_mode not in {"lightning", "council", "ultra"}:
        return False, "Invalid power_mode"
    return True, ""

def validate_host(host):
    # Basic validation: only allow hostnames/IPs, prevent command injection
    if not isinstance(host, str) or not host.strip():
        return False, "Invalid host parameter"
    if len(host) > 255 or not re.match(r"^[A-Za-z0-9._-]+$", host):
        return False, "Host contains invalid characters"
    return True, ""

def validate_command(command):
    # Basic validation: string, reasonable length, disallow obvious injections
    if not isinstance(command, str) or not command.strip():
        return False, "Command must be a non-empty string"
    if len(command) < 1 or len(command) > 2048:
        return False, "Command length must be between 1 and 2048 characters"
    # Prevent some dangerous characters (semicolon chaining, etc.)
    # This is not bulletproof, but agent mode should be protected more strictly elsewhere.
    if re.search(r"[;&|`]", command):
        return False, "Command contains potentially dangerous characters"
    return True, ""

def perform_grant_wish(query, power_mode='council', use_rag=True, job_id=None, cancel_checker=None):
    """Core wish processing logic shared by sync/async flows."""
    POWER_MODES = {
        'lightning': {'name': 'LIGHTNING', 'icon': '⚡', 'power': '1,000'},
        'council': {'name': 'COUNCIL', 'icon': '🔥', 'power': '9,000'},
        'ultra': {'name': 'ULTRA INSTINCT', 'icon': '🐉', 'power': 'OVER 9000!'}
    }

    mode_info = POWER_MODES.get(power_mode, POWER_MODES['council'])
    print(f"\n{mode_info['icon']} {mode_info['name']} MODE: {query[:50]}{'...' if len(query) > 50 else ''}")
    if job_id:
        append_job_event(job_id, f"{mode_info['icon']} {mode_info['name']} mode engaged", "info")

    if cancel_checker and cancel_checker():
        raise WishCancelled()

    if power_mode == 'lightning':
        result = execute_lightning_mode(query, cancel_checker=cancel_checker)
    elif power_mode == 'ultra':
        result = execute_ultra_instinct_mode(query, use_rag, cancel_checker=cancel_checker)
    else:
        result = shenron.grant_wish(query, use_rag=use_rag, cancel_checker=cancel_checker)

    result['power_mode'] = mode_info['name']
    result['power_level'] = mode_info['power']

    total_time = result.get('total_time')
    if total_time is not None:
        print(f"   {mode_info['icon']} Wish processed in {total_time:.1f}s")
    else:
        print(f"   {mode_info['icon']} Wish processed")

    if job_id:
        append_job_event(job_id, f"{mode_info['icon']} Mode processing complete in {total_time:.1f}s" if total_time else f"{mode_info['icon']} Mode processing complete", "info")

    return result

def process_wish_job(job_id, query, power_mode, use_rag, agent_mode):
    """Background worker for asynchronous wish processing."""
    if is_cancellation_requested(job_id):
        finalize_cancelled_job(job_id, "Cancellation acknowledged before processing")
        return

    start_time = time.time()
    update_job_record(
        job_id,
        status="running",
        started_at=start_time,
        progress=10,
        message="Consulting SHENRON council"
    )
    append_job_event(job_id, "Consulting SHENRON council", "info")

    def progress_worker():
        while True:
            with jobs_lock:
                job = jobs.get(job_id)
                if not job or job.get("status") != "running":
                    break
                elapsed = time.time() - job.get("started_at", time.time())
                expected = job.get("expected_duration", JOB_EXPECTED_DURATIONS.get(power_mode, 300))
                if expected <= 0:
                    expected = 60
                fraction = min(0.85, elapsed / expected)
                computed_progress = round(10 + fraction * 80, 1)
                if computed_progress > job.get("progress", 0):
                    job["progress"] = computed_progress
                if job.get("message") == "Consulting SHENRON council":
                    job["message"] = f"Consulting SHENRON council ({int(job['progress'])}%)"
            time.sleep(5)

    threading.Thread(target=progress_worker, daemon=True).start()

    try:
        if is_cancellation_requested(job_id):
            finalize_cancelled_job(job_id, "Cancellation acknowledged before processing")
            return

        cancel_checker = lambda: is_cancellation_requested(job_id)
        result = perform_grant_wish(query, power_mode=power_mode, use_rag=use_rag, job_id=job_id, cancel_checker=cancel_checker)

        if is_cancellation_requested(job_id):
            finalize_cancelled_job(job_id, "Wish cancelled after processing step")
            return

        artifacts = result.get("artifacts") or []
        pending_actions = result.get("pending_actions") or []

        if pending_actions and not artifacts:
            update_job_record(
                job_id,
                status="action_required",
                completed_at=time.time(),
                progress=95,
                result=result,
                message="Pending MCP actions required",
                pending_actions=pending_actions,
                artifacts=artifacts
            )
            append_job_event(job_id, f"{len(pending_actions)} follow-up action(s) detected – awaiting MCP execution", "warning")
            for action in pending_actions[:5]:
                summary = action.get("summary") or action.get("status") or "Pending directive"
                append_job_event(job_id, f"{action.get('source', 'Warrior')}: {summary}", "info")
            return

        if not artifacts and not result.get("wish_granted", False):
            update_job_record(
                job_id,
                status="failed",
                completed_at=time.time(),
                progress=100,
                error="No actionable artifacts produced",
                result=result,
                pending_actions=pending_actions,
                artifacts=artifacts,
                message="Wish concluded without artifacts"
            )
            append_job_event(job_id, "Wish ended without verifiable artifacts", "error")
            return

        # Record detailed events
        warrior_responses = result.get("warrior_responses") or []
        for warrior in warrior_responses:
            fighter = warrior.get("fighter", "Warrior")
            emoji = warrior.get("emoji", "")
            response_time = warrior.get("response_time")
            success = warrior.get("success", True)
            event_type = "success" if success else "error"
            if success:
                msg = f"{emoji} {fighter} completed in {response_time:.1f}s" if response_time else f"{emoji} {fighter} completed"
            else:
                msg = f"{emoji} {fighter} failed"
            append_job_event(job_id, msg.strip(), event_type)

        consensus = result.get("consensus") or {}
        consensus_type = consensus.get("type")
        if consensus_type:
            summary = consensus.get("message", "").strip()
            consensus_message = f"Consensus: {consensus_type.upper()}"
            if summary:
                consensus_message += f" – {summary}"
            append_job_event(job_id, consensus_message, "info")

        synthesis_method = result.get("synthesis_method")
        if synthesis_method:
            append_job_event(job_id, f"Synthesis method: {synthesis_method}", "info")

        if result.get("passes"):
            append_job_event(job_id, f"Ultra Instinct passes: {result['passes']}", "info")

        update_job_record(
            job_id,
            status="completed",
            completed_at=time.time(),
            progress=100,
            result=result,
            message="Wish granted",
            pending_actions=pending_actions,
            artifacts=artifacts