#!/usr/bin/env python3
"""
SHENRON QUEST MANAGER API
Flask API for web UI integration

Endpoints:
- POST /api/quest/create - Create new quest
- GET /api/quest/list - List all quests
- GET /api/quest/<id> - Get quest details
- POST /api/quest/<id>/start - Start quest
- POST /api/quest/<id>/pause - Pause quest
- POST /api/quest/<id>/stop - Stop quest
- GET /api/quest/<id>/history - Get attempt history
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from quest_manager import QuestManager, QuestDatabase
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web UI

# Initialize Quest Manager
quest_manager = QuestManager()
db = QuestDatabase()

logger = logging.getLogger('QuestAPI')

@app.route('/api/quest/create', methods=['POST'])
def create_quest():
    """Create a new quest"""
    try:
        data = request.json
        goal = data.get('goal')
        
        if not goal:
            return jsonify({'error': 'Goal is required'}), 400
        
        strategy = data.get('strategy', 'adaptive')
        priority = data.get('priority', 5)
        max_attempts = data.get('max_attempts', -1)
        timeout_minutes = data.get('timeout_minutes', -1)
        metadata = data.get('metadata', {})
        
        quest_id = quest_manager.create_quest(
            goal=goal,
            strategy=strategy,
            priority=priority,
            max_attempts=max_attempts,
            timeout_minutes=timeout_minutes,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'quest_id': quest_id,
            'message': f'Quest created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating quest: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/list', methods=['GET'])
def list_quests():
    """List all quests"""
    try:
        status_filter = request.args.get('status')
        
        cursor = db.conn.cursor()
        if status_filter:
            cursor.execute('''
                SELECT id, goal, status, priority, attempts_count, 
                       success_count, best_score, created_at, started_at
                FROM quests 
                WHERE status = ?
                ORDER BY priority DESC, created_at DESC
            ''', (status_filter,))
        else:
            cursor.execute('''
                SELECT id, goal, status, priority, attempts_count, 
                       success_count, best_score, created_at, started_at
                FROM quests 
                ORDER BY priority DESC, created_at DESC
            ''')
        
        quests = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'quests': quests,
            'count': len(quests)
        })
        
    except Exception as e:
        logger.error(f"Error listing quests: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/<int:quest_id>', methods=['GET'])
def get_quest(quest_id):
    """Get quest details"""
    try:
        status = quest_manager.get_quest_status(quest_id)
        
        if 'error' in status:
            return jsonify(status), 404
        
        return jsonify({
            'success': True,
            'quest': status
        })
        
    except Exception as e:
        logger.error(f"Error getting quest {quest_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/<int:quest_id>/start', methods=['POST'])
def start_quest(quest_id):
    """Start a quest"""
    try:
        quest_manager.start_quest(quest_id)
        return jsonify({
            'success': True,
            'message': f'Quest {quest_id} started'
        })
    except Exception as e:
        logger.error(f"Error starting quest {quest_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/<int:quest_id>/pause', methods=['POST'])
def pause_quest(quest_id):
    """Pause a quest"""
    try:
        quest_manager.pause_quest(quest_id)
        return jsonify({
            'success': True,
            'message': f'Quest {quest_id} paused'
        })
    except Exception as e:
        logger.error(f"Error pausing quest {quest_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/<int:quest_id>/stop', methods=['POST'])
def stop_quest(quest_id):
    """Stop a quest"""
    try:
        quest_manager.stop_quest(quest_id)
        return jsonify({
            'success': True,
            'message': f'Quest {quest_id} stopped'
        })
    except Exception as e:
        logger.error(f"Error stopping quest {quest_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/<int:quest_id>/history', methods=['GET'])
def get_quest_history(quest_id):
    """Get quest attempt history"""
    try:
        limit = int(request.args.get('limit', 50))
        history = db.get_quest_history(quest_id, limit=limit)
        
        return jsonify({
            'success': True,
            'quest_id': quest_id,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        logger.error(f"Error getting history for quest {quest_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/stats', methods=['GET'])
def get_stats():
    """Get overall quest statistics"""
    try:
        cursor = db.conn.cursor()
        
        # Overall stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_quests,
                SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(attempts_count) as total_attempts,
                SUM(success_count) as total_successes
            FROM quests
        ''')
        stats = dict(cursor.fetchone())
        
        # Success rate
        if stats['total_attempts'] > 0:
            stats['success_rate'] = stats['total_successes'] / stats['total_attempts']
        else:
            stats['success_rate'] = 0
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quest/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'service': 'SHENRON Quest Manager API',
        'status': 'operational',
        'version': '1.0',
        'quest_manager_running': quest_manager.running
    })


if __name__ == '__main__':
    print("="*60)
    print("SHENRON QUEST MANAGER API v1.0")
    print("="*60)
    print("Endpoints:")
    print("  POST /api/quest/create")
    print("  GET  /api/quest/list")
    print("  GET  /api/quest/<id>")
    print("  POST /api/quest/<id>/start")
    print("  POST /api/quest/<id>/pause")
    print("  POST /api/quest/<id>/stop")
    print("  GET  /api/quest/<id>/history")
    print("  GET  /api/quest/stats")
    print("  GET  /api/quest/health")
    print("="*60)
    print("Starting on http://localhost:5001")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)

