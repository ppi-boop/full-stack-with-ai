# 08 — Functions: Declarations, Expressions, Arrows & `this`

> **Quick Summary:** Hoisting differences, why arrow functions have no `this`, constructor limits, and the object literal return trap.

---

## 1. Declarations vs Expressions vs Arrows

| Feature | Function Declaration | Function Expression | Arrow Function |
|---|---|---|---|
| **Syntax** | `function foo() {}` | `const foo = function() {}` | `const foo = () => {}` |
| **Hoisting** | **Fully hoisted** (usable before line) | Hoisted in TDZ (cannot call before) | Hoisted in TDZ (cannot call before) |
| **Own `this`?** | ✅ Yes (depends on caller) | ✅ Yes (depends on caller) | ❌ **No (lexically inherited)** |
| **Use with `new`?** | ✅ Yes (Constructor) | ✅ Yes (Constructor) | ❌ **No (`TypeError`)** |
| **`arguments` object?** | ✅ Yes | ✅ Yes | ❌ **No (use `...args` instead)** |

---

## 2. The 3 Golden Rules of Arrow Functions

1. **Never use arrow functions for object methods that need `this`:**
   ```javascript
   const user = {
     name: "Asha",
     greet: () => `Hi ${this.name}` // 💥 this is undefined/window!
   };
   ```
2. **Always use arrow functions for inner callbacks (like `.map`, `.filter`, `setTimeout`):**
   ```javascript
   // ✅ Inherits `this` from the outer method:
   numbers.map((n) => n * this.factor);
   ```
3. **Cannot be a constructor:** Calling `new (() => {})()` throws `TypeError: ... is not a constructor`.

---

## 3. Two Classic Syntax Traps

### 1. Returning an Object Literal
Curly braces `{}` default to a code block. Wrap in parentheses `()` to return an object:
```javascript
// ❌ Returns undefined:
const makeUser = (name) => { name: name };

// ✅ Returns { name: "Asha" }:
const makeUser = (name) => ({ name: name });
```

### 2. Default Parameters
Default parameters **only trigger on `undefined`**, NEVER on `null`:
```javascript
function setRole(role = "viewer") { ... }

setRole(undefined); // role = "viewer" (Default kicks in)
setRole(null);      // role = null      (Explicit null is kept!)
```
