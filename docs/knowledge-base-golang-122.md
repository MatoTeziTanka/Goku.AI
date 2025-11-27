# Go 1.22+ Complete Programming Reference (2025-2026)
## Modern Go Development with Latest Features

**Go Version**: 1.22+ (Latest stable as of 2025-2026)  
**Release Date**: Go 1.22 released February 2024, Go 1.23 in August 2024  
**Philosophy**: Simple, fast, reliable software

---

## 🚀 **WHAT'S NEW IN GO 1.22+**

### **Go 1.22 Features**

1. **Enhanced `for` Loop Semantics**
   - Loop variables per iteration (fixes common gotcha)
   - Safer goroutines in loops

2. **Range over Integers**
   - `for i := range 10` - iterate 0 to 9
   - Cleaner loop syntax

3. **HTTP Routing Enhancements**
   - Method and path patterns in `http.ServeMux`
   - Better REST API routing

4. **Memory Optimizations**
   - Reduced memory overhead
   - Faster garbage collection

### **Go 1.23 Features** (August 2024)

1. **Iterators** (New!)
   - First-class support for custom iterators
   - `iter.Seq[T]` and `iter.Seq2[K, V]` types

2. **Timer Optimizations**
   - More efficient `time.Timer` and `time.Ticker`

3. **slices and maps Improvements**
   - New functions in `slices` and `maps` packages

---

## 📦 **INSTALLATION & SETUP**

### **Install Go**

**Linux**:
```bash
# Download latest Go
wget https://go.dev/dl/go1.23.0.linux-amd64.tar.gz

# Remove old version
sudo rm -rf /usr/local/go

# Extract
sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz

# Add to PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify
go version
# Output: go version go1.23.0 linux/amd64
```

**macOS**:
```bash
# Using Homebrew
brew install go

# Verify
go version
```

**Windows**:
```powershell
# Using winget
winget install GoLang.Go

# OR download from https://go.dev/dl/
# Run installer

# Verify
go version
```

---

## 💡 **GO BASICS (2025 STYLE)**

### **Hello World**

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

Run:
```bash
go run main.go
# Or compile:
go build main.go
./main
```

### **Variables**

```go
package main

import "fmt"

func main() {
    // Type inference
    name := "Seth"
    age := 30
    price := 99.99
    
    // Explicit types
    var count int = 10
    var isActive bool = true
    
    // Multiple variables
    x, y := 10, 20
    
    fmt.Println(name, age, price, count, isActive, x, y)
}
```

### **Functions**

```go
// Basic function
func add(a int, b int) int {
    return a + b
}

// Shortened parameter types
func multiply(a, b int) int {
    return a * b
}

// Multiple return values (very common in Go)
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func getCoordinates() (x, y int) {
    x = 10
    y = 20
    return // returns x and y
}

// Variadic function
func sum(numbers ...int) int {
    total := 0
    for _, num := range numbers {
        total += num
    }
    return total
}

func main() {
    fmt.Println(add(5, 3))                    // 8
    fmt.Println(multiply(4, 5))               // 20
    result, err := divide(10, 2)              // 5.0, nil
    x, y := getCoordinates()                  // 10, 20
    fmt.Println(sum(1, 2, 3, 4, 5))          // 15
}
```

---

## 🔄 **NEW: RANGE OVER INTEGERS (Go 1.22)**

```go
package main

import "fmt"

func main() {
    // Old way
    for i := 0; i < 10; i++ {
        fmt.Println(i)
    }

    // NEW in Go 1.22: Range over integers
    for i := range 10 {
        fmt.Println(i) // 0, 1, 2, ..., 9
    }

    // Works great for creating goroutines
    for i := range 5 {
        go func() {
            fmt.Printf("Goroutine %d\n", i)
        }()
    }
}
```

---

## 🧵 **GOROUTINES & CONCURRENCY**

### **Basic Goroutine**

```go
package main

import (
    "fmt"
    "time"
)

func sayHello() {
    fmt.Println("Hello from goroutine!")
}

func main() {
    // Start goroutine
    go sayHello()
    
    // Wait for goroutine to finish
    time.Sleep(100 * time.Millisecond)
    
    fmt.Println("Main function")
}
```

### **Channels**

```go
package main

import "fmt"

func sum(numbers []int, result chan int) {
    total := 0
    for _, num := range numbers {
        total += num
    }
    result <- total // Send result to channel
}

func main() {
    numbers := []int{1, 2, 3, 4, 5}
    
    result := make(chan int)
    
    // Split work across 2 goroutines
    go sum(numbers[:len(numbers)/2], result)
    go sum(numbers[len(numbers)/2:], result)
    
    // Receive results
    part1 := <-result
    part2 := <-result
    
    fmt.Println("Total:", part1 + part2) // 15
}
```

### **Select Statement** (Multiplexing Channels)

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)
    
    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "Message from ch1"
    }()
    
    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "Message from ch2"
    }()
    
    // Wait for either channel
    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-ch1:
            fmt.Println(msg1)
        case msg2 := <-ch2:
            fmt.Println(msg2)
        }
    }
}
```

---

## 🌐 **HTTP SERVER (Go 1.22 Enhanced Routing)**

### **Basic HTTP Server**

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    // NEW in Go 1.22: Method-specific routing
    http.HandleFunc("GET /hello", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello, World!")
    })

    http.HandleFunc("POST /data", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Data received!")
    })

    // Path patterns with variables
    http.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
        id := r.PathValue("id")
        fmt.Fprintf(w, "User ID: %s", id)
    })

    fmt.Println("Server running on http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}
```

### **RESTful API Example**

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

var users = []User{
    {ID: 1, Name: "Alice", Email: "alice@example.com"},
    {ID: 2, Name: "Bob", Email: "bob@example.com"},
}

func main() {
    // GET all users
    http.HandleFunc("GET /api/users", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(users)
    })

    // GET user by ID
    http.HandleFunc("GET /api/users/{id}", func(w http.ResponseWriter, r *http.Request) {
        id := r.PathValue("id")
        w.Header().Set("Content-Type", "application/json")
        
        for _, user := range users {
            if fmt.Sprint(user.ID) == id {
                json.NewEncoder(w).Encode(user)
                return
            }
        }
        
        http.NotFound(w, r)
    })

    // POST create user
    http.HandleFunc("POST /api/users", func(w http.ResponseWriter, r *http.Request) {
        var newUser User
        if err := json.NewDecoder(r.Body).Decode(&newUser); err != nil {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }
        
        newUser.ID = len(users) + 1
        users = append(users, newUser)
        
        w.Header().Set("Content-Type", "application/json")
        w.WriteStatus(http.StatusCreated)
        json.NewEncoder(w).Encode(newUser)
    })

    fmt.Println("API server on http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}
```

---

## 🛠️ **GO MODULES & PROJECT STRUCTURE**

### **Initialize Go Module**

```bash
# Create new project
mkdir my-go-app
cd my-go-app

# Initialize module
go mod init github.com/username/my-go-app

# Creates go.mod file
```

### **Project Structure**

```
my-go-app/
├── go.mod              # Module definition
├── go.sum              # Checksums for dependencies
├── main.go             # Entry point
├── api/
│   └── handlers.go     # HTTP handlers
├── models/
│   └── user.go         # Data models
├── database/
│   └── db.go           # Database logic
└── utils/
    └── helpers.go      # Utility functions
```

### **Adding Dependencies**

```bash
# Add dependency
go get github.com/gorilla/mux

# Update dependencies
go mod tidy

# Vendor dependencies (optional)
go mod vendor
```

---

## 📚 **POPULAR LIBRARIES (2025-2026)**

### **Web Frameworks**

**Gin** (Fast, minimalist):
```go
import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    
    r.Run() // localhost:8080
}
```

**Echo** (High performance):
```go
import "github.com/labstack/echo/v4"

func main() {
    e := echo.New()
    
    e.GET("/", func(c echo.Context) error {
        return c.String(200, "Hello, Echo!")
    })
    
    e.Start(":8080")
}
```

**Fiber** (Express-like):
```go
import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New()
    
    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, Fiber!")
    })
    
    app.Listen(":8080")
}
```

---

## 🧪 **TESTING**

### **Basic Test**

```go
// math.go
package math

func Add(a, b int) int {
    return a + b
}

// math_test.go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5
    
    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}

func TestAddNegative(t *testing.T) {
    result := Add(-1, -2)
    expected := -3
    
    if result != expected {
        t.Errorf("Add(-1, -2) = %d; want %d", result, expected)
    }
}
```

Run tests:
```bash
go test
go test -v  # Verbose
go test -cover  # Coverage
```

---

## 🎯 **BEST PRACTICES (2025-2026)**

### **1. Error Handling**

```go
// ✅ GOOD: Check errors explicitly
file, err := os.Open("file.txt")
if err != nil {
    return fmt.Errorf("failed to open file: %w", err)
}
defer file.Close()

// ❌ BAD: Ignoring errors
file, _ := os.Open("file.txt")
```

### **2. Use `defer` for Cleanup**

```go
// ✅ GOOD: defer ensures cleanup
func readFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close() // Always closes, even if panic
    
    // Read file...
    return nil
}
```

### **3. Context for Cancellation**

```go
import (
    "context"
    "time"
)

func fetchData(ctx context.Context) error {
    // Simulate long operation
    select {
    case <-time.After(5 * time.Second):
        return nil
    case <-ctx.Done():
        return ctx.Err() // Cancelled or timed out
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    if err := fetchData(ctx); err != nil {
        fmt.Println("Error:", err) // "context deadline exceeded"
    }
}
```

### **4. Use `sync.WaitGroup` for Goroutine Coordination**

```go
import (
    "fmt"
    "sync"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Printf("Worker %d done\n", id)
}

func main() {
    var wg sync.WaitGroup
    
    for i := range 5 {
        wg.Add(1)
        go worker(i, &wg)
    }
    
    wg.Wait() // Wait for all goroutines
    fmt.Println("All workers done")
}
```

---

## 📖 **LEARNING RESOURCES**

- **Official Go Tour**: https://go.dev/tour/
- **Effective Go**: https://go.dev/doc/effective_go
- **Go by Example**: https://gobyexample.com/
- **Go Standard Library**: https://pkg.go.dev/std
- **Awesome Go**: https://github.com/avelino/awesome-go (curated packages)

---

**Document Created**: November 6, 2025  
**Purpose**: Go 1.22+ programming reference for SHENRON AI knowledge base  
**Usage**: Help users write modern Go code with 2025-2026 best practices

**✨ Go knowledge complete! ✨** 🐹

