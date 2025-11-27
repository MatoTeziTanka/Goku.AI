# Python 3.11+ Complete Programming Reference (2025-2026)
## Modern Python Development with Performance & AI/ML Focus

**Version**: Python 3.11+ (3.12, 3.13 features included)  
**Use**: AI/ML, web development, automation, data science, scripting  
**Status**: Most popular language for AI/ML in 2025-2026

## PYTHON 3.11+ NEW FEATURES

### Exception Groups (3.11)
```python
try:
    raise ExceptionGroup("multiple errors", [ValueError("error 1"), TypeError("error 2")])
except* ValueError as e:
    print("Caught ValueError group")
except* TypeError as e:
    print("Caught TypeError group")
```

### Task Groups (3.11)
```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(1))
        task2 = tg.create_task(fetch_data(2))
    # Both tasks complete before continuing
```

### Type Hints Improvements (3.11+)
```python
from typing import Self, TypeVarTuple, Unpack

class Builder:
    def build(self) -> Self:  # Returns same type
        return self
```

### Python 3.12 Features
- Per-Interpreter GIL (better parallelism)
- Improved error messages with precise locations
- f-string improvements (nested expressions)

### Python 3.13 Features (Latest)
- Experimental JIT compiler (2x-10x faster for some workloads)
- Free-threaded mode (no GIL)
- Improved performance across the board

## BASICS

### Variables & Types
```python
name = "Seth"
age = 30
price = 99.99
is_active = True
items = [1, 2, 3]
data = {"key": "value"}
```

### Functions
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Lambda
add = lambda x, y: x + y

# Default arguments
def power(base: int, exp: int = 2) -> int:
    return base ** exp
```

### Classes
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

# Dataclasses (modern, concise)
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
```

## ASYNC PROGRAMMING (CRITICAL FOR AI/ML)

### Async/Await
```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    result = await fetch_data("https://api.example.com/data")
    print(result)

asyncio.run(main())
```

### Concurrent Execution
```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1"

async def task2():
    await asyncio.sleep(1)
    return "Task 2"

async def main():
    # Run concurrently
    results = await asyncio.gather(task1(), task2())
    print(results)  # ['Task 1', 'Task 2']
```

## AI/ML LIBRARIES (2025-2026 FOCUS)

### PyTorch 2.x (Industry Standard)
```python
import torch
import torch.nn as nn

# Create tensor
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

# Neural network
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = Net()
```

### TensorFlow 2.x
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')
```

### Transformers (Hugging Face)
```python
from transformers import pipeline

# Sentiment analysis
classifier = pipeline('sentiment-analysis')
result = classifier("I love this product!")

# Text generation
generator = pipeline('text-generation', model='gpt2')
text = generator("Once upon a time", max_length=50)
```

### LangChain (LLM Applications)
```python
from langchain import OpenAI, LLMChain, PromptTemplate

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(input_variables=["product"], template="What is {product}?")
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("AI")
```

## DATA SCIENCE STACK

### NumPy (Numerical Computing)
```python
import numpy as np

arr = np.array([[1, 2], [3, 4]])
mean = np.mean(arr)
result = arr @ arr  # Matrix multiplication
```

### Pandas (Data Analysis)
```python
import pandas as pd

df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})
filtered = df[df['age'] > 27]
grouped = df.groupby('age').count()
```

### Matplotlib/Seaborn (Visualization)
```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.plot([1, 2, 3], [4, 5, 6])
plt.show()

sns.heatmap(data, annot=True)
plt.show()
```

## WEB FRAMEWORKS

### FastAPI (Modern, High-Performance)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Run: uvicorn main:app --reload
```

### Flask (Simple, Flexible)
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.json
    return {"result": "processed"}

# Run: flask run
```

### Django (Full-Featured)
```python
# views.py
from django.http import JsonResponse

def api_view(request):
    return JsonResponse({"message": "Hello"})

# urls.py
from django.urls import path

urlpatterns = [
    path('api/', api_view),
]
```

## DATABASE & ORM

### SQLAlchemy (SQL ORM)
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
```

### Pydantic (Data Validation)
```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    age: int

user = User(name="Seth", email="seth@example.com", age=30)
```

## AUTOMATION & SCRIPTING

### File Operations
```python
from pathlib import Path

# Read file
content = Path('file.txt').read_text()

# Write file
Path('output.txt').write_text("Hello World")

# List files
for file in Path('.').glob('*.py'):
    print(file)
```

### HTTP Requests
```python
import requests

response = requests.get('https://api.example.com/data')
data = response.json()

response = requests.post('https://api.example.com/create', json={'key': 'value'})
```

## TESTING

### Pytest (Standard)
```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# Run: pytest
```

## PACKAGE MANAGEMENT

### pip (Standard)
```bash
pip install package-name
pip install -r requirements.txt
pip freeze > requirements.txt
```

### Poetry (Modern)
```bash
poetry init
poetry add fastapi
poetry install
```

## VIRTUAL ENVIRONMENTS

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Deactivate
deactivate
```

## TYPE HINTS (BEST PRACTICE 2025-2026)

```python
from typing import List, Dict, Optional, Union

def process_items(items: List[str], config: Dict[str, int]) -> Optional[str]:
    if not items:
        return None
    return items[0]

# Type aliases
UserId = int
UserData = Dict[str, Union[str, int]]

def get_user(user_id: UserId) -> UserData:
    return {"name": "Seth", "age": 30}
```

## PERFORMANCE OPTIMIZATION

### Using NumPy for Speed
```python
import numpy as np

# Slow (pure Python)
result = sum([x**2 for x in range(1000000)])

# Fast (NumPy)
result = np.sum(np.arange(1000000)**2)
```

### Multiprocessing
```python
from multiprocessing import Pool

def process_item(item):
    return item ** 2

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        results = pool.map(process_item, range(1000))
```

## BEST PRACTICES (2025-2026)

1. Use type hints for all functions
2. Use dataclasses for simple data containers
3. Use async/await for I/O-bound operations
4. Use FastAPI for APIs (not Flask for new projects)
5. Use Pydantic for data validation
6. Use pytest for testing
7. Use Black for code formatting
8. Use Ruff for linting (replaces flake8, pylint)
9. Use uv or Poetry for dependency management
10. Use Python 3.11+ for performance

## LEARNING RESOURCES

- Official Docs: docs.python.org
- Real Python: realpython.com
- PyTorch Tutorials: pytorch.org/tutorials
- FastAPI Docs: fastapi.tiangolo.com
- Hugging Face Course: huggingface.co/course

**Complete Python 3.11+ reference for SHENRON - AI/ML focused**

