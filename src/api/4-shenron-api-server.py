<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""
============================================================================
SHENRON v3.0 - API Server
============================================================================
Flask API server that exposes SHENRON's capabilities via HTTP endpoints.
This replaces the direct fighter queries in api.php.
============================================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import SHENRON orchestrator
# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shenron_orchestrator import ShenronOrchestrator

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize SHENRON (singleton)
print("🐉 Initializing SHENRON API Server...")
shenron = ShenronOrchestrator()
print("✅ SHENRON is ready to grant wishes!\n")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "SHENRON v3.0",
        "dragon_awakened": True
    })

@app.route('/api/shenron/grant-wish', methods=['POST'])
def grant_wish():
    """
    Main endpoint: Grant a wish by consulting the council
    
    Request JSON:
    {
        "query": "What is my name?",
        "use_rag": true
    }
    
    Response JSON:
    {
        "query": "...",
        "rag_used": true,
        "consensus": {...},
        "synthesized_answer": "...",
        "individual_responses": [...],
        "total_time": 45.2,
        "wish_granted": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in request",
                "wish_granted": False
            }), 400
        
        user_query = data['query']
        use_rag = data.get('use_rag', True)
        
        # Grant the wish
        result = shenron.grant_wish(user_query, use_rag=use_rag)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "wish_granted": False
        }), 500

@app.route('/api/shenron/search-knowledge', methods=['POST'])
def search_knowledge():
    """
    Search the knowledge base directly
    
    Request JSON:
    {
        "query": "What VMs are running?",
        "n_results": 5
    }
    
    Response JSON:
    {
        "query": "...",
        "results": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in request"
            }), 400
        
        user_query = data['query']
        n_results = data.get('n_results', 3)
        
        context = shenron.search_knowledge_base(user_query, n_results=n_results)
        
        return jsonify({
            "query": user_query,
            "context": context,
            "found": bool(context)
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/shenron/fighters', methods=['GET'])
def list_fighters():
    """List all DBZ-Fighters"""
    from shenron_orchestrator import FIGHTERS
    
    fighters_info = []
    for fighter in FIGHTERS:
        fighters_info.append({
            "name": fighter.name,
            "emoji": fighter.emoji,
            "role": fighter.role,
            "model": fighter.model,
            "temperature": fighter.temperature,
            "context_length": fighter.context_length,
            "max_tokens": fighter.max_tokens
        })
    
    return jsonify({
        "fighters": fighters_info,
        "count": len(fighters_info)
    })

def main():
    """Start the SHENRON API server"""
    print("\n" + "="*70)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  🐉 SHENRON API SERVER v3.0 - Starting...                    ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("="*70 + "\n")
    
    print("📡 API ENDPOINTS:")
    print("   GET  /health                       - Health check")
    print("   POST /api/shenron/grant-wish       - Grant a wish (main)")
    print("   POST /api/shenron/search-knowledge - Search knowledge base")
    print("   GET  /api/shenron/fighters         - List all fighters")
    print("")
    print("🌐 Server will be available at:")
    print("   http://localhost:5000")
    print("   http://<VM100_IP>:5000")
    print("")
    print("🐉 SHENRON is ready to grant wishes!")
    print("="*70 + "\n")
    
    # Start Flask server
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,
        debug=False,
        threaded=True
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  SHENRON API Server shut down by user")
    except Exception as e:
        print(f"\n\n❌ SHENRON API Server error: {e}")
        import traceback
        traceback.print_exc()

