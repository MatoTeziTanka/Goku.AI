# Java 21 Complete Programming Reference (2025-2026)
## Modern Java Development with LTS Features

**Java Version**: 21 (LTS - Long Term Support)  
**Release Date**: September 2023  
**Support Until**: September 2031 (8 years)  
**Current Status**: Latest LTS (as of 2025-2026)

---

## 🚀 **WHAT'S NEW IN JAVA 21**

### **Major Features**

1. **Virtual Threads** (Project Loom) - **GAME CHANGER**
   - Lightweight threads (1 million+ threads possible)
   - Simplifies concurrent programming
   - Perfect for I/O-heavy applications

2. **Pattern Matching for `switch`** (Final)
   - More expressive switch statements
   - Pattern matching in case labels
   - `when` guards for additional conditions

3. **Record Patterns** (Final)
   - Deconstruct records in pattern matching
   - Cleaner, more readable code

4. **Sequenced Collections**
   - New interfaces: `SequencedCollection`, `SequencedSet`, `SequencedMap`
   - Consistent API for ordered collections

5. **String Templates** (Preview)
   - Embedded expressions in strings
   - Type-safe string interpolation

6. **Unnamed Patterns and Variables**
   - Use `_` for unused variables
   - Cleaner code, better intent

---

## 📦 **INSTALLATION & SETUP**

### **Download & Install**

**Official Oracle JDK**:
```bash
# Download from: https://www.oracle.com/java/technologies/downloads/#java21
# Or use package manager:

# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-21-jdk -y

# macOS (Homebrew)
brew install openjdk@21

# Windows (winget)
winget install Oracle.JDK.21
```

**OpenJDK (Free, recommended)**:
```bash
# Ubuntu/Debian
sudo apt install openjdk-21-jdk -y

# macOS
brew install openjdk@21

# Windows (manually download from adoptium.net)
```

**Verify Installation**:
```bash
java --version
# Output: openjdk 21.0.x 2023-09-19 LTS

javac --version
# Output: javac 21.0.x
```

---

## 💡 **VIRTUAL THREADS - THE BIG FEATURE**

### **What are Virtual Threads?**

Virtual threads are **lightweight threads** managed by the JVM, not the OS.

**Traditional Threads** (Platform Threads):
- Heavy (1 MB stack per thread)
- OS-managed
- Limited to ~thousands of threads

**Virtual Threads**:
- Lightweight (few KB per thread)
- JVM-managed
- Can create millions of threads

### **Creating Virtual Threads**

```java
// Old way (platform threads)
Thread thread = new Thread(() -> {
    System.out.println("Hello from platform thread");
});
thread.start();

// New way (virtual threads) - Method 1
Thread vThread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from virtual thread");
});

// Method 2 - Using Executors
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        System.out.println("Task in virtual thread");
    });
} // Auto-shutdown

// Method 3 - Thread.startVirtualThread()
Thread.startVirtualThread(() -> {
    System.out.println("Quick virtual thread");
});
```

### **Real-World Example: HTTP Server**

```java
import java.io.*;
import java.net.*;
import java.util.concurrent.Executors;

public class VirtualThreadServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("Server started on port 8080");

        // Handle each connection in a virtual thread
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            while (true) {
                Socket client = serverSocket.accept();
                executor.submit(() -> handleClient(client));
            }
        }
    }

    private static void handleClient(Socket client) {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            PrintWriter out = new PrintWriter(client.getOutputStream(), true)
        ) {
            String request = in.readLine();
            System.out.println("Request: " + request);

            // Simulate processing
            Thread.sleep(100); // Virtual thread parks here, very efficient!

            out.println("HTTP/1.1 200 OK\r\n\r\nHello from Virtual Thread!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

// Can handle 100,000+ concurrent connections!
```

---

## 🔀 **PATTERN MATCHING FOR SWITCH**

### **Old Way vs New Way**

**Old Way** (Before Java 21):
```java
Object obj = getObject();

if (obj instanceof String) {
    String s = (String) obj;
    System.out.println("String of length: " + s.length());
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    System.out.println("Integer: " + i);
} else if (obj instanceof Double) {
    Double d = (Double) obj;
    System.out.println("Double: " + d);
} else {
    System.out.println("Unknown type");
}
```

**New Way** (Java 21):
```java
Object obj = getObject();

switch (obj) {
    case String s  -> System.out.println("String of length: " + s.length());
    case Integer i -> System.out.println("Integer: " + i);
    case Double d  -> System.out.println("Double: " + d);
    case null      -> System.out.println("null value");
    default        -> System.out.println("Unknown type");
}
```

### **Pattern Matching with Guards**

```java
switch (obj) {
    case String s when s.length() > 10 -> 
        System.out.println("Long string: " + s);
    case String s -> 
        System.out.println("Short string: " + s);
    case Integer i when i > 0 -> 
        System.out.println("Positive integer: " + i);
    case Integer i -> 
        System.out.println("Non-positive integer: " + i);
    default -> 
        System.out.println("Something else");
}
```

---

## 📝 **RECORD PATTERNS**

### **Records (Quick Recap)**

```java
// Define a record (immutable data class)
record Point(int x, int y) {}

record Rectangle(Point topLeft, Point bottomRight) {}
```

### **Record Patterns (Deconstruction)**

```java
Object obj = new Point(10, 20);

// Pattern matching with record deconstruction
if (obj instanceof Point(int x, int y)) {
    System.out.println("Point at: " + x + ", " + y);
}

// In switch
switch (obj) {
    case Point(int x, int y) -> 
        System.out.println("Point at: " + x + ", " + y);
    case Rectangle(Point(int x1, int y1), Point(int x2, int y2)) -> 
        System.out.println("Rectangle from (" + x1 + "," + y1 + ") to (" + x2 + "," + y2 + ")");
    default -> 
        System.out.println("Unknown shape");
}
```

---

## 🔢 **SEQUENCED COLLECTIONS**

### **New Interfaces**

Java 21 adds methods to get first/last elements and reversed views:

```java
import java.util.*;

public class SequencedCollectionsDemo {
    public static void main(String[] args) {
        // List (SequencedCollection)
        List<String> list = new ArrayList<>(List.of("A", "B", "C", "D"));
        
        String first = list.getFirst();  // "A"
        String last = list.getLast();    // "D"
        list.addFirst("Z");               // ["Z", "A", "B", "C", "D"]
        list.addLast("E");                // ["Z", "A", "B", "C", "D", "E"]
        list.removeFirst();               // ["A", "B", "C", "D", "E"]
        list.removeLast();                // ["A", "B", "C", "D"]
        List<String> reversed = list.reversed(); // ["D", "C", "B", "A"]

        // LinkedHashSet (SequencedSet)
        SequencedSet<Integer> set = new LinkedHashSet<>(Set.of(1, 2, 3, 4, 5));
        int firstElem = set.getFirst();  // 1
        int lastElem = set.getLast();    // 5
        SequencedSet<Integer> reversedSet = set.reversed();

        // LinkedHashMap (SequencedMap)
        SequencedMap<String, Integer> map = new LinkedHashMap<>();
        map.put("Alice", 30);
        map.put("Bob", 25);
        map.put("Charlie", 35);
        
        Map.Entry<String, Integer> firstEntry = map.firstEntry();  // Alice=30
        Map.Entry<String, Integer> lastEntry = map.lastEntry();    // Charlie=35
        SequencedMap<String, Integer> reversedMap = map.reversed();
    }
}
```

---

## 🧵 **BEST PRACTICES (2025-2026)**

### **1. Use Virtual Threads for I/O-Heavy Tasks**

```java
// ✅ GOOD: Virtual threads for I/O
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> {
            // Call API, read file, query database
            fetchDataFromAPI();
        });
    }
}

// ❌ BAD: Platform thread pool for I/O
ExecutorService executor = Executors.newFixedThreadPool(100);
// Limited to 100 concurrent requests, wasteful
```

### **2. Use Records for Immutable Data**

```java
// ✅ GOOD: Record for DTOs, value objects
record User(String name, int age, String email) {}

// ❌ BAD: Verbose class
class User {
    private final String name;
    private final int age;
    private final String email;
    
    public User(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }
    // ... getters, equals, hashCode, toString
}
```

### **3. Use Pattern Matching for `instanceof`**

```java
// ✅ GOOD: Pattern matching
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}

// ❌ BAD: Manual cast
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}
```

### **4. Use Sequenced Collections Methods**

```java
List<String> list = new ArrayList<>(List.of("A", "B", "C"));

// ✅ GOOD: Direct methods
String first = list.getFirst();
String last = list.getLast();

// ❌ BAD: Manual index access
String first = list.get(0);
String last = list.get(list.size() - 1);
```

---

## 🛠️ **BUILD TOOLS**

### **Maven (pom.xml)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-java-app</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Example: Spring Boot 3.2+ (supports Java 21) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
    </dependencies>
</project>
```

### **Gradle (build.gradle)**

```gradle
plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0-SNAPSHOT'

java {
    sourceCompatibility = '21'
    targetCompatibility = '21'
}

repositories {
    mavenCentral()
}

dependencies {
    // Example: Spring Boot 3.2+
    implementation 'org.springframework.boot:spring-boot-starter-web:3.2.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

application {
    mainClass = 'com.example.Main'
}
```

---

## 📚 **POPULAR FRAMEWORKS (Java 21 Compatible)**

### **Spring Boot 3.2+**

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/hello")
    public String hello() {
        return "Hello from Spring Boot 3.2 with Java 21!";
    }

    // Using virtual threads with Spring Boot
    @GetMapping("/async")
    public String asyncOperation() {
        Thread.startVirtualThread(() -> {
            // Perform async task
            System.out.println("Virtual thread in Spring!");
        });
        return "Task submitted";
    }
}
```

**Enable Virtual Threads in Spring Boot**:
```properties
# application.properties
spring.threads.virtual.enabled=true
```

---

## 🧪 **TESTING WITH JUNIT 5**

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    
    @Test
    @DisplayName("Addition of two numbers")
    void testAdd() {
        assertEquals(5, Calculator.add(2, 3));
    }

    @Test
    void testVirtualThreads() throws InterruptedException {
        var result = new java.util.concurrent.atomic.AtomicInteger(0);
        
        Thread vThread = Thread.ofVirtual().start(() -> {
            result.set(42);
        });
        
        vThread.join();
        assertEquals(42, result.get());
    }

    @RepeatedTest(10)
    void testConcurrency() {
        // Test runs 10 times
        assertTrue(true);
    }
}
```

---

## 📖 **LEARNING RESOURCES**

- **Official Java Tutorials**: https://docs.oracle.com/en/java/javase/21/
- **Java 21 Release Notes**: https://www.oracle.com/java/technologies/javase/21-relnote-issues.html
- **Project Loom (Virtual Threads)**: https://openjdk.org/projects/loom/
- **Modern Java in Action** (book)
- **Effective Java 3rd Edition** (Joshua Bloch)

---

**Document Created**: November 6, 2025  
**Purpose**: Java 21 programming reference for SHENRON AI knowledge base  
**Usage**: Help users write modern Java code with 2025-2026 best practices

**✨ Java 21 knowledge complete! ✨** ☕

