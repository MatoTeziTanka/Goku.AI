# C/C++ C23/C++23 Programming Reference (2025-2026)
## Modern Systems Programming with Latest Standards

**C Standard**: C23 (ISO/IEC 9899:2023)  
**C++ Standard**: C++23 (ISO/IEC 14882:2023)  
**Use**: Systems programming, embedded, performance-critical applications

## C23 NEW FEATURES

### nullptr constant
#define nullptr ((void*)0) // Now standard keyword

### typeof and typeof_unqual
typeof(variable) new_var = variable;

### Digit separators
int million = 1'000'000;

### Binary literals
int binary = 0b1010;

### Enhanced _Static_assert
_Static_assert(sizeof(int) == 4);

## C++23 NEW FEATURES

### std::print and std::println
#include <print>
std::println("Hello, {}!", "World");

### Multidimensional operator[]
matrix[i, j] = value; // Instead of matrix[i][j]

### if consteval
if consteval {
    // Compile-time code
} else {
    // Runtime code
}

### std::expected<T, E>
Error handling without exceptions

### Ranges improvements
More range algorithms and views

## C BASICS

### Variables
int age = 30;
float price = 99.99f;
double precise = 3.14159;
char letter = 'A';
const int MAX = 100;

### Pointers
int value = 42;
int *ptr = &value;
*ptr = 50; // Dereference

### Arrays
int numbers[5] = {1, 2, 3, 4, 5};
char str[] = "Hello";

### Structs
struct Person {
    char name[50];
    int age;
};

## C++ BASICS

### Classes
class Person {
private:
    std::string name;
    int age;
public:
    Person(std::string n, int a) : name(n), age(a) {}
    void display() { std::cout << name << ", " << age << std::endl; }
};

### Smart Pointers (Modern C++)
std::unique_ptr<int> ptr = std::make_unique<int>(42);
std::shared_ptr<int> shared = std::make_shared<int>(42);

### RAII (Resource Acquisition Is Initialization)
{
    std::lock_guard<std::mutex> lock(mtx);
    // Mutex automatically released when scope ends
}

## MODERN C++ (C++11/14/17/20/23)

### Auto keyword
auto value = 42; // int
auto str = "Hello"; // const char*
auto vec = std::vector<int>{1, 2, 3};

### Range-based for loop
for (const auto& item : container) {
    std::cout << item << std::endl;
}

### Lambda functions
auto add = [](int a, int b) { return a + b; };
auto result = add(5, 3);

### Move semantics
std::string str = "Hello";
std::string moved = std::move(str); // str is now empty

### constexpr
constexpr int square(int x) { return x * x; }

## MEMORY MANAGEMENT

### C-style (manual)
int *arr = (int*)malloc(10 * sizeof(int));
free(arr);

### C++-style (RAII, smart pointers)
std::vector<int> vec(10); // Automatic cleanup
auto ptr = std::make_unique<int[]>(10); // Automatic cleanup

## STANDARD LIBRARY (C++)

### Containers
std::vector<int> vec;
std::map<std::string, int> map;
std::unordered_map<std::string, int> hashmap;
std::set<int> set;

### Algorithms
std::sort(vec.begin(), vec.end());
std::find(vec.begin(), vec.end(), 42);
std::transform(vec.begin(), vec.end(), result.begin(), [](int x) { return x * 2; });

### Strings
std::string str = "Hello";
str += " World";
std::cout << str << std::endl;

## MULTITHREADING (C++11+)

### Threads
#include <thread>
std::thread t([]() {
    std::cout << "Hello from thread" << std::endl;
});
t.join();

### Mutex
#include <mutex>
std::mutex mtx;
{
    std::lock_guard<std::mutex> lock(mtx);
    // Critical section
}

### Atomic
#include <atomic>
std::atomic<int> counter(0);
counter++;

## BUILD SYSTEMS

### CMake (Modern standard)
cmake_minimum_required(VERSION 3.20)
project(MyApp)
add_executable(myapp main.cpp)

### Makefile (Traditional)
CC = gcc
CFLAGS = -Wall -std=c23
myapp: main.c
    $(CC) $(CFLAGS) -o myapp main.c

## COMPILERS

### GCC 13+
gcc -std=c23 main.c -o program
g++ -std=c++23 main.cpp -o program

### Clang 17+
clang -std=c23 main.c -o program
clang++ -std=c++23 main.cpp -o program

### MSVC (Visual Studio 2022+)
cl /std:c++latest main.cpp

## BEST PRACTICES (2025-2026)

1. Use smart pointers (unique_ptr, shared_ptr) not raw pointers
2. Prefer RAII for resource management
3. Use const correctness
4. Prefer STL containers over C-style arrays
5. Use auto for type deduction
6. Enable all compiler warnings (-Wall -Wextra)
7. Use modern C++20/23 features (ranges, concepts, coroutines)

## POPULAR LIBRARIES

- Boost: Comprehensive C++ libraries
- Qt: GUI framework
- SFML: Multimedia library
- Eigen: Linear algebra
- OpenCV: Computer vision

## LEARNING RESOURCES

- cppreference.com (comprehensive reference)
- learncpp.com (beginner-friendly)
- The C++ Programming Language (Bjarne Stroustrup)
- Effective Modern C++ (Scott Meyers)

**Complete C/C++ reference for SHENRON**

