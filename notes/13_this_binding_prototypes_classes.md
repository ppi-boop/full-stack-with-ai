# 13 — The `this` Keyword, Explicit Binding & Prototypes

> **Quick Summary:** The 4 binding rules of `this`, `.call()` vs `.apply()` vs `.bind()`, the permanent bind lock, and prototype inheritance.

---

## 1. The 4 Rules Determining `this`

| Rule | How Function is Called | What `this` Points To |
|---|---|---|
| **1. Default** | `fn()` (standalone call) | `undefined` in strict mode / ESM; `window` in legacy |
| **2. Implicit** | `obj.fn()` (called via object dot) | The object immediately before the dot (`obj`) |
| **3. Explicit** | `fn.call(ctx)`, `fn.apply(ctx)` | Whatever object is passed as `ctx` |
| **4. `new` operator** | `new Constructor()` | A brand new empty object `{}` created by the engine |
| **Arrow function** | `() => {}` | **No own `this`** (lexically inherits from surrounding code) |

---

## 2. `.call()` vs `.apply()` vs `.bind()`

```javascript
function greet(city, country) {
  return `${this.name} in ${city}, ${country}`;
}
const user = { name: "Asha" };

// 1. .call(): executes immediately, arguments passed as comma list
greet.call(user, "Surat", "India");

// 2. .apply(): executes immediately, arguments passed as an Array
greet.apply(user, ["Surat", "India"]);

// 3. .bind(): does NOT execute immediately; returns a locked function
const boundFn = greet.bind(user);
boundFn("Surat", "India");
```

> **The Permanent Bind Rule:** Once a function is bound with `.bind()`, its `this` cannot be changed by `.call()` or `.apply()`. `boundFn.call(otherObj)` will still execute with the original bound `this`!

---

## 3. The "Detached Method" Trap

```javascript
const user = {
  name: "Ravi",
  getName() { return this.name; }
};

const get = user.getName; // Stripped from its object owner!
get(); // 💥 this is undefined (Rule 1: Default Binding)

// Fix:
const boundGet = user.getName.bind(user);
boundGet(); // "Ravi"
```

---

## 4. Prototypes & Classes Under the Hood

* JavaScript classes are **syntactic sugar over prototype chains**.
* Methods defined in a `class` are stored on `Class.prototype`, not on individual instances:
  * 10,000 instances share **one copy** of methods in memory.
* Private fields use the `#` prefix: `#secret = 123` (enforced natively by the engine).
