# 04 — Variables, Hoisting & Temporal Dead Zone (TDZ)

> **Quick Summary:** Engine mechanics of `var` vs `let` vs `const`, lexical environments, proof of hoisting, and the loop closure trap.

---

## 1. `var` vs `let` vs `const`

| Feature | `var` | `let` | `const` |
|---|---|---|---|
| **Scope** | Function scoped (ignores `{}` blocks) | Block scoped `{}` | Block scoped `{}` |
| **Hoisting** | Hoisted + initialized with `undefined` | Hoisted, but in TDZ | Hoisted, but in TDZ |
| **Reassignable** | Yes | Yes | No (`TypeError`) |
| **Redeclarable** | Yes (bug-prone) | No (`SyntaxError`) | No (`SyntaxError`) |

---

## 2. The 2 Phases of Execution

JavaScript does not run straight top-to-bottom. It executes in two passes:
1. **Creation / Parsing Phase:** V8 scans the scope and allocates memory for all variable declarations.
2. **Execution Phase:** V8 executes the code line-by-line, assigning values.

---

## 3. What is the Temporal Dead Zone (TDZ)?

The **Temporal Dead Zone (TDZ)** is the region of code between the start of a block and the declaration of a `let` or `const` variable. Accessing the variable in this zone throws a `ReferenceError`.

### Proof that `let` is Hoisted:
```javascript
let myCity = "Surat";

function show() {
  console.log(myCity); // 💥 ReferenceError: Cannot access 'myCity' before initialization
  let myCity = "Mumbai";
}
show();
```
*If `let` were not hoisted*, the engine would not know `myCity` exists inside `show()` and would print the outer `"Surat"`. The fact that it throws an error proves the local declaration was hoisted into the function's scope during the creation phase!

---

## 4. Why `const` Objects Can Be Mutated

```javascript
const user = { name: "Asha" };
user.name = "Ravi"; // ✅ Allowed! (Mutating properties inside the object)
user = {};          // ❌ TypeError! (Reassigning the variable reference)
```
* **`const` only locks the variable's memory address pointer**, not the object's contents.
* To make an object immutable, use `Object.freeze(user)`.

---

## 5. The Classic Loop Trap: `var` vs `let`

```javascript
// Prints: 3 3 3
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}

// Prints: 0 1 2
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);
}
```
* **With `var`:** There is **one single shared memory box** for `i`. By the time the timers fire, the loop has ended and `i = 3`.
* **With `let`:** Because `let` is block-scoped, JavaScript creates a **brand new memory binding** for every single iteration. Each callback captures its own unique snapshot of `j`.
