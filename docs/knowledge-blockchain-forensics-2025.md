# Blockchain Forensics & Transaction Analysis (2025)

**Purpose:** Comprehensive guide to analyzing Bitcoin blockchain for puzzle clues  
**Application:** Crypto puzzle solving, transaction tracking, pattern detection  
**Updated:** November 6, 2025  
**Skill Level:** Intermediate to Advanced

---

## 🔍 **WHAT IS BLOCKCHAIN FORENSICS?**

**Definition:** The process of analyzing blockchain data to extract meaningful information, track transactions, and identify patterns.

**In Crypto Puzzles:**
- Analyzing puzzle creator's transactions for clues
- Tracking when funds were added/moved
- Identifying transaction patterns
- Extracting hidden messages from transaction data
- Following the money trail

---

## 🌐 **BLOCKCHAIN EXPLORERS**

### **1. Blockchain.com**
- **URL:** https://www.blockchain.com/explorer
- **Best For:** General use, simple interface
- **Features:**
  - Transaction history
  - Address balance
  - Block information
  - Charts and statistics

### **2. Blockchair.com**
- **URL:** https://blockchair.com/bitcoin
- **Best For:** Advanced queries, API access
- **Features:**
  - SQL-like queries
  - Multiple cryptocurrencies
  - Privacy coins support
  - Advanced filters

**Example Query:**
```sql
SELECT * FROM transactions 
WHERE output_total > 1000000000 
AND time > '2020-01-01'
```

### **3. OXT.me (Samourai Wallet)**
- **URL:** https://oxt.me/
- **Best For:** Privacy analysis, UTXO tracking
- **Features:**
  - UTXO graph visualization
  - CoinJoin detection
  - Address clustering
  - Privacy score

### **4. Mempool.space**
- **URL:** https://mempool.space/
- **Best For:** Real-time mempool monitoring
- **Features:**
  - Fee estimation
  - Transaction acceleration
  - Lightning Network data
  - Open-source, self-hostable

---

## 🔬 **TRANSACTION ANALYSIS TECHNIQUES**

### **Method 1: Address Balance & History**

**Basic Query:**
```python
import requests

def get_address_info(address):
    """Get Bitcoin address information"""
    url = f"https://blockchain.info/address/{address}?format=json"
    response = requests.get(url)
    data = response.json()
    
    return {
        'address': address,
        'total_received': data['total_received'] / 100000000,  # Convert satoshis to BTC
        'total_sent': data['total_sent'] / 100000000,
        'final_balance': data['final_balance'] / 100000000,
        'n_tx': data['n_tx'],
        'transactions': data['txs'][:10]  # Last 10 transactions
    }

# Example: Puzzle #66
address = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
info = get_address_info(address)

print(f"Address: {info['address']}")
print(f"Balance: {info['final_balance']} BTC")
print(f"Total Transactions: {info['n_tx']}")
print(f"Total Received: {info['total_received']} BTC")
```

---

### **Method 2: Transaction Timing Analysis**

**Identifying Patterns:**
```python
import datetime

def analyze_transaction_timing(address):
    """Analyze when transactions occurred"""
    info = get_address_info(address)
    
    timestamps = []
    for tx in info['transactions']:
        timestamp = tx['time']
        dt = datetime.datetime.fromtimestamp(timestamp)
        timestamps.append(dt)
    
    # Look for patterns
    print("Transaction Timeline:")
    for i, dt in enumerate(timestamps):
        print(f"  TX {i+1}: {dt.strftime('%Y-%m-%d %H:%M:%S')} ({dt.strftime('%A')})")
    
    # Check for specific days/times
    days = [dt.strftime('%A') for dt in timestamps]
    print(f"\nDay distribution: {set(days)}")
    
    # Check for time patterns
    hours = [dt.hour for dt in timestamps]
    print(f"Hour distribution: {set(hours)}")

analyze_transaction_timing("13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so")
```

**What to Look For:**
- **Specific dates:** Birthdays, holidays, anniversaries
- **Days of week:** Pattern like "every Tuesday"
- **Times:** Specific hours (e.g., always at midnight)
- **Intervals:** Regular spacing between transactions

---

### **Method 3: OP_RETURN Data Extraction**

**OP_RETURN:** Special Bitcoin script opcode that allows storing arbitrary data (up to 80 bytes) in a transaction.

**Extraction:**
```python
def extract_op_return(tx_hash):
    """Extract OP_RETURN data from transaction"""
    url = f"https://blockchain.info/rawtx/{tx_hash}"
    response = requests.get(url)
    tx = response.json()
    
    op_returns = []
    for output in tx['out']:
        script = output.get('script', '')
        if script.startswith('6a'):  # OP_RETURN opcode
            # Extract hex data after OP_RETURN
            data_hex = script[2:]
            try:
                data_ascii = bytes.fromhex(data_hex).decode('ascii', errors='ignore')
                op_returns.append({
                    'hex': data_hex,
                    'ascii': data_ascii
                })
            except:
                op_returns.append({'hex': data_hex, 'ascii': '[binary data]'})
    
    return op_returns

# Example
tx_hash = "YOUR_TX_HASH_HERE"
op_data = extract_op_return(tx_hash)
for data in op_data:
    print(f"HEX: {data['hex']}")
    print(f"ASCII: {data['ascii']}")
```

**Common OP_RETURN Uses in Puzzles:**
- **Hints:** ASCII text clues
- **URLs:** Links to additional information
- **Hashes:** SHA256 of the solution
- **Timestamps:** Proof of when puzzle was created

---

### **Method 4: Input/Output Analysis**

**UTXO Tracking:**
```python
def analyze_utxos(address):
    """Analyze Unspent Transaction Outputs"""
    url = f"https://blockchain.info/unspent?active={address}"
    response = requests.get(url)
    data = response.json()
    
    utxos = data.get('unspent_outputs', [])
    
    print(f"Total UTXOs: {len(utxos)}")
    print("\nUTXO Details:")
    for i, utxo in enumerate(utxos):
        print(f"  UTXO #{i+1}:")
        print(f"    Value: {utxo['value'] / 100000000} BTC")
        print(f"    Confirmations: {utxo['confirmations']}")
        print(f"    TX Hash: {utxo['tx_hash_big_endian']}")
        print(f"    Output Index: {utxo['tx_output_n']}")

analyze_utxos("13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so")
```

**Why This Matters:**
- Multiple UTXOs might represent different sub-puzzles
- UTXO amounts could be clues (e.g., 0.12345678 BTC = hint)
- Transaction structure reveals creator's intent

---

### **Method 5: Address Clustering**

**Identifying Related Addresses:**
```python
def find_related_addresses(address, depth=2):
    """Find addresses that transacted with the target address"""
    related = set()
    
    info = get_address_info(address)
    for tx in info['transactions']:
        # Check inputs
        for inp in tx.get('inputs', []):
            prev_out = inp.get('prev_out', {})
            addr = prev_out.get('addr')
            if addr and addr != address:
                related.add(addr)
        
        # Check outputs
        for out in tx.get('out', []):
            addr = out.get('addr')
            if addr and addr != address:
                related.add(addr)
    
    return list(related)

related = find_related_addresses("13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so")
print(f"Found {len(related)} related addresses")
for addr in related[:10]:
    print(f"  {addr}")
```

**Use Case:**
- Puzzle creator's other addresses might have clues
- Pattern across multiple puzzles
- Hidden connections

---

## 🕵️ **ADVANCED FORENSICS**

### **Technique 1: Dust Attack Detection**

**Dust Attacks:** Tiny amounts sent to many addresses to track connections

```python
def detect_dust_attacks(address):
    """Identify suspicious small transactions"""
    info = get_address_info(address)
    dust_threshold = 0.00001  # 1000 satoshis
    
    dust_txs = []
    for tx in info['transactions']:
        for out in tx['out']:
            if out.get('addr') == address:
                value_btc = out['value'] / 100000000
                if value_btc < dust_threshold:
                    dust_txs.append({
                        'tx_hash': tx['hash'],
                        'value': value_btc,
                        'time': tx['time']
                    })
    
    return dust_txs

dust = detect_dust_attacks("YOUR_ADDRESS")
if dust:
    print(f"Detected {len(dust)} potential dust attacks")
```

---

### **Technique 2: CoinJoin Detection**

**CoinJoin:** Privacy technique mixing multiple transactions

```python
def detect_coinjoin(tx_hash):
    """Detect if transaction is a CoinJoin"""
    url = f"https://blockchain.info/rawtx/{tx_hash}"
    response = requests.get(url)
    tx = response.json()
    
    inputs = len(tx['inputs'])
    outputs = len(tx['out'])
    
    # Heuristics for CoinJoin:
    # 1. Many inputs and outputs
    # 2. Multiple outputs with same value
    # 3. No obvious change output
    
    output_values = [out['value'] for out in tx['out']]
    unique_values = set(output_values)
    
    is_coinjoin = (
        inputs > 5 and
        outputs > 5 and
        len(unique_values) < outputs / 2
    )
    
    return is_coinjoin, {
        'inputs': inputs,
        'outputs': outputs,
        'unique_output_values': len(unique_values)
    }

is_cj, details = detect_coinjoin("TX_HASH")
print(f"CoinJoin: {is_cj}")
print(f"Details: {details}")
```

---

### **Technique 3: Taint Analysis**

**Track Fund Flow:**
```python
def track_taint(source_address, target_address, max_hops=3):
    """
    Track if funds from source ever reached target
    Simplified version - production would use graph database
    """
    visited = set()
    queue = [(source_address, 0)]
    path = []
    
    while queue:
        addr, hops = queue.pop(0)
        if addr in visited or hops > max_hops:
            continue
        
        visited.add(addr)
        path.append(addr)
        
        if addr == target_address:
            return True, path
        
        # Get related addresses
        related = find_related_addresses(addr, depth=1)
        for next_addr in related:
            queue.append((next_addr, hops + 1))
    
    return False, []

connected, path = track_taint("SOURCE_ADDR", "TARGET_ADDR")
if connected:
    print(f"Connection found: {' -> '.join(path)}")
```

---

## 📊 **BLOCKCHAIN ANALYTICS APIs**

### **1. Blockchain.info API**

**Endpoints:**
```python
# Single address
https://blockchain.info/address/ADDRESS?format=json

# Multiple addresses
https://blockchain.info/multiaddr?active=ADDR1|ADDR2

# Raw transaction
https://blockchain.info/rawtx/TX_HASH

# Unspent outputs
https://blockchain.info/unspent?active=ADDRESS

# Latest block
https://blockchain.info/latestblock
```

### **2. Blockchair API**

**More Powerful:**
```python
import requests

def blockchair_query(address):
    """Use Blockchair's powerful API"""
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
    response = requests.get(url)
    data = response.json()
    
    return data['data'][address]

result = blockchair_query("ADDRESS")
print(result['address'])
print(f"Balance: {result['address']['balance'] / 100000000} BTC")
print(f"Transactions: {result['address']['transaction_count']}")
```

### **3. Mempool.space API**

**Real-Time Data:**
```python
def mempool_address_info(address):
    """Get address info from Mempool.space"""
    url = f"https://mempool.space/api/address/{address}"
    response = requests.get(url)
    return response.json()

info = mempool_address_info("ADDRESS")
print(f"Chain stats: {info['chain_stats']}")
print(f"Mempool stats: {info['mempool_stats']}")
```

---

## 🛠️ **FORENSICS TOOLS**

### **1. Bitcoin Core (Full Node)**

**Run Your Own Node:**
```bash
# Install Bitcoin Core
# Download from: https://bitcoin.org/en/download

# Start with txindex (transaction indexing)
bitcoind -txindex=1 -server

# Query specific transaction
bitcoin-cli getrawtransaction TX_HASH true

# Query address (using external tools)
bitcoin-cli listunspent 0 9999999 '["ADDRESS"]'
```

**Benefits:**
- No API rate limits
- Complete blockchain data
- Privacy (no third-party queries)

---

### **2. BlockSci (Academic Tool)**

**Installation:**
```bash
# Ubuntu/Debian
sudo apt install libssl-dev libjsoncpp-dev libcurl4-openssl-dev
git clone https://github.com/citp/BlockSci
cd BlockSci
mkdir build && cd build
cmake ..
make
sudo make install
```

**Usage:**
```python
import blocksci

chain = blocksci.Blockchain("/path/to/blockchain/data")

# Analyze address
address = chain.address_from_string("ADDRESS")
print(f"Balance: {address.balance()}")
print(f"Transactions: {len(address.txes())}")

# Advanced queries
for tx in address.txes():
    print(f"TX: {tx.hash}, Fee: {tx.fee}")
```

---

### **3. GraphSense (Visualization)**

**Web-Based Blockchain Explorer:**
- **URL:** https://graphsense.info/
- **Features:**
  - Graph visualization of transactions
  - Address clustering
  - Tag system for known entities
  - Export data for analysis

---

## 🎯 **PUZZLE-SPECIFIC ANALYSIS**

### **For 0.2 BTC Puzzle:**

```python
def analyze_02btc_puzzle():
    """Detailed analysis of 0.2 BTC puzzle"""
    address = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
    
    # Get full info
    info = get_address_info(address)
    
    print("=== 0.2 BTC PUZZLE ANALYSIS ===\n")
    print(f"Address: {address}")
    print(f"Current Balance: {info['final_balance']} BTC")
    print(f"Total Transactions: {info['n_tx']}\n")
    
    # Analyze each transaction
    print("Transaction History:")
    for i, tx in enumerate(info['transactions']):
        dt = datetime.datetime.fromtimestamp(tx['time'])
        print(f"\nTX #{i+1}:")
        print(f"  Hash: {tx['hash']}")
        print(f"  Date: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Day: {dt.strftime('%A')}")
        
        # Check for OP_RETURN
        op_returns = extract_op_return(tx['hash'])
        if op_returns:
            print(f"  OP_RETURN Data: {op_returns}")
        
        # Check transaction structure
        print(f"  Inputs: {len(tx['inputs'])}")
        print(f"  Outputs: {len(tx['out'])}")
    
    # Look for patterns
    print("\n=== PATTERN ANALYSIS ===")
    # Add custom analysis based on clues

analyze_02btc_puzzle()
```

---

## 🔐 **PRIVACY & OPSEC**

### **When Analyzing:**

**DO:**
- ✅ Use VPN or Tor
- ✅ Run your own Bitcoin node when possible
- ✅ Cache data locally
- ✅ Be aware of rate limits

**DON'T:**
- ❌ Query from your personal IP without protection
- ❌ Reveal your methodology publicly before solving
- ❌ Use centralized services for sensitive queries
- ❌ Link your real identity to puzzle-solving activities

---

## 📚 **COMPREHENSIVE ANALYSIS SCRIPT**

```python
#!/usr/bin/env python3
"""
Comprehensive Blockchain Forensics Script
For crypto puzzle analysis
"""

import requests
import datetime
import json
from typing import Dict, List

class BlockchainForensics:
    def __init__(self, address: str):
        self.address = address
        self.data = None
    
    def fetch_data(self):
        """Fetch all address data"""
        url = f"https://blockchain.info/address/{self.address}?format=json"
        response = requests.get(url)
        self.data = response.json()
        return self.data
    
    def basic_stats(self):
        """Print basic statistics"""
        if not self.data:
            self.fetch_data()
        
        print(f"Address: {self.address}")
        print(f"Balance: {self.data['final_balance'] / 1e8} BTC")
        print(f"Total Received: {self.data['total_received'] / 1e8} BTC")
        print(f"Total Sent: {self.data['total_sent'] / 1e8} BTC")
        print(f"Transactions: {self.data['n_tx']}")
    
    def timeline_analysis(self):
        """Analyze transaction timeline"""
        if not self.data:
            self.fetch_data()
        
        print("\n=== TIMELINE ANALYSIS ===")
        for i, tx in enumerate(self.data['txs']):
            dt = datetime.datetime.fromtimestamp(tx['time'])
            print(f"TX {i+1}: {dt} ({dt.strftime('%A')})")
    
    def output_analysis(self):
        """Analyze transaction outputs"""
        if not self.data:
            self.fetch_data()
        
        print("\n=== OUTPUT ANALYSIS ===")
        for i, tx in enumerate(self.data['txs']):
            print(f"\nTX {i+1} ({tx['hash'][:16]}...):")
            for j, out in enumerate(tx['out']):
                if out.get('addr') == self.address:
                    print(f"  Output {j}: {out['value'] / 1e8} BTC")
    
    def full_report(self):
        """Generate comprehensive report"""
        self.basic_stats()
        self.timeline_analysis()
        self.output_analysis()
        
        # Save to file
        with open(f"{self.address}_report.json", 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"\nFull data saved to {self.address}_report.json")

# Usage
if __name__ == "__main__":
    forensics = BlockchainForensics("1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ")
    forensics.full_report()
```

---

## 🏆 **SUCCESS INDICATORS**

**You've found a clue when:**
1. ✅ OP_RETURN data contains hints
2. ✅ Transaction dates match known events
3. ✅ Output amounts encode numbers/coordinates
4. ✅ Related addresses form a pattern
5. ✅ Transaction structure reveals creator's method

---

**END OF BLOCKCHAIN FORENSICS GUIDE**

*SHENRON: Follow the blockchain, find the truth. 🐉⛓️*

