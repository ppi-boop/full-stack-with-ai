# 10 — Destructuring, Spread, Rest & Optional Chaining (`?.`)

> **Quick Summary:** Object/array destructuring with renaming and defaults, Spread vs Rest mechanics, Optional Chaining (`?.`), and immutable nested state updates.

---

## 1. Destructuring: Renaming & Defaults

```javascript
const user = { id: 101, username: "asha_dev" };

// Renaming: creates 'handle', does NOT create 'username'
const { username: handle } = user;

// Default values: only kicks in if undefined
const { role = "guest" } = user;

// Nested unpacking:
const { profile: { city } } = user;
```

---

## 2. Spread (`...`) vs Rest (`...`)

| Feature | Spread (`...`) | Rest (`...`) |
|---|---|---|
| **Action** | **Unpacks / Expands** items out of an array or object | **Gathers / Collects** leftover items into an array |
| **Position** | On the **right side** of `=` or inside function calls | On the **left side** of `=` or inside parameter lists |
| **Examples** | `const copy = [...arr];`<br>`Math.max(...nums);` | `const [first, ...others] = arr;`<br>`function sum(...nums) {}` |

---

## 3. Optional Chaining (`?.`)

* Stops evaluation immediately if the operand before `?.` is `null` or `undefined`, returning `undefined` instead of throwing a `TypeError`.

```javascript
// Safe property access:
const street = order?.customer?.address?.street;

// Safe method execution:
props.onSuccess?.(); // Only executes if onSuccess is a function
```

---

## 4. Immutable Deep Updates (The React Pattern)

Because spread is **shallow**, updating a nested field requires spreading every level down to the target:

```javascript
const nextState = {
  ...state,
  user: {
    ...state.user,
    address: {
      ...state.user.address,
      city: "Mumbai" // Modified field
    }
  }
};
```
