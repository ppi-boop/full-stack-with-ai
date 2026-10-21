# 09 — Arrays, Objects, Maps, Sets & Mutating vs Immutable Methods

> **Quick Summary:** Mutating vs Immutable array methods, `.sort()` string comparison trap, `.at(-1)`, deduplicating with `Set`, and `Map` vs plain objects.

---

## 1. Mutating vs Immutable Methods

| Mutating (Destroys Original) | Immutable (Returns New Copy) |
|---|---|
| `push()`, `pop()` | `concat()` |
| `shift()`, `unshift()` | `slice()` |
| `splice()` | `map()`, `filter()` |
| `sort()` | `toSorted()` (ES2023) |
| `reverse()` | `toReversed()` (ES2023) |

> **The React Rule:** React uses reference equality (`Object.is`) to detect state changes. Never mutate state with `push` or `splice`. Always return a new array with `spread` or immutable methods (`filter`, `map`).

---

## 2. The `.sort()` Trap

By default, `.sort()` converts all items to **strings** and compares alphabetical character codes:
```javascript
[10, 5, 40, 25, 100, 1].sort(); 
// Output: [1, 10, 100, 25, 40, 5] (Alphabetical order!)

// Fix: Always pass a comparison function:
numbers.sort((a, b) => a - b); // [1, 5, 10, 25, 40, 100]
```

---

## 3. Modern Indexing: `.at(-1)`

Negative indexing from the end of an array without verbose `.length - 1`:
```javascript
const list = ["apple", "banana", "cherry"];
list.at(-1); // "cherry"
list.at(-2); // "banana"
```

---

## 4. `Set` vs `Map`

### `Set` (Unique Values Only)
* Deduplicates arrays in one clean line:
```javascript
const unique = [...new Set(["react", "node", "react", "next"])];
// ["react", "node", "next"]
```

### `Map` (Key-Value Store)
* Plain objects only allow strings and symbols as keys. `Map` allows **ANY key type** (including Objects, DOM nodes, Functions).
* Has a built-in `.size` property and guarantees insertion order.
```javascript
const user = { id: 42 };
const sessionMap = new Map();
sessionMap.set(user, { token: "abc" });
sessionMap.get(user); // { token: "abc" }
```
