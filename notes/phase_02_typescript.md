# Phase 02 — TypeScript Master Study Handbook

> **Comprehensive Revision Guide:** Phase 2 (TypeScript Foundations & Advanced Typing)  
> Covers compile-time vs runtime boundaries, structural typing, types vs interfaces, generics, discriminated unions, utility types, and React typing.

---

## Quick Navigation
* [Topic 1: TypeScript Mental Model (Compile-Time vs Runtime, Structural Typing & Inference)](#topic-1-typescript-mental-model)
* [Topic 2: Primitive, Array, Tuple, Object & Function Types](#topic-2-primitive-array-tuple-object--function-types)

---

# Topic 1: TypeScript Mental Model

### 1. Simple Definitions & Mental Models (Easy Language)
* **What is TypeScript?** A static blueprint inspector and spellchecker for JavaScript.
* **Compile-Time vs Runtime (Airport Scanner Analogy):**
  * **Compile-Time:** The airport security scanner scanning your luggage before departure.
  * **Runtime:** The flight in mid-air. The scanner is left on the ground. TypeScript completely disappears from your production code.
* **The Golden Rule:** TypeScript does **NOT** make your code run faster or add runtime type validation. `tsc` strips all types and produces 100% plain JavaScript.

### 2. Under the Hood Mechanics

#### A. Type Erasure
All `type`, `interface`, and type annotations are deleted during compilation:
```typescript
interface User { id: number; name: string; }
function greet(u: User): string { return `Hi, ${u.name}`; }
```
Compiles directly to:
```javascript
function greet(u) { return `Hi, ${u.name}`; }
```

#### B. The API Trust Boundary Fallacy
TypeScript cannot validate data arriving over the network:
```typescript
// ⚠️ DANGER: TypeScript believes your assertion, but runtime data might differ!
const user = await res.json() as User;
```
If the backend returns `{ id: "10", name: null }`, TypeScript will not catch it at runtime. A runtime schema validator (like **Zod**) is needed at trust boundaries.

#### C. Structural Typing vs Excess Property Checks
* **Structural Typing ("Shape over Name"):**
  If an object has all required properties, extra properties are tolerated when passing a variable reference:
  ```typescript
  type Point = { x: number; y: number };
  function draw(p: Point) { ... }
  
  const p3d = { x: 1, y: 2, z: 3 };
  draw(p3d); // ✅ Allowed! (Wallet analogy: has x and y)
  ```
* **Excess Property Checks (Inline Object Literal Trap):**
  Passing an object literal directly triggers strict typo protection:
  ```typescript
  draw({ x: 1, y: 2, z: 3 }); 
  // ❌ Compile Error: Object literal may only specify known properties!
  ```

#### D. Type Inference & `as const`
* **Local Variables:** Let TypeScript infer types automatically (`let x = 5` is `number`; `const x = 5` is literal type `10`).
* **Boundaries:** Explicitly annotate function parameters, exported function return types, and public interfaces.
* **`as const`:** Locks an object or array to `readonly` and infers literal types rather than primitive widenings (`string`, `number`).

---

# Topic 2: Primitive, Array, Tuple, Object & Function Types

### 1. Simple Definitions & Mental Models (Easy Language)
* **Primitives:** Basic building blocks (`number`, `string`, `boolean`, `bigint`, `symbol`).
* **Array (`string[]`):** The Shopping List. Variable length, can add/remove elements anytime.
* **Tuple (`[string, number]`):** The Passport ID. Fixed length, fixed order per slot (e.g., React's `useState` returns `[state, setter]`).
* **`void` vs `undefined` as return types:**
  * `undefined`: Function **must explicitly return the literal value `undefined`**.
  * `void`: Tells caller **"ignore whatever value is returned"**. Allows callbacks to return values that callers discard (e.g. `forEach(num => set.add(num))`).
* **The `{}` & `Object` Anti-Pattern:** `{}` does NOT mean a plain object; it means **any non-nullish value** (strings and numbers pass `{}`!). Use `Record<string, unknown>` or explicit shapes instead.

### 2. Under the Hood Mechanics & Code

#### A. Array vs Tuple Inference Trap
```typescript
let a = ["Alpha", 1]; // Inferred as (string | number)[] — standard array!
a.push("Beta");       // ✅ Allowed
a.push(2);            // ✅ Allowed
// a.push(true);      // ❌ Error: boolean not assignable to string | number

// Explicit tuple annotation needed for fixed length/slots:
let t: [string, number] = ["Alpha", 1];
```

#### B. Tuple Mutation Trap (`.push` bypass)
```typescript
const point: [number, number] = [10, 20];
point.push(30); // 💥 Compiles! Array.prototype methods bypass tuple length checks.

// Senior Fix (Readonly Tuple):
const safePoint: readonly [number, number] = [10, 20];
// safePoint.push(30); // ❌ Compile Error: push does not exist on readonly tuple
```

#### C. Optional Properties & Strict Null Checks
```typescript
type Config = {
  readonly port: number;
  tags?: string[]; // Type is string[] | undefined
};

const server: Config = { port: 8080, tags: ["web"] };
// server.tags.push("api"); // ❌ Compile Error with strictNullChecks: Object is possibly 'undefined'!
server.tags?.push("api");   // ✅ Safe: Optional chaining handles undefined cleanly
```
