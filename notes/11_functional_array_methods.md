# 11 — Functional Array Methods (`map`, `filter`, `reduce`, `find`, `some`, `every`)

> **Quick Summary:** Pure & immutable data transformations, `.find()` vs `.filter()[0]` performance, short-circuiting with `some`/`every`, and grouping/aggregating with `.reduce()`.

---

## 1. Method Comparison Matrix

| Method | Returns | Stops Early? | Purpose |
|---|---|---|---|
| **`.map()`** | Array of same length | No | 1-to-1 data transformation |
| **`.filter()`** | Array ($\le$ original length) | No | Subset selection based on boolean predicate |
| **`.find()`** | First matching element (or `undefined`) | **YES** | Fast single-item lookup |
| **`.some()`** | `boolean` | **YES** | Checks if **at least one** item matches |
| **`.every()`** | `boolean` | **YES** | Checks if **all** items match |
| **`.reduce()`** | Any single accumulator value | No | Fold array into a sum, object, map, or pipeline |

---

## 2. Senior Performance Tip: `.find()` vs `.filter()[0]`

```javascript
// ❌ SLOW on large arrays (iterates all 50,000 items):
const user = users.filter((u) => u.id === targetId)[0];

// ✅ FAST (halts execution immediately on first match):
const user = users.find((u) => u.id === targetId);
```

---

## 3. Mastering `.reduce()`

### Pattern 1: Mathematical Aggregation
```javascript
const netBalance = transactions.reduce((acc, t) => {
  return t.type === "credit" ? acc + t.amount : acc - t.amount;
}, 0);
```

### Pattern 2: Grouping Objects by Category
```javascript
const grouped = orders.reduce((acc, order) => {
  (acc[order.status] ??= []).push(order);
  return acc;
}, {});
```

### ⚠️ The Fatal `.reduce()` Bug
Calling `.reduce()` without an `initialValue` on an empty array crashes with:
`TypeError: Reduce of empty array with no initial value`.
**Production Rule:** Always supply the second argument (`, 0`, `, {}`, `, []`).
