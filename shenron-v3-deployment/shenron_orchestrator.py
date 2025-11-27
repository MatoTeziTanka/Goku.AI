<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""
============================================================================
SHENRON v3.0 - The Dragon Orchestrator
============================================================================
SHENRON consults the 6 DBZ-Fighters, analyzes their responses,
and provides a unified, synthesized answer with consensus detection.
============================================================================
"""

import requests
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import chromadb
from chromadb.utils import embedding_functions

# Configuration
LM_STUDIO_API = "http://<VM100_IP>:1234/v1"
CHROMA_DB_PATH = r"C:\GOKU-AI\chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

@dataclass
class Fighter:
    """DBZ-Fighter configuration"""
    name: str
    emoji: str
    role: str
    model: str
    temperature: float
    context_length: int = 32768
    max_tokens: int = 2048

# The 6 DBZ-Fighters (Updated with LM Studio API identifiers)
FIGHTERS = [
    Fighter("GOKU", "🥋", "Orchestrator & Shenron's Voice", "Goku-deepseek-coder-v2-lite-instruct", 0.7),
    Fighter("VEGETA", "👑", "Technical Authority", "Vegeta-llama-3.2-3b-instruct", 0.5),
    Fighter("PICCOLO", "🧠", "Strategic Sage", "Piccolo-qwen2.5-coder-7b-instruct", 0.6),
    Fighter("GOHAN", "⚠️", "Risk Sentinel", "Gohan-mistral-7b-instruct-v0.3", 0.4),
    Fighter("KRILLIN", "🔧", "Practical Engineer", "Krillin-phi-3-mini-128k-instruct", 0.6),
    Fighter("FRIEZA", "😈", "Chaos Tyrant", "Frieza-phi-3-mini-128k-instruct", 0.8),
]

class ShenronOrchestrator:
    """The Eternal Dragon that grants wishes through AI consensus"""
    
    def __init__(self):
        """Initialize SHENRON with RAG capabilities"""
        print("🐉 Initializing SHENRON...")
        
        # Initialize ChromaDB client
        try:
            self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL
            )
            self.collection = self.chroma_client.get_collection(
                name="knowledge_base",
                embedding_function=self.embedding_function
            )
            print("   ✅ RAG system initialized")
        except Exception as e:
            print(f"   ⚠️  RAG system not available: {e}")
            self.collection = None
    
    def search_knowledge_base(self, query: str, n_results: int = 3) -> str:
        """
        Search the knowledge base for relevant context.
        
        Args:
            query: The user's question
            n_results: Number of relevant chunks to retrieve
        
        Returns:
            Formatted context string
        """
        if not self.collection:
            return ""
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return ""
            
            # Format context
            context_parts = []
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i]['source']
                context_parts.append(f"[{source}] {doc}")
            
            context = "\n\n".join(context_parts)
            return f"**KNOWLEDGE BASE CONTEXT:**\n{context}\n\n"
            
        except Exception as e:
            print(f"   ⚠️  Knowledge base search failed: {e}")
            return ""
    
    def query_fighter(self, fighter: Fighter, user_query: str, context: str = "") -> Dict[str, Any]:
        """
        Query a single DBZ-Fighter.
        
        Args:
            fighter: Fighter configuration
            user_query: The user's question
            context: RAG context to inject
        
        Returns:
            Dictionary with fighter response and metadata
        """
        start_time = time.time()
        
        # Build prompt with context
        if context:
            prompt = f"{context}**USER QUESTION:**\n{user_query}"
        else:
            prompt = user_query
        
        try:
            response = requests.post(
                f"{LM_STUDIO_API}/chat/completions",
                json={
                    "model": fighter.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": fighter.temperature,
                    "max_tokens": fighter.max_tokens
                },
                timeout=900  # 15 minutes
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer = data['choices'][0]['message']['content']
                
                return {
                    "fighter": fighter.name,
                    "emoji": fighter.emoji,
                    "role": fighter.role,
                    "answer": answer,
                    "success": True,
                    "response_time": elapsed_time,
                    "temperature": fighter.temperature,
                    "model": fighter.model
                }
            else:
                return {
                    "fighter": fighter.name,
                    "emoji": fighter.emoji,
                    "role": fighter.role,
                    "answer": f"Error: HTTP {response.status_code}",
                    "success": False,
                    "response_time": elapsed_time
                }
                
        except requests.exceptions.Timeout:
            return {
                "fighter": fighter.name,
                "emoji": fighter.emoji,
                "role": fighter.role,
                "answer": "Error: Request timeout (>15 minutes)",
                "success": False,
                "response_time": 900
            }
        except Exception as e:
            return {
                "fighter": fighter.name,
                "emoji": fighter.emoji,
                "role": fighter.role,
                "answer": f"Error: {str(e)}",
                "success": False,
                "response_time": time.time() - start_time
            }
    
    def consult_council(self, user_query: str, use_rag: bool = True) -> Dict[str, Any]:
        """
        Consult all 6 DBZ-Fighters in parallel.
        
        Args:
            user_query: The user's question
            use_rag: Whether to search knowledge base first
        
        Returns:
            Dictionary with all fighter responses and metadata
        """
        print(f"\n🐉 SHENRON: Consulting the council...")
        print(f"   Question: {user_query[:100]}{'...' if len(user_query) > 100 else ''}")
        
        # Step 1: Search knowledge base (RAG)
        context = ""
        if use_rag:
            print(f"   📚 Searching knowledge base...")
            context = self.search_knowledge_base(user_query, n_results=3)
            if context:
                print(f"   ✅ Found relevant context ({len(context)} chars)")
            else:
                print(f"   ℹ️  No relevant context found (proceeding without RAG)")
        
        # Step 2: Query all fighters in parallel
        print(f"   ⚡ Querying 6 fighters in parallel...")
        responses = []
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(self.query_fighter, fighter, user_query, context): fighter
                for fighter in FIGHTERS
            }
            
            for future in as_completed(futures):
                fighter = futures[future]
                try:
                    result = future.result()
                    responses.append(result)
                    status = "✅" if result["success"] else "❌"
                    print(f"      {status} {result['emoji']} {result['fighter']} responded ({result['response_time']:.1f}s)")
                except Exception as e:
                    print(f"      ❌ {fighter.emoji} {fighter.name} failed: {e}")
                    responses.append({
                        "fighter": fighter.name,
                        "emoji": fighter.emoji,
                        "role": fighter.role,
                        "answer": f"Error: {str(e)}",
                        "success": False,
                        "response_time": 0
                    })
        
        # Step 3: Sort responses by original fighter order
        response_order = {f.name: i for i, f in enumerate(FIGHTERS)}
        responses.sort(key=lambda r: response_order.get(r['fighter'], 999))
        
        return {
            "query": user_query,
            "rag_context_used": bool(context),
            "responses": responses,
            "success_count": sum(1 for r in responses if r["success"]),
            "total_fighters": len(FIGHTERS)
        }
    
    def analyze_consensus(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze responses to detect consensus, conflicts, and novel ideas.
        
        Args:
            responses: List of fighter responses
        
        Returns:
            Consensus analysis
        """
        successful_responses = [r for r in responses if r["success"]]
        
        if not successful_responses:
            return {
                "type": "failure",
                "message": "No fighters were able to respond.",
                "consensus_level": 0
            }
        
        # Simple consensus detection (could be enhanced with NLP)
        success_rate = len(successful_responses) / len(responses)
        
        if success_rate == 1.0:
            consensus_type = "unanimous"
            message = f"All {len(responses)} fighters agree."
        elif success_rate >= 0.75:
            consensus_type = "strong"
            message = f"{len(successful_responses)}/{len(responses)} fighters provided answers."
        elif success_rate >= 0.5:
            consensus_type = "majority"
            message = f"{len(successful_responses)}/{len(responses)} fighters responded."
        else:
            consensus_type = "weak"
            message = f"Only {len(successful_responses)}/{len(responses)} fighters responded."
        
        return {
            "type": consensus_type,
            "message": message,
            "consensus_level": success_rate,
            "successful_fighters": [r['fighter'] for r in successful_responses],
            "failed_fighters": [r['fighter'] for r in responses if not r['success']]
        }
    
    def synthesize_response(self, council_result: Dict[str, Any]) -> str:
        """
        Synthesize a unified response from all fighter answers.
        
        This is a simple synthesis - in the future, we could use another AI
        to actually read all responses and create a true unified answer.
        
        Args:
            council_result: Results from consult_council()
        
        Returns:
            Synthesized response text
        """
        responses = council_result["responses"]
        successful = [r for r in responses if r["success"]]
        
        if not successful:
            return "Unfortunately, the council was unable to provide an answer at this time."
        
        # For now, combine all successful responses
        # In v4.0, we'd use an AI to synthesize these into one coherent answer
        synthesis = []
        
        for response in successful:
            synthesis.append(f"**{response['emoji']} {response['fighter']} ({response['role']}):**\n{response['answer']}")
        
        return "\n\n---\n\n".join(synthesis)
    
    def grant_wish(self, user_query: str, use_rag: bool = True) -> Dict[str, Any]:
        """
        Main entry point: Grant the user's wish by consulting the council.
        
        Args:
            user_query: The user's question/request
            use_rag: Whether to use knowledge base
        
        Returns:
            Complete response with consensus and synthesis
        """
        start_time = time.time()
        
        # Consult the council
        council_result = self.consult_council(user_query, use_rag=use_rag)
        
        # Analyze consensus
        consensus = self.analyze_consensus(council_result["responses"])
        
        # Synthesize response
        synthesized_answer = self.synthesize_response(council_result)
        
        elapsed_time = time.time() - start_time
        
        return {
            "query": user_query,
            "rag_used": council_result["rag_context_used"],
            "consensus": consensus,
            "synthesized_answer": synthesized_answer,
            "individual_responses": council_result["responses"],
            "total_time": elapsed_time,
            "wish_granted": consensus["consensus_level"] > 0
        }

def main():
    """Test SHENRON orchestrator"""
    print("\n" + "="*70)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  🐉 SHENRON v3.0 - The Eternal Dragon Awakens! ⚡             ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("="*70 + "\n")
    
    # Initialize SHENRON
    shenron = ShenronOrchestrator()
    
    # Test query
    test_query = "What is my name and mission?"
    print(f"\n📝 TEST QUERY: {test_query}\n")
    
    # Grant the wish
    result = shenron.grant_wish(test_query, use_rag=True)
    
    # Display results
    print("\n" + "="*70)
    print("🐉 SHENRON'S RESPONSE:")
    print("="*70)
    print(f"\n📊 Consensus: {result['consensus']['type'].upper()}")
    print(f"   {result['consensus']['message']}")
    print(f"\n⏱️  Total Time: {result['total_time']:.1f} seconds")
    print(f"📚 RAG Used: {'Yes' if result['rag_used'] else 'No'}")
    
    print("\n" + "-"*70)
    print("SYNTHESIZED ANSWER:")
    print("-"*70)
    print(result['synthesized_answer'])
    
    if result['wish_granted']:
        print("\n" + "="*70)
        print("✨ So be it. Your wish has been granted! ✨")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("⚠️  The dragon could not grant your wish at this time.")
        print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  SHENRON interrupted by user")
    except Exception as e:
        print(f"\n\n❌ SHENRON encountered an error: {e}")
        import traceback
        traceback.print_exc()

