#!/usr/bin/env python3
"""
Create Warrior State Machines for Goku.AI
Implements state tracking for each warrior as per Master Prompt v3.0.0
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).parent.parent
STATES_FILE = REPO_ROOT / "src" / "services" / "warrior_states.py"
STATES_JSON = REPO_ROOT / "src" / "services" / "warrior_states.json"

# Warrior configurations
WARRIORS = {
    "goku": {"emoji": "🥋", "model": "deepseek-coder-v2-lite", "temp": 0.7},
    "vegeta": {"emoji": "👑", "model": "llama-3.2-3b", "temp": 0.3},
    "piccolo": {"emoji": "🧠", "model": "qwen2.5-coder-7b", "temp": 0.5},
    "gohan": {"emoji": "⚠️", "model": "mistral-7b", "temp": 0.4},
    "krillin": {"emoji": "🔧", "model": "phi-3-mini-128k", "temp": 0.6},
    "frieza": {"emoji": "😈", "model": "phi-3-mini-128k", "temp": 0.9}
}

PYTHON_TEMPLATE = '''"""
Warrior State Machines for Goku.AI
Implements state tracking for each warrior as per Master Prompt v3.0.0

State Machine tracks:
- Current task
- Task queue
- Memory log
- Last activity timestamp
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WarriorTask:
    """Represents a single task for a warrior."""
    task_id: str
    query: str
    status: TaskStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

@dataclass
class WarriorState:
    """State machine for a single warrior."""
    warrior_name: str
    emoji: str
    model: str
    current_task: Optional[WarriorTask] = None
    queue: List[WarriorTask] = None
    memory_log: List[Dict[str, Any]] = None
    last_activity: Optional[str] = None
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    
    def __post_init__(self):
        if self.queue is None:
            self.queue = []
        if self.memory_log is None:
            self.memory_log = []

class WarriorStateManager:
    """Manages state for all warriors."""
    
    def __init__(self, state_file: Path = None):
        if state_file is None:
            state_file = Path(__file__).parent / "warrior_states.json"
        self.state_file = state_file
        self.states: Dict[str, WarriorState] = {}
        self._load_states()
    
    def _load_states(self):
        """Load states from JSON file."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding='utf-8'))
                for name, state_data in data.items():
                    # Reconstruct state from dict
                    state = WarriorState(**state_data)
                    self.states[name] = state
            except Exception as e:
                print(f"⚠️  Error loading states: {e}")
                self._initialize_states()
        else:
            self._initialize_states()
    
    def _initialize_states(self):
        """Initialize states for all warriors."""
        warriors_config = {
            "goku": {"emoji": "🥋", "model": "deepseek-coder-v2-lite", "temp": 0.7},
            "vegeta": {"emoji": "👑", "model": "llama-3.2-3b", "temp": 0.3},
            "piccolo": {"emoji": "🧠", "model": "qwen2.5-coder-7b", "temp": 0.5},
            "gohan": {"emoji": "⚠️", "model": "mistral-7b", "temp": 0.4},
            "krillin": {"emoji": "🔧", "model": "phi-3-mini-128k", "temp": 0.6},
            "frieza": {"emoji": "😈", "model": "phi-3-mini-128k", "temp": 0.9}
        }
        
        for name, config in warriors_config.items():
            self.states[name] = WarriorState(
                warrior_name=name,
                emoji=config["emoji"],
                model=config["model"]
            )
    
    def save_states(self):
        """Save states to JSON file."""
        data = {}
        for name, state in self.states.items():
            state_dict = asdict(state)
            # Convert enums to strings
            if state_dict.get("current_task"):
                if isinstance(state_dict["current_task"].get("status"), TaskStatus):
                    state_dict["current_task"]["status"] = state_dict["current_task"]["status"].value
            data[name] = state_dict
        
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
    
    def get_state(self, warrior_name: str) -> Optional[WarriorState]:
        """Get state for a specific warrior."""
        return self.states.get(warrior_name.lower())
    
    def add_task(self, warrior_name: str, query: str) -> str:
        """Add a task to warrior's queue."""
        warrior = self.get_state(warrior_name)
        if not warrior:
            raise ValueError(f"Unknown warrior: {warrior_name}")
        
        task_id = f"{warrior_name}_{datetime.now().isoformat()}"
        task = WarriorTask(
            task_id=task_id,
            query=query,
            status=TaskStatus.PENDING,
            created_at=datetime.now().isoformat()
        )
        
        warrior.queue.append(task)
        warrior.last_activity = datetime.now().isoformat()
        self.save_states()
        
        return task_id
    
    def start_task(self, warrior_name: str, task_id: str):
        """Mark a task as running."""
        warrior = self.get_state(warrior_name)
        if not warrior:
            return
        
        # Find task in queue
        for task in warrior.queue:
            if task.task_id == task_id:
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now().isoformat()
                warrior.current_task = task
                warrior.last_activity = datetime.now().isoformat()
                self.save_states()
                return
    
    def complete_task(self, warrior_name: str, task_id: str, result: str):
        """Mark a task as completed."""
        warrior = self.get_state(warrior_name)
        if not warrior:
            return
        
        for task in warrior.queue:
            if task.task_id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                task.result = result
                warrior.current_task = None
                warrior.total_tasks_completed += 1
                warrior.last_activity = datetime.now().isoformat()
                
                # Add to memory log
                warrior.memory_log.append({
                    "task_id": task_id,
                    "query": task.query,
                    "result": result,
                    "completed_at": task.completed_at
                })
                
                # Keep only last 100 entries
                if len(warrior.memory_log) > 100:
                    warrior.memory_log = warrior.memory_log[-100:]
                
                self.save_states()
                return

# Global state manager instance
_state_manager = None

def get_state_manager() -> WarriorStateManager:
    """Get global state manager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = WarriorStateManager()
    return _state_manager
'''

def create_warrior_states():
    """Create warrior state machines file."""
    
    print("=" * 70)
    print("CREATING WARRIOR STATE MACHINES".center(70))
    print("=" * 70)
    print()
    
    # Create directory if needed
    STATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Write Python file
    STATES_FILE.write_text(PYTHON_TEMPLATE, encoding='utf-8')
    print(f"✅ Created: {STATES_FILE}")
    
    # Initialize JSON state file
    initial_states = {}
    for name, config in WARRIORS.items():
        initial_states[name] = {
            "warrior_name": name,
            "emoji": config["emoji"],
            "model": config["model"],
            "current_task": None,
            "queue": [],
            "memory_log": [],
            "last_activity": None,
            "total_tasks_completed": 0,
            "total_tasks_failed": 0
        }
    
    STATES_JSON.write_text(json.dumps(initial_states, indent=2), encoding='utf-8')
    print(f"✅ Created: {STATES_JSON}")
    print()
    
    print("=" * 70)
    print("✅ WARRIOR STATE MACHINES CREATED".center(70))
    print("=" * 70)
    print()
    print("Files created:")
    print(f"  - {STATES_FILE.relative_to(REPO_ROOT)}")
    print(f"  - {STATES_JSON.relative_to(REPO_ROOT)}")
    print()
    print("Next: Import in your API:")
    print("  from src.services.warrior_states import get_state_manager")
    print()

if __name__ == "__main__":
    create_warrior_states()

