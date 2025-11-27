# Rust 1.75+ Complete Programming Reference (2025-2026)
## Modern Systems Programming with Memory Safety

**Rust Version**: 1.75+ (Latest stable as of 2025-2026)  
**Philosophy**: Safety, speed, concurrency  
**Motto**: "Fearless concurrency"

---

## 🚀 **WHY RUST IN 2025-2026?**

**Rust is THE language for**:
- ✅ Systems programming (OS, drivers, embedded)
- ✅ Web servers (Actix, Axum, Rocket)
- ✅ CLI tools (ripgrep, bat, fd)
- ✅ WebAssembly (WASM)
- ✅ Blockchain & crypto
- ✅ High-performance backends
- ✅ Replacing C/C++ in critical systems

**Rust's Guarantees**:
- **Memory safety** without garbage collection
- **Thread safety** at compile time
- **Zero-cost abstractions**

---

## 📦 **INSTALLATION**

### **Install Rustup** (Official Installer)

**Linux / macOS**:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add to PATH
source $HOME/.cargo/env

# Verify
rustc --version
cargo --version
```

**Windows**:
```powershell
# Download from: https://rust-lang.org/tools/install
# Run rustup-init.exe

# OR use winget
winget install Rustlang.Rustup

# Verify
rustc --version
cargo --version
```

### **Update Rust**

```bash
rustup update
```

---

## 💡 **RUST BASICS**

### **Hello World**

```rust
fn main() {
    println!("Hello, World!");
}
```

Run:
```bash
rustc main.rs
./main

# OR use Cargo (package manager)
cargo new hello_world
cd hello_world
cargo run
```

### **Variables**

```rust
fn main() {
    // Immutable by default (Rust's philosophy)
    let x = 5;
    // x = 6; // ERROR: cannot mutate immutable variable

    // Mutable variable
    let mut y = 10;
    y = 15; // OK

    // Type inference
    let name = "Seth";
    let age = 30;

    // Explicit types
    let count: i32 = 100;
    let price: f64 = 99.99;

    println!("{} is {} years old, count: {}, price: {}", name, age, count, price);
}
```

### **Ownership** (Rust's Secret Sauce)

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1's ownership MOVED to s2
    
    // println!("{}", s1); // ERROR: s1 no longer valid
    println!("{}", s2); // OK

    // To copy: use .clone()
    let s3 = s2.clone();
    println!("{} and {}", s2, s3); // Both OK
}
```

### **Borrowing** (References)

```rust
fn main() {
    let s1 = String::from("hello");
    
    // Borrow (immutable reference)
    let len = calculate_length(&s1);
    println!("Length of '{}' is {}", s1, len); // s1 still valid!
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope, but doesn't drop the String (only borrowed)
```

### **Mutable Borrowing**

```rust
fn main() {
    let mut s = String::from("hello");
    
    change(&mut s);
    
    println!("{}", s); // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

---

## 🔧 **FUNCTIONS**

```rust
// Basic function
fn add(a: i32, b: i32) -> i32 {
    a + b // No semicolon = return value
}

// Multiple return values (tuple)
fn divide(a: f64, b: f64) -> (f64, bool) {
    if b == 0.0 {
        (0.0, false) // error case
    } else {
        (a / b, true) // success case
    }
}

// Result type (idiomatic error handling)
fn divide_result(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}

fn main() {
    println!("{}", add(5, 3)); // 8

    let (result, success) = divide(10.0, 2.0);
    if success {
        println!("Result: {}", result);
    }

    match divide_result(10.0, 0.0) {
        Ok(result) => println!("Result: {}", result),
        Err(e) => println!("Error: {}", e),
    }
}
```

---

## 📦 **STRUCTS & ENUMS**

### **Structs**

```rust
struct User {
    name: String,
    age: u32,
    email: String,
}

impl User {
    // Associated function (like static method)
    fn new(name: String, age: u32, email: String) -> User {
        User { name, age, email }
    }

    // Method (takes &self)
    fn display(&self) {
        println!("{} ({}) - {}", self.name, self.age, self.email);
    }

    // Mutable method
    fn increment_age(&mut self) {
        self.age += 1;
    }
}

fn main() {
    let mut user = User::new(
        String::from("Seth"),
        30,
        String::from("seth@example.com")
    );

    user.display(); // Seth (30) - seth@example.com
    user.increment_age();
    user.display(); // Seth (31) - seth@example.com
}
```

### **Enums**

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}

enum Option<T> {
    Some(T),
    None,
}

// Custom enum
enum TrafficLight {
    Red,
    Yellow,
    Green,
}

impl TrafficLight {
    fn action(&self) -> &str {
        match self {
            TrafficLight::Red => "Stop",
            TrafficLight::Yellow => "Caution",
            TrafficLight::Green => "Go",
        }
    }
}

fn main() {
    let light = TrafficLight::Red;
    println!("{}", light.action()); // Stop
}
```

---

## 🧵 **CONCURRENCY (Fearless!)**

### **Threads**

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("Thread: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("Main: {}", i);
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap(); // Wait for thread to finish
}
```

### **Channels** (Message Passing)

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("Hello from thread");
        tx.send(val).unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Got: {}", received);
}
```

### **Shared State** (Arc + Mutex)

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap()); // 10
}
```

---

## 🌐 **WEB SERVER WITH ACTIX-WEB**

### **Create Project**

```bash
cargo new my-web-app
cd my-web-app

# Add dependencies to Cargo.toml
# [dependencies]
# actix-web = "4.5"
# tokio = { version = "1", features = ["full"] }
```

### **Simple HTTP Server**

```rust
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct User {
    name: String,
    age: u32,
}

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hello, Actix!")
}

#[get("/users/{id}")]
async fn get_user(path: web::Path<u32>) -> impl Responder {
    let id = path.into_inner();
    HttpResponse::Ok().body(format!("User ID: {}", id))
}

#[post("/users")]
async fn create_user(user: web::Json<User>) -> impl Responder {
    HttpResponse::Created().json(user.into_inner())
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Server running on http://127.0.0.1:8080");

    HttpServer::new(|| {
        App::new()
            .service(hello)
            .service(get_user)
            .service(create_user)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
```

Run:
```bash
cargo run
```

---

## 📚 **POPULAR CRATES (2025-2026)**

### **Web Frameworks**
- **actix-web**: Fast, pragmatic (most popular)
- **axum**: Ergonomic, tokio-based
- **rocket**: Easy, type-safe
- **warp**: Composable filters

### **Async Runtime**
- **tokio**: Most popular (1M+ downloads/day)
- **async-std**: Alternative to tokio

### **CLI Tools**
- **clap**: Command-line argument parsing
- **indicatif**: Progress bars
- **colored**: Colored terminal output

### **Serialization**
- **serde**: Serialize/deserialize (JSON, YAML, etc.)
- **serde_json**: JSON support

### **HTTP Client**
- **reqwest**: Easy HTTP client
- **hyper**: Low-level HTTP library

---

## 🧪 **TESTING**

### **Unit Tests**

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -2), -3);
    }

    #[test]
    #[should_panic]
    fn test_panic() {
        panic!("This test should panic");
    }
}
```

Run tests:
```bash
cargo test
cargo test --verbose
cargo test test_add  # Run specific test
```

---

## 🎯 **BEST PRACTICES (2025-2026)**

### **1. Use `Result` for Error Handling**

```rust
use std::fs::File;
use std::io::{self, Read};

// ✅ GOOD: Return Result
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// ❌ BAD: Use unwrap() everywhere
fn read_file_bad(path: &str) -> String {
    let mut file = File::open(path).unwrap(); // CRASH if fails!
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}
```

### **2. Avoid `.clone()` Unless Necessary**

```rust
// ✅ GOOD: Use references
fn print_length(s: &String) {
    println!("Length: {}", s.len());
}

// ❌ BAD: Unnecessary clone
fn print_length_bad(s: String) { // Takes ownership!
    println!("Length: {}", s.len());
}
```

### **3. Use `match` for Exhaustive Handling**

```rust
enum Status {
    Success,
    Error,
    Pending,
}

// ✅ GOOD: Handle all cases
fn handle_status(status: Status) {
    match status {
        Status::Success => println!("Success!"),
        Status::Error => println!("Error!"),
        Status::Pending => println!("Pending..."),
    }
}
```

### **4. Use `derive` for Common Traits**

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = p1.clone();
    println!("{:?}", p1); // Debug print
    println!("Equal: {}", p1 == p2);
}
```

---

## 📖 **LEARNING RESOURCES**

- **The Rust Book**: https://doc.rust-lang.org/book/
- **Rust by Example**: https://doc.rust-lang.org/rust-by-example/
- **Rustlings** (exercises): https://github.com/rust-lang/rustlings
- **Crates.io**: https://crates.io/ (package registry)
- **Docs.rs**: https://docs.rs/ (documentation)
- **Rust Users Forum**: https://users.rust-lang.org/

---

## 🚀 **CARGO COMMANDS**

```bash
# Create new project
cargo new my-project
cargo new --lib my-library

# Build
cargo build
cargo build --release  # Optimized

# Run
cargo run
cargo run --release

# Test
cargo test
cargo test --verbose

# Check (faster than build)
cargo check

# Format code
cargo fmt

# Lint
cargo clippy

# Documentation
cargo doc --open

# Update dependencies
cargo update

# Add dependency
cargo add actix-web
```

---

**Document Created**: November 6, 2025  
**Purpose**: Rust 1.75+ programming reference for SHENRON AI knowledge base  
**Usage**: Help users write modern Rust code with memory safety and concurrency

**✨ Rust knowledge complete! ✨** 🦀

