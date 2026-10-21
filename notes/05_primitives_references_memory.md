# 05 — Primitive vs Reference Values & Memory Model

> **Quick Summary:** Stack vs Heap, IEEE 754 floating point precision, `NaN` identity, shallow vs deep copying, and React reference equality.

---

## 1. Stack vs Heap Memory

| Feature | Primitive Values | Reference Types (Objects/Arrays) |
|---|---|---|
| **Types** | `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol` | `Object`, `Array`, `Function`, `Map`, `Set` |
| **Storage Location** | **Stack** (fast, fixed-size) | **Heap** (dynamic, flexible memory) |
| **Variable Holds** | The **actual raw value** | A **pointer (memory address)** to the Heap |
| **Copy Behavior** | Copied by **value** (completely independent) | Copied by **reference** (shares the same object) |

---

## 2. Core Gotchas & Production Traps

### 1. `typeof null === "object"`
* A historical 1995 bug in the original JavaScript engine's type-tag system.
* `null` is a **primitive**, not an object.
* Always check for null with strict equality: `value === null`.

### 2. Floating-Point Math (`0.1 + 0.2 !== 0.3`)
* Computers store numbers in binary floating-point (IEEE 754 format). Binary cannot cleanly represent fractions like $1/10$.
* `0.1 + 0.2` results in `0.30000000000000004`.
* **The Production Rule for Money:**
  * **Never use floats for currency.**
  * Store all monetary amounts as **integer smallest units** (cents or paise):
    ```javascript
    const priceInPaise = 1999; // ₹19.99
    ```

### 3. `NaN` Is Never Equal to Itself
* `NaN === NaN` is `false`.
* To check if a value is `NaN`, use:
  ```javascript
  Number.isNaN(val); // ✅ Correct
  ```

---

## 3. Shallow Copy vs Deep Copy

```javascript
const user = { name: "Asha", address: { city: "Surat" } };

// Shallow Copy (Spread):
const shallow = { ...user };
shallow.address.city = "Mumbai"; // 💥 Mutates user.address.city too!

// Deep Copy (structuredClone):
const deep = structuredClone(user);
deep.address.city = "Delhi";     // ✅ user.address.city remains "Surat"
```

* **Spread (`...`) or `Object.assign`:** Only clones the 1st layer. Nested objects are still shared references.
* **`structuredClone()`:** Native deep copy (handles nested objects, arrays, Dates, Maps, Sets). Avoid `JSON.parse(JSON.stringify())` as it strips functions and `undefined`.

---

## 4. Why This Matters in React (`===` Comparison)

React uses shallow reference equality (`Object.is`) to detect prop and state changes:
```javascript
{} === {} // false (Two different heap addresses)
[] === [] // false
```
* If you pass an inline object literal `<Chart config={{ theme: "dark" }} />`, React sees a **new memory address on every render** and forces the child component to re-render.
