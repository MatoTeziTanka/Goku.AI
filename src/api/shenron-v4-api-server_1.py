<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
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
    "lightning": 120,   # seconds
    "council": 300,
    "ultra": 1800
}

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
    with jobs_lock:
        return jobs.get(job_id, {}).copy()

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
            message = "Wish cancelled before processing began"
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
        )
        append_job_event(job_id, "Wish granted successfully", "success")
    except WishCancelled:
        finalize_cancelled_job(job_id, "Wish cancelled by user")
        append_job_event(job_id, "Wish cancelled", "warning")
    except Exception as exc:
        update_job_record(
            job_id,
            status="failed",
            completed_at=time.time(),
            progress=100,
            error=str(exc),
            message=f"Failed: {exc}"
        )
        append_job_event(job_id, f"Wish failed: {exc}", "error")

@app.route('/api/shenron/grant-wish', methods=['POST'])
def grant_wish():
    """
    Main endpoint: Grant a wish with POWER MODE support (sync or async)
    """
    try:
        data = request.get_json() or {}

        if 'query' not in data:
            return jsonify({
                "error": "Missing 'query' parameter",
                "wish_granted": False
            }), 400

        query = data['query']
        power_mode = data.get('power_mode', 'council')
        use_rag = data.get('use_rag', True)
        async_mode = bool(data.get('async_mode') or data.get('async'))
        agent_mode = bool(data.get('agent_mode'))

        if async_mode:
            job_id = create_job_record(query, power_mode, agent_mode)
            worker = threading.Thread(
                target=process_wish_job,
                args=(job_id, query, power_mode, use_rag, agent_mode),
                daemon=True
            )
            worker.start()
            return jsonify({
                "job_id": job_id,
                "status": "queued"
            }), 202

        result = perform_grant_wish(query, power_mode=power_mode, use_rag=use_rag)
        return jsonify(result)

    except Exception as e:
        print(f"    Error: {e}")
        return jsonify({
            "error": str(e),
            "wish_granted": False
        }), 500

@app.route('/api/shenron/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    """Return status/result for asynchronous wish processing."""
    job = get_job_record(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    response = {
        "job_id": job_id,
        "status": job.get("status", "unknown"),
        "progress": job.get("progress", 0),
        "power_mode": job.get("power_mode"),
        "agent_mode": job.get("agent_mode"),
        "created_at": job.get("created_at"),
        "started_at": job.get("started_at"),
        "completed_at": job.get("completed_at"),
        "message": job.get("message"),
        "events": job.get("events", []),
        "expected_duration": job.get("expected_duration"),
        "pending_actions": job.get("pending_actions", []),
        "artifacts": job.get("artifacts", [])
    }

    if job.get("status") in ("completed", "action_required"):
        response["result"] = job.get("result")
    elif job.get("status") == "failed":
        response["error"] = job.get("error", "Unknown error")

    started_at = job.get("started_at")
    if started_at:
        elapsed = time.time() - started_at
        response["elapsed_seconds"] = elapsed
        expected = job.get("expected_duration") or JOB_EXPECTED_DURATIONS.get(job.get("power_mode", ""), 300)
        remaining = max(0, expected - elapsed) if expected else None
        response["estimated_remaining"] = remaining
        if remaining is not None:
            response["eta_timestamp"] = time.time() + remaining

    return jsonify(response)

@app.route('/api/shenron/cancel-job/<job_id>', methods=['POST'])
def cancel_job(job_id):
    """Request cancellation of a queued or running wish job."""
    success, message = request_job_cancellation(job_id)
    status_code = 200 if success else 400
    return jsonify({
        "job_id": job_id,
        "success": success,
        "message": message
    }), status_code

@app.route('/api/shenron/metrics', methods=['GET'])
def system_metrics():
    """Provide system, LM Studio, and job queue metrics."""
    return jsonify(get_system_metrics())


def execute_lightning_mode(query, cancel_checker=None):
    """
    ⚡ LIGHTNING MODE: Single warrior (Goku), fastest response
    - Power: 1,000
    - Accuracy: 85-90%
    - Time: 5-10s
    """
    import time
    
    start_time = time.time()
    
    if cancel_checker and cancel_checker():
        raise WishCancelled()

    # Use the orchestrator's consult_council but limit to partial result
    # For now, just use standard grant_wish with RAG disabled
    result = shenron.grant_wish(query, use_rag=False, cancel_checker=cancel_checker)
    
    # Extract just Goku's response (first warrior)
    if result.get('warrior_responses'):
        goku_response = result['warrior_responses'][0]
        
        total_time = time.time() - start_time
        
        return shenron.post_process_result({
            'query': query,
            'rag_used': False,
            'warrior_responses': [goku_response],
            'synthesized_answer': goku_response['answer'],
            'consensus': {'type': 'single_warrior', 'message': 'Lightning mode - single warrior response'},
            'synthesis_method': 'lightning',
            'total_time': total_time,
            'wish_granted': True
        })
    
    # Fallback to standard result
    result['synthesis_method'] = 'lightning'
    return shenron.post_process_result(result)


def execute_ultra_instinct_mode(query, use_rag=True, cancel_checker=None):
    """
    🐉 ULTRA INSTINCT MODE: Multi-pass with conflict resolution
    - Power: OVER 9000!
    - Accuracy: 99.99999999%
    - Time: 60-180s
    """
    import time
    
    start_time = time.time()
    
    # Pass 1: Standard council consensus
    result_pass1 = shenron.grant_wish(query, use_rag=use_rag, cancel_checker=cancel_checker)
    
    # Check consensus for conflicts
    consensus_type = result_pass1.get('consensus', {}).get('type', 'unknown')
    
    if consensus_type in ['split', 'conflicted', 'weak']:
        # Pass 2: Re-query with focus on conflict resolution
        print(f"   🐉 Detected {consensus_type} consensus - initiating second pass...")
        
        debate_query = f"Regarding '{query}', synthesize the best answer considering all perspectives."
        if cancel_checker and cancel_checker():
            raise WishCancelled()
        result_pass2 = shenron.grant_wish(debate_query, use_rag=use_rag, cancel_checker=cancel_checker)
        
        # Use second pass synthesis as final answer
        final_answer = result_pass2['synthesized_answer']
        passes = 2
    else:
        # Consensus is strong, use first pass
        final_answer = result_pass1['synthesized_answer']
        passes = 1
    
    total_time = time.time() - start_time
    
    result_pass1['synthesized_answer'] = final_answer
    result_pass1['synthesis_method'] = 'ultra_instinct'
    result_pass1['total_time'] = total_time
    result_pass1['passes'] = passes
    
    return shenron.post_process_result(result_pass1)

@app.route('/api/shenron/search-knowledge', methods=['POST'])
def search_knowledge():
    """
    Direct knowledge base search
    
    Request:
        {
            "query": "infrastructure details",
            "n_results": 3
        }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        query = data['query']
        n_results = data.get('n_results', 3)

        context = shenron.search_knowledge_base(query, n_results=n_results)

        return jsonify({
            "query": query,
            "context": context,
            "found": bool(context)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shenron/fighters', methods=['GET'])
def list_fighters():
    """List all DBZ-Warriors and their configurations"""
    from shenron_v4_orchestrator import FIGHTERS

    fighters_info = []
    for f in FIGHTERS:
        fighters_info.append({
            "name": f.name,
            "emoji": f.emoji,
            "role": f.role,
            "model": f.model,
            "temperature": f.temperature,
            "context_length": f.context_length,
            "max_tokens": f.max_tokens
        })

    return jsonify({
        "fighters": fighters_info,
        "total": len(fighters_info)
    })

@app.route('/api/shenron/execute-command', methods=['POST'])
def execute_command():
    """
    NEW v4.0: Execute SSH command (AGENT MODE)
    
    Request:
        {
            "host": "vm150",
            "command": "df -h",
            "require_approval": true
        }
    
    Response:
        {
            "success": true,
            "output": "...",
            "classification": "safe",
            "executed": true
        }
        
        OR (if approval needed):
        {
            "success": false,
            "approval_required": true,
            "classification": "moderate",
            "command": "...",
            "message": "Command requires approval"
        }
    """
    try:
        data = request.get_json()

        if not data or 'host' not in data or 'command' not in data:
            return jsonify({
                "error": "Missing 'host' or 'command' parameter",
                "success": False
            }), 400

        host = data['host']
        command = data['command']
        require_approval = data.get('require_approval', True)

        print(f"\n Agent mode: {host} -> {command}")

        result = shenron.execute_command(host, command, require_approval=require_approval)

        if result.get('approval_required'):
            print(f"     Approval required ({result['classification']})")
        elif result.get('executed'):
            print(f"    Executed successfully")
        else:
            print(f"    Execution failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        print(f"    Error: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/shenron/approve-command', methods=['POST'])
def approve_command():
    """
    NEW v4.0: Approve and execute a moderate/unknown command
    
    Request:
        {
            "host": "vm150",
            "command": "systemctl restart apache2",
            "approved": true
        }
    """
    try:
        data = request.get_json()

        if not data or 'host' not in data or 'command' not in data:
            return jsonify({
                "error": "Missing 'host' or 'command' parameter",
                "success": False
            }), 400

        if not data.get('approved'):
            return jsonify({
                "success": False,
                "message": "Command not approved",
                "executed": False
            })

        host = data['host']
        command = data['command']

        print(f"\n Executing APPROVED command: {host} -> {command}")

        # Execute with approval bypass
        result = shenron.execute_command(host, command, require_approval=False)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("")
    print("         SHENRON API SERVER v4.0 - Starting...               ")
    print("")
    print("="*70 + "\n")

    print(" API ENDPOINTS:")
    print("   GET  /health                      - Health check")
    print("   POST /api/shenron/grant-wish      - Grant a wish (main)")
    print("   POST /api/shenron/search-knowledge - Search knowledge base")
    print("   GET  /api/shenron/fighters        - List all fighters")
    print("   POST /api/shenron/execute-command - Execute SSH command (agent mode)")
    print("   POST /api/shenron/approve-command - Approve and execute command")
    print("\n Server will be available at:")
    print("   http://localhost:5000")
    print("   http://<VM100_IP>:5000")
    print("\n SHENRON is ready to grant wishes!")
    print("="*70 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False)

