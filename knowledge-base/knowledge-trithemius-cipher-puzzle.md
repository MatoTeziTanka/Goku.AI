# Trithemius Cipher Puzzle - Complete Analysis

**Source:** https://github.com/MatoTeziTanka/CryptoPuzzles/tree/main/Trithemius  
**Puzzle Type:** Classical Cryptography  
**Difficulty:** Medium  
**Status:** Check repository for current status

---

## 🔐 **TRITHEMIUS CIPHER BACKGROUND**

### **What is Trithemius Cipher?**

The Trithemius cipher, also known as **Tabula Recta** or **Trithemius Tableau**, is a polyalphabetic substitution cipher invented by Johannes Trithemius in the 15th century.

### **How It Works:**

**Basic Principle:**
- Each letter in the plaintext is shifted by its position in the text
- First letter: shift by 0 (or 1)
- Second letter: shift by 1 (or 2)
- Third letter: shift by 2 (or 3)
- And so on...

**Example:**
```
Plaintext:  HELLO
Positions:  0 1 2 3 4

H + 0 = H
E + 1 = F
L + 2 = N
L + 3 = O
O + 4 = S

Ciphertext: HFNOS
```

### **Variations:**

1. **Standard Trithemius**: Shift = position (0-indexed)
2. **Modified Trithemius**: Shift = position + 1 (1-indexed)
3. **Reverse Trithemius**: Shift = -position (decrementing)
4. **Keyed Trithemius**: Shift based on keyword values

---

## 🧮 **DECRYPTION ALGORITHM**

### **Python Implementation:**

```python
def trithemius_decrypt(ciphertext, reverse=False, offset=0):
    """
    Decrypt Trithemius cipher
    
    Args:
        ciphertext (str): Encrypted text
        reverse (bool): Use reverse shifting
        offset (int): Starting offset (0 or 1)
    
    Returns:
        str: Decrypted plaintext
    """
    plaintext = []
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Calculate shift based on position
            shift = (i + offset) if not reverse else -(i + offset)
            
            # Determine if uppercase or lowercase
            if char.isupper():
                # Decrypt: (C - shift) mod 26
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            plaintext.append(decrypted)
        else:
            # Keep non-alphabetic characters unchanged
            plaintext.append(char)
    
    return ''.join(plaintext)


def trithemius_encrypt(plaintext, reverse=False, offset=0):
    """Encrypt using Trithemius cipher"""
    ciphertext = []
    
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = (i + offset) if not reverse else -(i + offset)
            
            if char.isupper():
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            
            ciphertext.append(encrypted)
        else:
            ciphertext.append(char)
    
    return ''.join(ciphertext)


# Test all variations
def solve_trithemius(ciphertext):
    """Try all common Trithemius variations"""
    print("Testing Trithemius variations:\n")
    
    variations = [
        ("Standard (offset=0)", False, 0),
        ("Modified (offset=1)", False, 1),
        ("Reverse (offset=0)", True, 0),
        ("Reverse (offset=1)", True, 1),
    ]
    
    for name, reverse, offset in variations:
        result = trithemius_decrypt(ciphertext, reverse, offset)
        print(f"{name}:")
        print(f"  {result}\n")
    
    return results


# Example usage:
ciphertext = "YOUR_CIPHERTEXT_HERE"
solve_trithemius(ciphertext)
```

---

## 🔍 **ANALYSIS TECHNIQUES**

### **1. Frequency Analysis**
Even though Trithemius is polyalphabetic, patterns emerge:
- First letters have minimal shift
- End of text has maximum shift
- Analyze letter frequency at different positions

### **2. Known Plaintext Attack**
If you suspect certain words (e.g., "THE", "AND", "BITCOIN"):
```python
def test_known_plaintext(ciphertext, known_word, position):
    """Test if known word appears at position"""
    for offset in [0, 1]:
        for reverse in [False, True]:
            encrypted = trithemius_encrypt(known_word, reverse, position + offset)
            if ciphertext[position:position+len(known_word)] == encrypted:
                print(f"MATCH: offset={offset}, reverse={reverse}")
                return (offset, reverse)
    return None
```

### **3. English Detection**
After decryption, validate if output is English:
```python
def is_english(text):
    """Check if text is likely English"""
    common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'with']
    text_lower = text.lower()
    matches = sum(1 for word in common_words if word in text_lower)
    return matches >= 3
```

---

## 🎯 **SOLVING STRATEGY**

### **Step 1: Identify Cipher Type**
- Check GitHub repo for hints
- Look for keywords: "Trithemius", "Tabula Recta", "progressive shift"

### **Step 2: Extract Ciphertext**
- May be in a file, image, or README
- Note any special formatting or spacing

### **Step 3: Try All Variations**
```python
for offset in [0, 1, -1]:
    for reverse in [False, True]:
        result = trithemius_decrypt(ciphertext, reverse, offset)
        if is_english(result):
            print(f"POSSIBLE SOLUTION (offset={offset}, reverse={reverse}):")
            print(result)
```

### **Step 4: Analyze Context**
- Check repo commits for clues
- Read any accompanying documentation
- Look for Bitcoin addresses or private keys in output

### **Step 5: Validate Solution**
- If output contains Bitcoin address: Check balance on blockchain
- If output contains private key: CAREFULLY test (could contain funds)
- Ensure solution makes sense contextually

---

## 🔧 **ADVANCED TECHNIQUES**

### **Keyed Trithemius**
If puzzle uses a keyword:
```python
def keyed_trithemius_decrypt(ciphertext, keyword):
    """Decrypt with keyword-based shifts"""
    plaintext = []
    keyword_repeated = (keyword * (len(ciphertext) // len(keyword) + 1))[:len(ciphertext)]
    
    for i, (cipher_char, key_char) in enumerate(zip(ciphertext, keyword_repeated)):
        if cipher_char.isalpha() and key_char.isalpha():
            shift = ord(key_char.upper()) - ord('A') + i
            if cipher_char.isupper():
                decrypted = chr((ord(cipher_char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(cipher_char) - ord('a') - shift) % 26 + ord('a'))
            plaintext.append(decrypted)
        else:
            plaintext.append(cipher_char)
    
    return ''.join(plaintext)
```

### **Automated Keyword Search**
```python
common_keywords = ['bitcoin', 'satoshi', 'crypto', 'puzzle', 'cipher', 'key']

for keyword in common_keywords:
    result = keyed_trithemius_decrypt(ciphertext, keyword)
    if is_english(result):
        print(f"Keyword: {keyword}")
        print(result)
```

---

## 📚 **HISTORICAL CONTEXT**

### **Johannes Trithemius (1462-1516)**
- German abbot and polymath
- Pioneer in cryptography and steganography
- Author of "Steganographia" and "Polygraphiae"
- Invented Tabula Recta (used later in Vigenère cipher)

### **Modern Usage**
- Educational tool for learning cryptography
- CTF (Capture The Flag) competitions
- Puzzle hunts and treasure hunts
- Historical encryption demonstrations

---

## 🎲 **COMMON PUZZLE PATTERNS**

### **Bitcoin Puzzles Using Trithemius:**
1. **Private Key Encryption**:
   - Encrypt WIF (Wallet Import Format) key
   - Solver decrypts to get private key
   - Import to wallet to claim funds

2. **Seed Phrase Encryption**:
   - Encrypt BIP39 seed words
   - Decrypt to get valid seed phrase
   - Restore wallet to claim prize

3. **Multi-Stage**:
   - Trithemius reveals next clue
   - Chain of ciphers
   - Final stage reveals Bitcoin address or key

---

## 🚀 **SHENRON AUTO-SOLVE SCRIPT**

```python
import re
from mnemonic import Mnemonic
from bitcoin import *

def auto_solve_trithemius_puzzle(repo_path):
    """
    Autonomous solver for Trithemius puzzles
    
    1. Scan repo for ciphertext
    2. Try all Trithemius variations
    3. Validate outputs
    4. Check for Bitcoin keys/addresses
    """
    
    # Step 1: Find potential ciphertext
    ciphertexts = scan_repo_for_ciphertext(repo_path)
    
    # Step 2: Try decryption
    for ciphertext in ciphertexts:
        print(f"\nTrying ciphertext: {ciphertext[:50]}...")
        
        # Try all variations
        for offset in [0, 1, -1]:
            for reverse in [False, True]:
                plaintext = trithemius_decrypt(ciphertext, reverse, offset)
                
                # Check if English
                if is_english(plaintext):
                    print(f"\n[POSSIBLE] offset={offset}, reverse={reverse}")
                    print(plaintext)
                    
                    # Check for Bitcoin data
                    check_for_bitcoin_data(plaintext)


def scan_repo_for_ciphertext(repo_path):
    """Scan GitHub repo for potential ciphertext"""
    import os
    
    ciphertexts = []
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.txt', '.md', '.cipher')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for encoded text (mostly uppercase, no spaces)
                    matches = re.findall(r'[A-Z]{20,}', content)
                    ciphertexts.extend(matches)
    
    return ciphertexts


def check_for_bitcoin_data(text):
    """Check if text contains Bitcoin keys/addresses"""
    
    # Check for Bitcoin address (starts with 1, 3, or bc1)
    addresses = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', text)
    if addresses:
        print(f"\n[BITCOIN ADDRESS FOUND]: {addresses}")
    
    # Check for WIF private key (starts with 5, K, or L)
    wif_keys = re.findall(r'\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b', text)
    if wif_keys:
        print(f"\n[PRIVATE KEY FOUND]: {wif_keys[0][:10]}... (truncated)")
        print("[WARNING] Handle with care - may contain funds!")
    
    # Check for seed phrase words
    mnemo = Mnemonic("english")
    words = text.lower().split()
    seed_words = [w for w in words if w in mnemo.wordlist]
    if len(seed_words) >= 12:
        print(f"\n[POTENTIAL SEED WORDS]: {len(seed_words)} BIP39 words found")
        print(f"  {seed_words[:12]}")


# Run the solver
auto_solve_trithemius_puzzle("/path/to/MatoTeziTanka/CryptoPuzzles/Trithemius")
```

---

## 🎯 **QUEST CONFIGURATION FOR SHENRON**

```python
quest_id = manager.create_quest(
    goal="""
    Solve the Trithemius cipher puzzle from 
    https://github.com/MatoTeziTanka/CryptoPuzzles/tree/main/Trithemius
    
    Approach:
    1. Clone/download repository
    2. Scan for ciphertext in files
    3. Apply Trithemius decryption (all variations)
    4. Validate English output
    5. Search for Bitcoin addresses/keys
    6. Test any found keys (CAREFULLY)
    """,
    strategy="systematic",
    priority=8,
    max_attempts=100,
    metadata={
        "puzzle_type": "trithemius_cipher",
        "repo": "MatoTeziTanka/CryptoPuzzles/Trithemius",
        "cipher_variations": ["standard", "modified", "reverse", "keyed"]
    }
)
```

---

## 📊 **SUCCESS INDICATORS**

### **You've Solved It When:**
1. ✅ Decrypted text is readable English
2. ✅ Output contains Bitcoin address or private key
3. ✅ Address has balance (check blockchain explorer)
4. ✅ Private key imports successfully to wallet
5. ✅ Puzzle creator confirms solution (if applicable)

### **Common Pitfalls:**
- ❌ Assuming offset is 0 (try 1 and -1 too)
- ❌ Not testing reverse mode
- ❌ Ignoring case sensitivity
- ❌ Not checking for keyword-based variations
- ❌ Missing ciphertext hidden in images/comments

---

## 🔗 **RELATED CIPHERS**

If Trithemius doesn't work, try:
- **Vigenère**: Uses keyword (evolved from Trithemius)
- **Caesar**: Simple shift (subset of Trithemius)
- **Autokey**: Self-keying variant
- **Beaufort**: Similar to Vigenère but different operation

---

**END OF TRITHEMIUS CIPHER KNOWLEDGE**

*SHENRON: Master the classics to unlock the future. 🔐*

