# Phase 02 — TypeScript Master Study Handbook

> **Comprehensive Revision Guide:** Phase 2 (TypeScript Foundations & Advanced Typing)  
> Covers compile-time vs runtime boundaries, structural typing, types vs interfaces, generics, discriminated unions, utility types, and React typing.

---

## Quick Navigation
* [Topic 1: TypeScript Mental Model (Compile-Time vs Runtime, Structural Typing & Inference)](#topic-1-typescript-mental-model)
* [Topic 2: Primitive, Array, Tuple, Object & Function Types](#topic-2-primitive-array-tuple-object--function-types)
* [Topic 3: Interfaces vs Type Aliases; Optional (?) and readonly](#topic-3-interfaces-vs-type-aliases-optional--and-readonly)
* [Topic 4: Union, Intersection, Literal Types & Discriminated Unions](#topic-4-union-intersection-literal-types--discriminated-unions)

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

---

# Topic 3: Interfaces vs Type Aliases; Optional (`?`) and `readonly`

### 1. Simple Definitions & Mental Models (Easy Language)
* **`type` (The Swiss Army Knife):** Can describe *anything* — unions (`"light" | "dark"`), tuples, primitives (`type ID = string`), objects, and functions. Once defined, it is closed and cannot be reopened.
* **`interface` (The Expandable Lego Brick):** Strictly for **object contracts and classes**. Can extend other interfaces cleanly (`extends`), and can be declared multiple times to automatically combine fields (**Declaration Merging**).
* **`readonly`:** Compile-time flag preventing reassignment (`user.id = 2`). Disappears at runtime (not a runtime lock like `Object.freeze`).
* **The "Everything Optional `?`" Trap:** Marking properties with `?` to silence TypeScript errors turns your code into an unsafe guessing game where `{}` is considered valid. Only use `?` for truly optional/nullable fields.

### 2. Under the Hood Mechanics & Code

#### A. Extending Objects: `extends` vs Intersection (`&`)
```typescript
// Interface extension (Recommended for object contracts)
interface BaseEntity { readonly id: number; createdAt: string; }
interface Order extends BaseEntity { totalAmount: number; }

// Type alias intersection
type BaseEntity = { readonly id: number; createdAt: string; };
type Order = BaseEntity & { totalAmount: number; };
```

#### B. Declaration Merging (Interface-Only Superpower)
```typescript
interface Cart { items: string[]; }
interface Cart { total: number; }

// TypeScript automatically merges both declarations:
const c: Cart = { items: ["Book"], total: 20 }; // Must have BOTH fields!
```
*Crucial in production for augmenting third-party library types, `window`, or `process.env` in `.d.ts` files.*

#### C. `readonly` is Shallow (The Nested Mutation Trap)
```typescript
type Admin = {
  readonly config: { theme: string };
};

const admin: Admin = { config: { theme: "light" } };
admin.config.theme = "dark"; // ✅ Allowed! (readonly was on 'config' pointer, not 'theme')
// admin.config = { theme: "dark" }; // ❌ Error: Cannot assign to 'config'
```

#### D. When `interface extends` Fails
An `interface` can only extend an **object type or statically-known object shape**. It **CANNOT** extend a union (`type ID = string | number`) or primitive because interfaces must describe objects.

---

# Topic 4: Union, Intersection, Literal Types & Discriminated Unions

### 1. Simple Definitions & Mental Models (Easy Language)
* **Literal Types:** Exact specific values instead of general categories (e.g. `"paid"`, `404`, `true`).
* **Union (`|` = OR):** The Restaurant Menu Choice. Value can be one of several options (`"light" | "dark"`).
* **Intersection (`&` = AND):** The Combo Meal. Combines all properties into one required shape (`Person & Employee`).
  * **The Conflict Trap:** If `A` has `y: string` and `B` has `y: number`, `A & B` produces `y: never` because no value can simultaneously be a string and a number. You can never instantiate this object!
* **Discriminated Unions (The Tagged State):** Mutually exclusive objects sharing a common literal property (the tag / discriminant, e.g. `status` or `type`).
* **The "Impossible State" Anti-Pattern:** Modeling UI state as `{ isLoading: boolean; isError: boolean; data?: T }` allows invalid states (loading + error + data simultaneously). Discriminated unions prevent this permanently.

### 2. Under the Hood Mechanics & Code

#### A. Modeling UI & API States Cleanly
```typescript
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: T };

function render(s: RequestState<string[]>) {
  switch (s.status) {
    case "idle":
    case "loading":
      return "Loading...";
    case "error":
      return `Error: ${s.message}`; // ✅ s is narrowed: message is guaranteed to exist
    case "success":
      return s.data.join(", ");     // ✅ s is narrowed: data is guaranteed to exist
    default: {
      // 🛡️ Exhaustive check: compile error if a case is added to RequestState but not handled here
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}
```

#### B. The Exhaustive `never` Check
When all possible union variants are handled in `if/else` or `switch`, the remaining type in `default` narrows down to `never`. If a developer adds a new variant to the union later, TypeScript immediately flags the `never` assignment, catching unhandled cases at compile time!
