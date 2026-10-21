# 07 — Loops, Iteration & The Async forEach Trap

> **Quick Summary:** `for...of` vs `for...in`, iterating modern objects, and why `forEach` silently breaks with `async/await`.

---

## 1. `for...of` vs `for...in`

| Feature | `for...of` | `for...in` |
|---|---|---|
| **Iterates Over** | **VALUES** of Iterables (Arrays, Sets, Maps, Strings) | **KEYS / PROPERTY NAMES** of Objects |
| **Array Usage** | ✅ **Standard & Recommended** | ❌ **Dangerous Anti-Pattern** |
| **Output Type** | Direct values | String indices (`"0"`, `"1"`) + Prototype keys! |

```javascript
const colors = ["red", "green", "blue"];

// for...of gives VALUES:
for (const color of colors) {
  console.log(color); // "red", "green", "blue"
}

// Getting both Index and Value in for...of:
for (const [index, color] of colors.entries()) {
  console.log(index, color); // 0 "red", 1 "green", 2 "blue"
}
```

---

## 2. Iterating Objects (The Modern Way)

Avoid `for...in` on plain objects. Use `Object` static methods:
```javascript
const user = { name: "Asha", role: "admin", city: "Surat" };

Object.keys(user);    // ["name", "role", "city"]
Object.values(user);  // ["Asha", "admin", "Surat"]

for (const [key, value] of Object.entries(user)) {
  console.log(`${key} => ${value}`);
}
```

---

## 3. The #1 Senior Bug: `forEach` with `async/await`

```javascript
// ❌ BROKEN: forEach does NOT wait for promises!
async function process() {
  console.log("Start");

  [1, 2, 3].forEach(async (num) => {
    await wait(100);
    console.log("Num:", num);
  });

  console.log("End"); // Runs IMMEDIATELY!
}
// Output: Start -> End -> Num: 1 -> Num: 2 -> Num: 3
```

### Why?
`Array.prototype.forEach` is a synchronous 2009 function. Internally, it calls `callback(item)` and **throws away the returned Promise**. It never `await`s the callback.

---

## 4. The 2 Production Solutions

### Solution A: Sequential Waiting (One-by-one in order)
Use **`for...of`** (the `await` pauses the main loop):
```javascript
for (const num of [1, 2, 3]) {
  await wait(100);
  console.log("Num:", num);
}
console.log("End"); // Waits for all items to finish!
```

### Solution B: Concurrent / Parallel Execution (Fastest)
Use **`map` + `Promise.all`**:
```javascript
await Promise.all(
  [1, 2, 3].map(async (num) => {
    await wait(100);
    console.log("Num:", num);
  })
);
console.log("All finished in parallel!");
```
