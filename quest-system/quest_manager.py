#!/usr/bin/env python3
"""
SHENRON ETERNAL QUEST MANAGER v1.0
Autonomous background agent for continuous problem-solving

Features:
- Creates and manages quests
- Runs autonomous solution attempts in background
- Learns from successes and failures
- Integrates with 6 AI warriors via SHENRON orchestrator
- Tracks progress and notifies on breakthroughs
"""

import sqlite3
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:/GOKU-AI/quest-manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('QuestManager')

class QuestDatabase:
    """Manages SQLite database for quests and attempts"""
    
    def __init__(self, db_path: str = 'C:/GOKU-AI/quests.db'):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Quests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                strategy TEXT DEFAULT 'adaptive',
                status TEXT DEFAULT 'created',
                priority INTEGER DEFAULT 5,
                max_attempts INTEGER DEFAULT -1,
                timeout_minutes INTEGER DEFAULT -1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                paused_at TIMESTAMP,
                completed_at TIMESTAMP,
                attempts_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                best_solution TEXT,
                best_score REAL DEFAULT 0.0,
                notes TEXT,
                metadata TEXT
            )
        ''')
        
        # Attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quest_id INTEGER NOT NULL,
                attempt_number INTEGER NOT NULL,
                approach TEXT NOT NULL,
                strategy_used TEXT,
                result TEXT,
                score REAL DEFAULT 0.0,
                success BOOLEAN DEFAULT 0,
                execution_time REAL,
                ai_responses TEXT,
                learned TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quest_id) REFERENCES quests(id)
            )
        ''')
        
        # Quest checkpoints (for saving state)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quest_id INTEGER NOT NULL,
                state_data TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quest_id) REFERENCES quests(id)
            )
        ''')
        
        self.conn.commit()
        logger.info(f"Database initialized: {self.db_path}")
    
    def create_quest(self, goal: str, strategy: str = 'adaptive', 
                     priority: int = 5, max_attempts: int = -1,
                     timeout_minutes: int = -1, metadata: Dict = None) -> int:
        """Create a new quest"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO quests (goal, strategy, priority, max_attempts, 
                               timeout_minutes, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (goal, strategy, priority, max_attempts, timeout_minutes,
              json.dumps(metadata) if metadata else None))
        self.conn.commit()
        quest_id = cursor.lastrowid
        logger.info(f"Quest created: ID={quest_id}, Goal='{goal}'")
        return quest_id
    
    def get_quest(self, quest_id: int) -> Optional[Dict]:
        """Get quest by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM quests WHERE id = ?', (quest_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_active_quests(self) -> List[Dict]:
        """Get all running quests"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM quests 
            WHERE status = 'running' 
            ORDER BY priority DESC, created_at ASC
        ''')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_quest_status(self, quest_id: int, status: str):
        """Update quest status"""
        cursor = self.conn.cursor()
        timestamp_field = {
            'running': 'started_at',
            'paused': 'paused_at',
            'completed': 'completed_at',
            'failed': 'completed_at'
        }.get(status)
        
        if timestamp_field:
            cursor.execute(f'''
                UPDATE quests 
                SET status = ?, {timestamp_field} = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, quest_id))
        else:
            cursor.execute('UPDATE quests SET status = ? WHERE id = ?', 
                         (status, quest_id))
        self.conn.commit()
        logger.info(f"Quest {quest_id} status: {status}")
    
    def log_attempt(self, quest_id: int, attempt_number: int, approach: str,
                   result: str, score: float, success: bool, 
                   execution_time: float, ai_responses: Dict = None,
                   learned: str = None) -> int:
        """Log a quest attempt"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO attempts (quest_id, attempt_number, approach, result,
                                score, success, execution_time, ai_responses, learned)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (quest_id, attempt_number, approach, result, score, success,
              execution_time, json.dumps(ai_responses) if ai_responses else None,
              learned))
        self.conn.commit()
        
        # Update quest stats
        cursor.execute('''
            UPDATE quests 
            SET attempts_count = attempts_count + 1,
                success_count = success_count + ?
            WHERE id = ?
        ''', (1 if success else 0, quest_id))
        
        # Update best solution if this is better
        if success and score > 0:
            cursor.execute('''
                UPDATE quests 
                SET best_solution = ?, best_score = ?
                WHERE id = ? AND (best_score IS NULL OR best_score < ?)
            ''', (result, score, quest_id, score))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_quest_history(self, quest_id: int, limit: int = 50) -> List[Dict]:
        """Get attempt history for a quest"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM attempts 
            WHERE quest_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (quest_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class Quest:
    """Represents a single quest with its execution logic"""
    
    def __init__(self, quest_id: int, db: QuestDatabase, shenron_api: str):
        self.id = quest_id
        self.db = db
        self.shenron_api = shenron_api
        self.data = self.db.get_quest(quest_id)
        self.attempt_number = self.data['attempts_count']
        
    def should_continue(self) -> bool:
        """Check if quest should continue running"""
        # Refresh data
        self.data = self.db.get_quest(self.id)
        
        if self.data['status'] != 'running':
            return False
        
        # Check max attempts
        if self.data['max_attempts'] > 0:
            if self.data['attempts_count'] >= self.data['max_attempts']:
                logger.info(f"Quest {self.id}: Max attempts reached")
                return False
        
        # Check timeout
        if self.data['timeout_minutes'] > 0 and self.data['started_at']:
            start_time = datetime.fromisoformat(self.data['started_at'])
            elapsed = (datetime.now() - start_time).total_seconds() / 60
            if elapsed >= self.data['timeout_minutes']:
                logger.info(f"Quest {self.id}: Timeout reached")
                return False
        
        return True
    
    def generate_approach(self) -> str:
        """Generate a new approach to try"""
        # Get past attempts to learn from
        history = self.db.get_quest_history(self.id, limit=10)
        
        # Build context for SHENRON
        context = f"Quest Goal: {self.data['goal']}\n\n"
        context += f"Attempt #{self.attempt_number + 1}\n"
        context += f"Strategy: {self.data['strategy']}\n\n"
        
        if history:
            context += "Previous attempts:\n"
            for i, attempt in enumerate(reversed(history[-5:]), 1):
                context += f"{i}. {attempt['approach']} -> "
                context += f"{'SUCCESS' if attempt['success'] else 'FAILED'} "
                context += f"(score: {attempt['score']})\n"
                if attempt['learned']:
                    context += f"   Learned: {attempt['learned']}\n"
            context += "\n"
        
        context += "What is a NEW approach to try? Be specific and actionable."
        
        return context
    
    def execute_attempt(self) -> Dict[str, Any]:
        """Execute one solution attempt"""
        start_time = time.time()
        self.attempt_number += 1
        
        logger.info(f"Quest {self.id}: Starting attempt #{self.attempt_number}")
        
        # Generate approach
        approach_query = self.generate_approach()
        
        try:
            # Query SHENRON orchestrator
            response = requests.post(
                f"{self.shenron_api}/api/shenron/grant-wish",
                json={"query": approach_query, "use_rag": True},
                timeout=300  # 5 minute timeout
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract suggested approach
            approach = data.get('synthesized_answer', '')
            
            # Evaluate the approach (simplified for Phase 1)
            # In Phase 2, this would actually execute and test the solution
            score = self._evaluate_approach(approach, data)
            success = score >= 0.7  # 70% threshold
            
            execution_time = time.time() - start_time
            
            # Determine what we learned
            learned = self._extract_learning(data, success, score)
            
            # Log the attempt
            self.db.log_attempt(
                quest_id=self.id,
                attempt_number=self.attempt_number,
                approach=approach[:500],  # Truncate for storage
                result=json.dumps(data.get('consensus', {})),
                score=score,
                success=success,
                execution_time=execution_time,
                ai_responses=data.get('individual_responses', {}),
                learned=learned
            )
            
            logger.info(f"Quest {self.id}: Attempt #{self.attempt_number} - "
                       f"{'SUCCESS' if success else 'FAILED'} (score: {score:.2f})")
            
            return {
                'success': success,
                'score': score,
                'approach': approach,
                'learned': learned,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"Quest {self.id}: Attempt failed: {e}")
            execution_time = time.time() - start_time
            
            self.db.log_attempt(
                quest_id=self.id,
                attempt_number=self.attempt_number,
                approach=f"ERROR: {str(e)}",
                result=str(e),
                score=0.0,
                success=False,
                execution_time=execution_time,
                learned=f"Error encountered: {str(e)}"
            )
            
            return {
                'success': False,
                'score': 0.0,
                'error': str(e),
                'execution_time': execution_time
            }
    
    def _evaluate_approach(self, approach: str, shenron_data: Dict) -> float:
        """
        Evaluate how good an approach is
        Phase 1: Based on AI consensus
        Phase 2: Will actually test the solution
        """
        consensus = shenron_data.get('consensus', {})
        consensus_level = consensus.get('consensus_level', 0)
        
        # Higher consensus = better approach
        # 4 = UNANIMOUS (100%), 3 = STRONG (75%), 2 = MAJORITY (50%), 1 = WEAK (25%)
        score = consensus_level / 4.0
        
        # Bonus for specific, actionable approaches
        if any(keyword in approach.lower() for keyword in 
               ['step 1', 'first', 'configure', 'set', 'run', 'execute']):
            score += 0.1
        
        return min(1.0, score)
    
    def _extract_learning(self, shenron_data: Dict, success: bool, score: float) -> str:
        """Extract what we learned from this attempt"""
        consensus = shenron_data.get('consensus', {})
        
        if success:
            return f"Strong consensus approach (score: {score:.2f}). " \
                   f"Consensus: {consensus.get('summary', 'N/A')}"
        else:
            return f"Low consensus (score: {score:.2f}). Need more specific approach. " \
                   f"Conflicts: {len(consensus.get('conflicts', []))}"


class QuestManager:
    """Main quest manager orchestrating all quests"""
    
    def __init__(self, shenron_api: str = "http://localhost:5000"):
        self.db = QuestDatabase()
        self.shenron_api = shenron_api
        self.running = False
        logger.info("Quest Manager initialized")
    
    def create_quest(self, goal: str, **kwargs) -> int:
        """Create a new quest"""
        return self.db.create_quest(goal, **kwargs)
    
    def start_quest(self, quest_id: int):
        """Start a quest"""
        self.db.update_quest_status(quest_id, 'running')
    
    def pause_quest(self, quest_id: int):
        """Pause a quest"""
        self.db.update_quest_status(quest_id, 'paused')
    
    def stop_quest(self, quest_id: int):
        """Stop a quest"""
        self.db.update_quest_status(quest_id, 'stopped')
    
    def get_quest_status(self, quest_id: int) -> Dict:
        """Get current quest status"""
        quest_data = self.db.get_quest(quest_id)
        if not quest_data:
            return {'error': 'Quest not found'}
        
        history = self.db.get_quest_history(quest_id, limit=5)
        
        return {
            'id': quest_id,
            'goal': quest_data['goal'],
            'status': quest_data['status'],
            'attempts': quest_data['attempts_count'],
            'successes': quest_data['success_count'],
            'best_score': quest_data['best_score'],
            'best_solution': quest_data['best_solution'],
            'recent_attempts': history
        }
    
    def run_quest_loop(self, quest_id: int, delay_seconds: int = 60):
        """
        Run quest loop for a single quest
        This would be called by the Windows service
        """
        quest = Quest(quest_id, self.db, self.shenron_api)
        
        logger.info(f"Starting quest loop: {quest_id}")
        
        while quest.should_continue():
            try:
                result = quest.execute_attempt()
                
                if result['success']:
                    logger.info(f"Quest {quest_id}: SUCCESS! Score: {result['score']}")
                    # Could notify user here
                
                # Wait before next attempt
                time.sleep(delay_seconds)
                
            except Exception as e:
                logger.error(f"Quest {quest_id}: Error in loop: {e}")
                time.sleep(delay_seconds)
        
        # Quest finished
        final_data = self.db.get_quest(quest_id)
        if final_data['success_count'] > 0:
            self.db.update_quest_status(quest_id, 'completed')
            logger.info(f"Quest {quest_id}: COMPLETED")
        else:
            self.db.update_quest_status(quest_id, 'failed')
            logger.info(f"Quest {quest_id}: FAILED")
    
    def run_manager_loop(self, delay_seconds: int = 10):
        """
        Main manager loop - monitors all active quests
        This runs as the Windows service
        """
        self.running = True
        logger.info("Quest Manager loop started")
        
        while self.running:
            try:
                active_quests = self.db.get_active_quests()
                
                if not active_quests:
                    logger.debug("No active quests")
                    time.sleep(delay_seconds)
                    continue
                
                # Process each active quest
                for quest_data in active_quests:
                    quest = Quest(quest_data['id'], self.db, self.shenron_api)
                    
                    if quest.should_continue():
                        try:
                            result = quest.execute_attempt()
                            logger.info(f"Quest {quest_data['id']}: "
                                      f"Attempt result - {result}")
                        except Exception as e:
                            logger.error(f"Quest {quest_data['id']}: Error: {e}")
                
                # Wait before next iteration
                time.sleep(delay_seconds)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Manager loop error: {e}")
                time.sleep(delay_seconds)
        
        logger.info("Quest Manager loop stopped")
    
    def stop(self):
        """Stop the manager"""
        self.running = False
        self.db.close()


# CLI Interface for testing
if __name__ == '__main__':
    import sys
    
    manager = QuestManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create' and len(sys.argv) > 2:
            goal = ' '.join(sys.argv[2:])
            quest_id = manager.create_quest(goal)
            print(f"Quest created: ID={quest_id}")
        
        elif command == 'start' and len(sys.argv) > 2:
            quest_id = int(sys.argv[2])
            manager.start_quest(quest_id)
            print(f"Quest {quest_id} started")
        
        elif command == 'status' and len(sys.argv) > 2:
            quest_id = int(sys.argv[2])
            status = manager.get_quest_status(quest_id)
            print(json.dumps(status, indent=2))
        
        elif command == 'run' and len(sys.argv) > 2:
            quest_id = int(sys.argv[2])
            manager.run_quest_loop(quest_id)
        
        elif command == 'service':
            # Run as service
            manager.run_manager_loop()
    
    else:
        print("SHENRON Quest Manager v1.0")
        print("Usage:")
        print("  python quest_manager.py create <goal>")
        print("  python quest_manager.py start <quest_id>")
        print("  python quest_manager.py status <quest_id>")
        print("  python quest_manager.py run <quest_id>")
        print("  python quest_manager.py service")

