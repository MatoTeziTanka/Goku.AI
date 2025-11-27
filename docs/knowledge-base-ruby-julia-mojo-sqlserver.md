# Ruby 3.3+, Julia 1.10+, Mojo 0.6+ & SQL Server 2019 Quick Reference

## RUBY 3.3+ (2025-2026)

**Version**: 3.3+ (Latest stable)
**Use**: Web development (Rails), scripting, automation

### Installation
gem install rails # Web framework
rbenv install 3.3.0 # Version manager

### Basics
name = "Seth"
age = 30
puts "#{name} is #{age} years old"

### Methods
def greet(name)
  "Hello, #{name}!"
end

### Classes
class Person
  attr_accessor :name, :age
  
  def initialize(name, age)
    @name = name
    @age = age
  end
end

### Rails 7 (Web Framework)
rails new myapp
rails generate scaffold Article title:string body:text
rails server

---

## JULIA 1.10+ (2025-2026)

**Version**: 1.10+ (Latest stable)
**Use**: Scientific computing, data science, ML

### Installation
# Download from julialang.org

### Basics
name = "Seth"
age = 30
println("$name is $age years old")

### Functions
function add(x, y)
    x + y
end
add(x, y) = x + y # Short form

### Multiple Dispatch (Julia's superpower)
function process(x::Int)
    println("Integer: $x")
end
function process(x::String)
    println("String: $x")
end

### Data Science
using DataFrames, Plots
df = DataFrame(x=1:10, y=rand(10))
plot(df.x, df.y)

### GPU Computing
using CUDA
a = cu([1, 2, 3]) # GPU array

---

## MOJO 0.6+ (2025-2026)

**Version**: 0.6+ (New language by Modular)
**Use**: AI/ML, high-performance Python alternative

### Installation
# Download from modular.com

### Basics (Python-like syntax)
fn main():
    let name = "Seth"
    let age: Int = 30
    print(name, "is", age, "years old")

### Performance
fn add(x: Int, y: Int) -> Int:
    return x + y

### Python Interoperability
from python import Python
let np = Python.import_module("numpy")
let array = np.array([1, 2, 3])

### SIMD (Single Instruction Multiple Data)
from sys.intrinsics import simd_load, simd_store
# Vectorized operations for performance

---

## SQL SERVER 2019 (Complete Guide)

**Edition**: Developer & Standard
**Use**: Relational database, enterprise applications

### Installation (Windows)
Download SQL Server 2019 from Microsoft
Install with default settings
Install SSMS (SQL Server Management Studio)

### Connect
Server: localhost or VM100
Authentication: Windows Authentication or SQL Server

### Basic SQL

#### Create Database
CREATE DATABASE MyDatabase;
USE MyDatabase;

#### Create Table
CREATE TABLE Users (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(255) UNIQUE,
    Age INT,
    CreatedAt DATETIME DEFAULT GETDATE()
);

#### Insert Data
INSERT INTO Users (Name, Email, Age) VALUES ('Seth', 'seth@example.com', 30);

#### Query Data
SELECT * FROM Users;
SELECT Name, Email FROM Users WHERE Age > 25;

#### Update Data
UPDATE Users SET Age = 31 WHERE Name = 'Seth';

#### Delete Data
DELETE FROM Users WHERE Age < 18;

### Advanced Features

#### Stored Procedures
CREATE PROCEDURE GetUsersByAge @MinAge INT
AS
BEGIN
    SELECT * FROM Users WHERE Age >= @MinAge;
END;
-- Execute: EXEC GetUsersByAge @MinAge = 25;

#### Views
CREATE VIEW ActiveUsers AS
SELECT Name, Email FROM Users WHERE Age >= 18;

#### Indexes
CREATE INDEX idx_email ON Users(Email);

#### Transactions
BEGIN TRANSACTION;
UPDATE Users SET Age = Age + 1;
COMMIT; -- or ROLLBACK;

### High Availability

#### Always On Availability Groups
Primary replica + secondary replicas
Automatic failover for high availability

#### Backup & Restore
BACKUP DATABASE MyDatabase TO DISK = 'C:\\Backup\\MyDatabase.bak';
RESTORE DATABASE MyDatabase FROM DISK = 'C:\\Backup\\MyDatabase.bak';

### Performance Tuning

#### Execution Plans
SET SHOWPLAN_TEXT ON;
SELECT * FROM Users;

#### Query Store
Enable Query Store for performance monitoring

#### Indexing Strategy
Clustered index (primary key)
Non-clustered indexes for frequently queried columns

### Integration Services (SSIS)
ETL (Extract, Transform, Load) tool
Data migration and transformation

### Reporting Services (SSRS)
Report generation and delivery
Paginated reports, dashboards

### Analysis Services (SSAS)
OLAP cubes for business intelligence
Tabular and multidimensional models

### PowerShell Administration
Import-Module SqlServer
Invoke-Sqlcmd -Query "SELECT * FROM Users" -ServerInstance "localhost"

### Best Practices
1. Always use parameterized queries (prevent SQL injection)
2. Index frequently queried columns
3. Regular backups (full, differential, transaction log)
4. Monitor performance with Query Store
5. Use stored procedures for complex logic
6. Enable Always On for high availability

### Learning Resources
- Microsoft Learn: learn.microsoft.com/sql
- SQL Server Documentation: docs.microsoft.com/sql
- Brent Ozar (SQL Server expert): brentozar.com

**Complete Ruby, Julia, Mojo, SQL Server reference for SHENRON**

