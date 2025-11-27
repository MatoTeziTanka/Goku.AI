#!/usr/bin/env python3
"""
============================================================================
SHENRON v3.0 - Phase 1: Ingest Knowledge Base into ChromaDB
============================================================================
This script reads all markdown files from the knowledge base and creates
vector embeddings for semantic search (RAG).
============================================================================
"""

import os
import sys
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime

# Configuration
KNOWLEDGE_BASE_PATH = r"C:\GOKU-AI\knowledge-base"
CHROMA_DB_PATH = r"C:\GOKU-AI\chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, efficient model

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Print formatted step"""
    print(f"⚡ Step {step_num}: {text}")

def print_success(text):
    """Print success message"""
    print(f"   ✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"   ❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"   ℹ️  {text}")

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks for better context preservation.
    
    Args:
        text: The text to chunk
        chunk_size: Number of words per chunk
        overlap: Number of words to overlap between chunks
    
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks

def ingest_knowledge_base():
    """Main ingestion function"""
    
    print_header("🐉 SHENRON v3.0 - Knowledge Base Ingestion")
    
    # Step 1: Check if knowledge base exists
    print_step(1, "Checking knowledge base directory...")
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        print_error(f"Knowledge base not found at: {KNOWLEDGE_BASE_PATH}")
        print_info("Please create knowledge base files first!")
        return False
    print_success(f"Found knowledge base at: {KNOWLEDGE_BASE_PATH}")
    
    # Step 2: List knowledge base files
    print_step(2, "Scanning knowledge base files...")
    md_files = list(Path(KNOWLEDGE_BASE_PATH).glob("*.md"))
    
    if not md_files:
        print_error("No markdown files found in knowledge base!")
        return False
    
    print_success(f"Found {len(md_files)} markdown files:")
    for file in md_files:
        file_size = os.path.getsize(file) / 1024  # KB
        print(f"      - {file.name} ({file_size:.1f} KB)")
    
    # Step 3: Initialize ChromaDB
    print_step(3, "Initializing ChromaDB...")
    try:
        # Create persistent client
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # Initialize embedding function
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        
        # Delete existing collection if it exists (fresh start)
        try:
            client.delete_collection(name="knowledge_base")
            print_info("Deleted existing collection (fresh start)")
        except:
            pass
        
        # Create new collection
        collection = client.create_collection(
            name="knowledge_base",
            embedding_function=embedding_function,
            metadata={"description": "Seth's infrastructure knowledge base"}
        )
        
        print_success(f"ChromaDB initialized at: {CHROMA_DB_PATH}")
        print_info(f"Using embedding model: {EMBEDDING_MODEL}")
    except Exception as e:
        print_error(f"Failed to initialize ChromaDB: {e}")
        return False
    
    # Step 4: Process and ingest files
    print_step(4, "Processing and embedding knowledge base files...")
    
    total_chunks = 0
    documents = []
    metadatas = []
    ids = []
    
    for file in md_files:
        try:
            # Read file content
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks
            chunks = chunk_text(content, chunk_size=500, overlap=100)
            
            print_info(f"Processing {file.name}: {len(chunks)} chunks")
            
            # Add each chunk to collection
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file.stem}_chunk_{i}"
                documents.append(chunk)
                metadatas.append({
                    "source": file.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "ingested_at": datetime.now().isoformat()
                })
                ids.append(chunk_id)
            
            total_chunks += len(chunks)
            
        except Exception as e:
            print_error(f"Failed to process {file.name}: {e}")
            continue
    
    # Step 5: Add all documents to ChromaDB
    print_step(5, f"Adding {total_chunks} chunks to vector database...")
    try:
        # ChromaDB has a limit on batch size, so we add in batches
        batch_size = 166  # ChromaDB limit
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
            print_info(f"Added batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}")
        
        print_success(f"Successfully added {total_chunks} chunks to database")
    except Exception as e:
        print_error(f"Failed to add documents: {e}")
        return False
    
    # Step 6: Verify ingestion
    print_step(6, "Verifying ingestion...")
    try:
        count = collection.count()
        print_success(f"Database contains {count} documents")
        
        # Test query
        print_info("Testing semantic search...")
        results = collection.query(
            query_texts=["What is Seth's name?"],
            n_results=1
        )
        
        if results['documents']:
            print_success("Semantic search is working!")
            print(f"\n      Test query: 'What is Seth's name?'")
            print(f"      Top result preview: {results['documents'][0][0][:150]}...")
        else:
            print_error("No results from test query!")
            return False
            
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False
    
    # Success summary
    print("\n" + "="*70)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  ✅ KNOWLEDGE BASE INGESTION COMPLETE!                        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("")
    print("📊 INGESTION SUMMARY:")
    print(f"   - Files processed: {len(md_files)}")
    print(f"   - Total chunks: {total_chunks}")
    print(f"   - Database location: {CHROMA_DB_PATH}")
    print(f"   - Embedding model: {EMBEDDING_MODEL}")
    print("")
    print("🐉 RAG is now operational!")
    print("")
    print("🚀 NEXT STEP: Run 3-Build-Shenron-Orchestrator.py")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = ingest_knowledge_base()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

