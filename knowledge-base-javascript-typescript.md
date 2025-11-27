# JavaScript ES2024 & TypeScript 5.3+ Programming Reference (2025-2026)
## Modern Web Development with Latest Features

**JavaScript**: ES2024 (ECMAScript 2024)  
**TypeScript**: 5.3+ (Latest stable)  
**Status**: Industry standard for web development

## JAVASCRIPT ES2024 NEW FEATURES

### Array Grouping
Object.groupBy() and Map.groupBy() for grouping array elements

Example:
const people = [{name: "Alice", age: 30}, {name: "Bob", age: 30}];
const byAge = Object.groupBy(people, p => p.age);

### Promise.withResolvers()
Easier promise creation with external resolve/reject

### Temporal API (Stage 3)
Modern date/time API replacing Date

## TYPESCRIPT 5.3+ FEATURES

### Decorator Metadata
Stage 3 decorators with metadata support

### Import Attributes
import json from './data.json' with { type: 'json' };

### Type Narrowing Improvements
Better type inference in switch statements and instanceof

## BASICS

### Variables
let name = "Seth";
const age = 30;
var legacy = "avoid"; // Use let/const instead

### Functions
// Arrow functions (preferred)
const add = (a: number, b: number): number => a + b;

// Traditional function
function multiply(a: number, b: number): number {
    return a * b;
}

// Async/await
async function fetchData(url: string): Promise<Response> {
    const response = await fetch(url);
    return response.json();
}

## TYPES IN TYPESCRIPT

### Basic Types
let name: string = "Seth";
let age: number = 30;
let isActive: boolean = true;
let values: number[] = [1, 2, 3];
let tuple: [string, number] = ["Seth", 30];

### Interfaces
interface User {
    name: string;
    age: number;
    email?: string; // Optional property
}

### Type Aliases
type ID = string | number;
type Result<T> = { success: true; data: T } | { success: false; error: string };

### Generics
function identity<T>(arg: T): T {
    return arg;
}

## MODERN JAVASCRIPT PATTERNS

### Destructuring
const {name, age} = user;
const [first, second] = array;

### Spread Operator
const newArray = [...oldArray, newItem];
const newObject = {...oldObject, newProp: value};

### Optional Chaining
const email = user?.profile?.email;

### Nullish Coalescing
const name = user.name ?? "Guest";

## ASYNC PROGRAMMING

### Promises
fetch(url)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

### Async/Await (Preferred)
try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
} catch (error) {
    console.error(error);
}

## POPULAR FRAMEWORKS (2025-2026)

### React 18+
const App = () => {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
};

### Vue 3+
<script setup>
const count = ref(0);
</script>
<template><button @click="count++">{{ count }}</button></template>

### Angular Latest
@Component({...})
export class AppComponent {
    count = signal(0);
}

### Next.js 14+ (React framework)
Server components, app router, server actions

### Svelte 5 (Runes)
New reactivity system with runes

## NODE.JS RUNTIME

### File Operations
import fs from 'fs/promises';
const data = await fs.readFile('file.txt', 'utf8');

### HTTP Server
import http from 'http';
http.createServer((req, res) => {
    res.writeHead(200);
    res.end('Hello World');
}).listen(3000);

### Express.js
import express from 'express';
const app = express();
app.get('/', (req, res) => res.send('Hello'));
app.listen(3000);

## BUILD TOOLS

### Vite (Modern, fast)
npm create vite@latest my-app

### TypeScript Compiler
tsc --init
tsc

### ESBuild (Very fast)
esbuild app.ts --bundle --outfile=out.js

## TESTING

### Jest
test('adds 1 + 2 to equal 3', () => {
    expect(add(1, 2)).toBe(3);
});

### Vitest (Vite-native)
import { test, expect } from 'vitest';
test('adds', () => expect(add(1, 2)).toBe(3));

## BEST PRACTICES (2025-2026)

1. Use TypeScript for type safety
2. Prefer async/await over .then() chains
3. Use const by default, let when needed, never var
4. Use arrow functions for concise syntax
5. Enable strict mode in TypeScript
6. Use ES modules (import/export) not CommonJS (require)

## PACKAGE MANAGERS

npm (default), yarn (fast), pnpm (efficient)

## LEARNING RESOURCES

- MDN Web Docs: developer.mozilla.org
- TypeScript Handbook: typescriptlang.org/docs/handbook
- javascript.info (comprehensive guide)

**Complete JavaScript/TypeScript reference for SHENRON**

