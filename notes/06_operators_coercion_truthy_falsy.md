# 06 — Operators, Type Coercion, Truthy/Falsy & Nullish Coalescing

> **Quick Summary:** The 8 falsy values, abstract equality conversion rules, the `||` vs `??` production bug, and coercion traps.

---

## 1. The Only 8 Falsy Values

Every value in JavaScript is truthy **EXCEPT** these 8:
1. `false`
2. `0`
3. `-0`
4. `0n` (BigInt zero)
5. `""` (Empty string)
6. `null`
7. `undefined`
8. `NaN`

> **Critical Trap:**
> In Python, `[]` and `{}` are falsy. **In JavaScript, `[]` and `{}` are TRUTHY!**
> Non-empty string `"0"` is also truthy in boolean contexts.

---

## 2. `||` (Logical OR) vs `??` (Nullish Coalescing)

| Operator | Fallback Trigger | Behavior on `0`, `""`, and `false` |
|---|---|---|
| **`||`** | Triggers on **ANY falsy value** | **Replaces them** (Causes bugs when `0` or `""` are valid data) |
| **`??`** | Triggers **ONLY on `null` and `undefined`** | **Preserves them** (Safe for counts, strings, and booleans) |

### The Production Bug Example:
```javascript
const speed = 0; // 0 km/h is a valid measurement!

const bug = speed || 50;  // 50 (Bug: 0 was treated as missing!)
const safe = speed ?? 50; // 0  (Correct: 0 is preserved!)
```

---

## 3. `==` (Loose) vs `===` (Strict) Coercion Rules

* **`===` (Strict):** No type conversion. If types differ, returns `false`.
* **`==` (Loose):** Converts types using the Abstract Equality algorithm:
  * Comparing string/boolean with number $\rightarrow$ **converts both to numbers!**

```javascript
"0" == false   // TRUE! ("0" -> 0, false -> 0, so 0 == 0)
"0" === false  // FALSE (string !== boolean)

0 == ""        // TRUE! ("" converts to 0)
[] == false    // TRUE! ([] converts to "", then to 0)
null == undefined  // TRUE! (Special specification rule)
null === undefined // FALSE (Different types)
```

### Math Coercion Trap:
* `+` prefers string concatenation: `"5" + 1 === "51"`
* `-`, `*`, `/` force number conversion: `"5" - 1 === 4`
