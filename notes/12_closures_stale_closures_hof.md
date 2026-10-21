# 12 — Callbacks, Higher-Order Functions, Closures & Stale Closures

> **Quick Summary:** Lexical environments, the backpack analogy, private variables, writing `debounce()`, and solving the React Stale Closure bug.

---

## 1. What is a Closure?

A **Closure** is a function bundled together with references to its surrounding lexical state.
* **The Backpack Model:** When a function is created, it packs all variables in scope into a private "backpack". Wherever the function is passed or executed, it retains access to those variables.
* **Heap Retention:** Even when the outer function completes, variables referenced by the inner function are preserved on the **Heap** (not garbage collected).

```javascript
function makeCounter() {
  let count = 0; // Private variable encapsulated in closure
  return () => ++count;
}

const c1 = makeCounter();
const c2 = makeCounter(); // Separate closure backpack!
c1(); // 1
c1(); // 2
c2(); // 1
```

---

## 2. Real-World Implementation: `debounce()`

Delays execution until a specified idle duration has passed (essential for search inputs and resize events):

```javascript
function debounce(fn, delayMs) {
  let timerId; // Stored in the closure scope

  return function(...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      fn(...args);
    }, delayMs);
  };
}
```

---

## 3. The React "Stale Closure" Bug

Occurs when a callback or `useEffect` captures a state variable from an earlier render and continues referencing the old snapshot:

```jsx
// ❌ BUG: Always reads count from initial render (0 + 1 = 1)
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1); // Trapped in stale closure!
  }, 1000);
  return () => clearInterval(timer);
}, []); // Missing count in dependency array

// ✅ FIX: Functional State Updater
setCount((prev) => prev + 1); // Always guaranteed to read the latest state!
```
