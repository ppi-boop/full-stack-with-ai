## 9. SQL and MongoDB

### Joins and set operations

**Q: What is a self join and when do you use it?**
A: A table joined to itself using two aliases, for example employees to their managers: `SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id`.

**Q: What is the difference between a filter in `ON` and in `WHERE` on a LEFT JOIN?**
A: A `WHERE` filter on the right table throws away the NULL rows, so the LEFT JOIN behaves like an INNER JOIN. Put the condition in `ON` to keep unmatched left rows.

**Q: How do you find rows in table A that have no match in table B?**
A: Use `LEFT JOIN b ON ... WHERE b.id IS NULL` or `WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.a_id = a.id)`. Avoid `NOT IN` when the subquery can return NULL, because then the condition matches no rows at all.

**Q: Why do counts and sums come out too large after a join?**
A: A one-to-many join repeats the "one" side's row once per match, so summing a column from that side counts it several times. Aggregate in a subquery first, or use `COUNT(DISTINCT ...)` where that is valid.

**Q: What do `INTERSECT` and `EXCEPT` do?**
A: `INTERSECT` returns rows that appear in both queries. `EXCEPT` returns rows from the first query that are not in the second (`MINUS` in Oracle). Both remove duplicates unless you add `ALL`.

**Q: What does `LATERAL` do in PostgreSQL?**
A: It lets a subquery in `FROM` refer to columns of tables listed before it, so it runs per row. A typical use is "latest 3 orders for each customer".

### Aggregation, NULL and query order

**Q: `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`?**
A: `COUNT(*)` counts rows. `COUNT(col)` counts rows where `col` is not NULL. `COUNT(DISTINCT col)` counts unique non-NULL values.

**Q: Why does `WHERE col = NULL` return nothing?**
A: Any comparison with NULL gives "unknown", and `WHERE` keeps only true rows. Use `IS NULL` or `IS NOT NULL`.

**Q: `COALESCE` vs `NULLIF`?**
A: `COALESCE(a, b)` returns the first non-NULL value. `NULLIF(a, b)` returns NULL when the two are equal, which avoids divide-by-zero: `x / NULLIF(y, 0)`.

**Q: What is the logical execution order of a SELECT query?**
A: FROM and JOIN, WHERE, GROUP BY, HAVING, window functions, SELECT, DISTINCT, ORDER BY, then LIMIT. That is why a SELECT alias cannot be used in `WHERE` but can be used in `ORDER BY`.

**Q: How do you count conditionally in one query?**
A: `COUNT(*) FILTER (WHERE status = 'paid')` in PostgreSQL, or the portable `SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)`.

### Window functions

**Q: How is a window function different from `GROUP BY`?**
A: A window function calculates over a set of related rows but keeps every input row in the output, while `GROUP BY` collapses rows into one per group. Syntax: `fn() OVER (PARTITION BY ... ORDER BY ...)`.

**Q: `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`?**
A: For scores 100, 90, 90, 80: `ROW_NUMBER` gives 1,2,3,4, `RANK` gives 1,2,2,4 and `DENSE_RANK` gives 1,2,2,3.

**Q: What do `LAG` and `LEAD` do?**
A: They read a column from the previous or next row in the window, for example `revenue - LAG(revenue) OVER (ORDER BY day)` for the change from the previous day.

**Q: How do you write a running total?**
A: `SUM(amount) OVER (ORDER BY created_at)`. Add `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` if you want strict row-by-row behaviour, because the default `RANGE` frame gives tied rows the same total.

**Q: Can you filter on a window function result in `WHERE`?**
A: No, windows are calculated after `WHERE`. Put the query in a subquery or CTE and filter outside it (some databases have `QUALIFY`, PostgreSQL does not).

### CTEs and subqueries

**Q: What is a recursive CTE?**
A: A CTE with a base query and a recursive part joined by `UNION ALL`, repeated until no new rows appear. It is used for trees such as org charts or category paths, and it needs a stop condition.

**Q: Correlated vs uncorrelated subquery?**
A: A correlated subquery refers to columns of the outer query and logically runs once per outer row. An uncorrelated one runs once. Slow correlated subqueries can often be rewritten as a join or window function.

**Q: Does a CTE act as an optimisation fence in PostgreSQL?**
A: Before version 12 a CTE was always materialised. From 12 on, a simple non-recursive CTE used once is inlined, and you can force either behaviour with `MATERIALIZED` or `NOT MATERIALIZED`.

### Write the query

**Q: How would you write a query for the second highest salary?**
A: `SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees)`. For the Nth highest, use `DENSE_RANK()` in a subquery.

**Q: How would you get the top 3 salaries in each department?**
A: `SELECT * FROM (SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk FROM employees e) t WHERE rnk <= 3`.

**Q: How would you find duplicate emails?**
A: `SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1`.

**Q: How would you delete duplicate users but keep the lowest id (PostgreSQL)?**
A: `DELETE FROM users a USING users b WHERE a.email = b.email AND a.id > b.id`.

**Q: How would you get total revenue per month?**
A: `SELECT date_trunc('month', created_at) AS month, SUM(amount) FROM orders GROUP BY 1 ORDER BY 1` (PostgreSQL).

**Q: How would you get the latest order of each customer?**
A: PostgreSQL: `SELECT DISTINCT ON (customer_id) * FROM orders ORDER BY customer_id, created_at DESC`. Portable: number rows with `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC)` and keep row 1.

**Q: How would you list employees who earn more than their manager?**
A: `SELECT e.name FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary`.

**Q: How would you show each row's share of the total?**
A: `SELECT name, amount, amount * 100.0 / SUM(amount) OVER () AS pct FROM sales`. The empty `OVER ()` means one window over all rows.

**Q: How would you find customers who bought both product A and product B?**
A: `SELECT customer_id FROM order_items WHERE product IN ('A', 'B') GROUP BY customer_id HAVING COUNT(DISTINCT product) = 2`.

### Indexes

**Q: How do you choose the column order in a composite index?**
A: Put columns used with equality first, then the range column, and sort columns where possible. An index on `(a, b)` serves filters on `a` and on `a, b`, but not efficiently on `b` alone (leftmost prefix rule).

**Q: With an index on `(country, city)`, which queries can use it well?**
A: `WHERE country = 'IN'` and `WHERE country = 'IN' AND city = 'Pune'` can. `WHERE city = 'Pune'` alone usually cannot, because the index is sorted by country first.

**Q: What is a covering index?**
A: An index that holds every column the query needs, so the database answers from the index alone (an index-only scan) without reading the table. PostgreSQL can add extra payload columns with `INCLUDE`.

**Q: What is a partial index?**
A: An index on only the rows matching a condition, such as `CREATE INDEX ON orders (user_id) WHERE status = 'open'`. It is smaller, faster to maintain and good for hot subsets.

**Q: Clustered vs non-clustered index?**
A: A clustered index decides the physical row order, one per table (the primary key in MySQL InnoDB, SQL Server). PostgreSQL tables are heaps with no maintained clustered index; `CLUSTER` is a one-time reorder.

**Q: When do you use B-tree, hash, GIN, GiST and BRIN indexes in PostgreSQL?**
A: B-tree is the default for equality, range and sorting. Hash is equality only. GIN suits many values per row (JSONB, arrays, full text). GiST suits geometry, ranges and nearest-neighbour. BRIN is a tiny index for huge tables whose values follow disk order, like timestamps.

**Q: Why might the database ignore my index?**
A: A function on the column (`WHERE LOWER(email) = ...`), a type mismatch, a leading wildcard (`LIKE '%abc'`), low selectivity so a scan is cheaper, stale statistics, or the wrong column order. For the function case, create an expression index on `LOWER(email)`.

**Q: Does a foreign key create an index automatically?**
A: In PostgreSQL no: only the referenced primary or unique key is indexed, so add an index on the FK column for joins and cascading deletes. MySQL InnoDB creates one automatically.

**Q: What does `CREATE INDEX CONCURRENTLY` do?**
A: It builds a PostgreSQL index without blocking writes. It is slower, cannot run inside a transaction block, and can leave an invalid index behind if it fails.

### EXPLAIN and query tuning

**Q: Is it safe to run `EXPLAIN ANALYZE` on an `UPDATE`?**
A: `EXPLAIN` only shows the estimated plan, but `EXPLAIN ANALYZE` actually executes the statement and changes data. Wrap it in `BEGIN; ... ROLLBACK;`.

**Q: What are Seq Scan, Index Scan, Index Only Scan and Bitmap Heap Scan?**
A: Seq scan reads the whole table. Index scan follows the index to rows. Index only scan reads just the index. Bitmap scan collects many matches from the index and then reads table pages in order, which suits medium selectivity.

**Q: Nested loop vs hash join vs merge join?**
A: Nested loop suits few outer rows with an indexed inner side. Hash join builds a hash table of one side and suits large equality joins. Merge join walks two sorted inputs and suits large sorted or indexed inputs.

**Q: What does it mean when estimated rows and actual rows in a plan differ hugely?**
A: The planner statistics are stale or misleading, so it may pick a bad plan. Run `ANALYZE`, raise the statistics target, or create extended statistics for correlated columns.

**Q: Why is `OFFSET 100000` slow and what is the alternative?**
A: The database still reads and throws away the first 100000 rows. Use keyset pagination: `WHERE id > :last_id ORDER BY id LIMIT 20`.

### Normalisation and schema design

**Q: Can you explain 1NF, 2NF and 3NF in simple words?**
A: 1NF: atomic values, no repeating groups. 2NF: no column depends on only part of a composite key. 3NF: non-key columns depend only on the key and not on other non-key columns ("the key, the whole key, and nothing but the key").

**Q: How do you model a many-to-many relationship?**
A: With a junction table holding two foreign keys and a composite primary key, for example `enrollments(student_id, course_id, enrolled_at)`.

**Q: UUID vs auto-increment id?**
A: Auto-increment is compact and index friendly but guessable and awkward across shards. UUIDs are globally unique and can be generated anywhere, but they are larger and random ones fragment B-trees; time-ordered UUIDs reduce that.

**Q: How does soft delete work and what are its costs?**
A: A `deleted_at` column marks rows instead of removing them, which keeps history and allows undo. Every query must filter it, and unique constraints need partial indexes that ignore deleted rows.

**Q: How should you store money?**
A: As `NUMERIC(12,2)` or as integer minor units (paise, cents). Never use floating point, which cannot represent most decimals exactly.

### Transactions, isolation and locking

**Q: Can you give an example of a non-repeatable read and of a phantom read?**
A: Non-repeatable read: you read a row twice in one transaction and a committed update changes it in between. Phantom read: you run the same range query twice and a committed insert adds a new matching row.

**Q: Does PostgreSQL allow dirty reads, and what is the default level in MySQL?**
A: No: PostgreSQL treats `READ UNCOMMITTED` as `READ COMMITTED`. Its default is Read Committed, while MySQL InnoDB defaults to Repeatable Read.

**Q: What is MVCC?**
A: Multi-version concurrency control: each transaction sees a consistent snapshot and writers create new row versions. So readers do not block writers and writers do not block readers.

**Q: What does `SELECT ... FOR UPDATE` do?**
A: It locks the selected rows until the transaction ends, so other transactions that want to change them must wait. Use it for read-then-write logic such as checking and deducting a balance.

**Q: What is `FOR UPDATE SKIP LOCKED` used for?**
A: It skips rows that another transaction has locked, so several workers can pull different jobs from a queue table without blocking each other.

**Q: Optimistic vs pessimistic locking?**
A: Pessimistic locks the row up front (`FOR UPDATE`). Optimistic uses a version column: `UPDATE ... SET version = version + 1 WHERE id = 1 AND version = 5`, and retries if zero rows were updated.

**Q: How do you prevent a lost update on an account balance?**
A: Use an atomic statement like `UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100`, lock the row with `FOR UPDATE`, or use an optimistic version check. Do not read the value into the app and write it back.

**Q: After an error inside a PostgreSQL transaction, why do later statements fail?**
A: The transaction enters an aborted state and rejects commands until you `ROLLBACK`. Use a `SAVEPOINT` and `ROLLBACK TO` if you want to recover from one failed statement and continue.

### Migrations, pooling, partitioning and replication

**Q: How do you add a NOT NULL column to a large live table safely?**
A: Use expand and contract: add the column as nullable, deploy code that writes it, backfill in small batches, then add the constraint. Recent PostgreSQL versions add a column with a constant default without rewriting the table.

**Q: Why can an `ALTER TABLE` take a site down?**
A: Many DDL statements need a strong table lock. If one waits behind a long transaction, all new queries queue behind it. Set a `lock_timeout` and run risky DDL at low traffic.

**Q: What does PgBouncer do and what is transaction pooling?**
A: PgBouncer is a lightweight connection pooler in front of PostgreSQL. In transaction mode a server connection is lent for one transaction only, which gives the best reuse but can break session-based features such as session-level `SET`, advisory locks or some prepared statements.

**Q: How do you size a connection pool?**
A: Keep it small. Each PostgreSQL connection is a server process, and more connections than the database can run in parallel only add contention. The total across all app instances must stay under `max_connections`.

**Q: Partitioning vs sharding?**
A: Partitioning splits one table into pieces (by range, list or hash) inside one database, which helps pruning and maintenance. Sharding spreads data across several database servers.

**Q: Sync vs async replication, and what is replication lag?**
A: The primary streams changes to replicas. Async is faster but replicas can lag, so reads may be stale and a failover can lose recent writes. Sync waits for the replica but adds latency. Send reads that need fresh data to the primary.

### PostgreSQL specifics

**Q: JSON vs JSONB in PostgreSQL?**
A: `JSON` stores the exact input text. `JSONB` stores a parsed binary form that is faster to query and can be indexed, but drops whitespace and duplicate keys. Use `JSONB` in almost all cases.

**Q: How do you query and index JSONB?**
A: `->` returns JSON, `->>` returns text, and `@>` tests containment: `WHERE data @> '{"role": "admin"}'`. A GIN index speeds up containment queries.

**Q: When should you not use JSONB?**
A: For fields you filter, join, constrain or aggregate heavily. Use real columns for those, and keep JSONB for sparse or variable attributes.

**Q: How do upsert and `RETURNING` work in PostgreSQL?**
A: `INSERT ... ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name RETURNING id` inserts or updates in one atomic statement and returns the row, saving a second query.

**Q: `timestamp` vs `timestamptz`?**
A: `timestamptz` stores an exact instant (internally UTC) and converts to the session time zone on display. Prefer it; plain `timestamp` has no zone and invites bugs.

**Q: What does `VACUUM` do?**
A: PostgreSQL keeps old row versions after `UPDATE` and `DELETE` (MVCC). `VACUUM` reclaims that dead space and updates the visibility map that index-only scans rely on; autovacuum normally runs it for you.

**Q: What is pgvector?**
A: A PostgreSQL extension that adds a `vector` column type, distance operators and approximate indexes for embedding similarity search. It is a good fit for RAG when your data already lives in PostgreSQL.

**Q: How do you run a nearest-neighbour query with pgvector?**
A: `SELECT id FROM docs ORDER BY embedding <=> :query_vec LIMIT 5`. The operator `<=>` is cosine distance, `<->` is L2 distance and `<#>` is negative inner product.

**Q: HNSW vs IVFFlat indexes in pgvector?**
A: HNSW usually gives better speed and recall but uses more memory and build time. IVFFlat builds faster and needs data present first plus tuning of `lists` and `probes`. Both are approximate, so results can miss true neighbours.

### MongoDB

**Q: What is `_id` and what is an ObjectId?**
A: Every document has a unique `_id`, automatically indexed. The default ObjectId is 12 bytes made of a timestamp, a random value and a counter, so it is roughly time-ordered.

**Q: What is the main schema design principle in MongoDB?**
A: Model data for how the application reads it: data accessed together is stored together. Start from your queries and access patterns, not from entity diagrams.

**Q: Why avoid unbounded arrays inside documents?**
A: A document is limited to 16 MB and large growing arrays make updates and indexes slow. Move the many side to its own collection or use a bucketing pattern.

**Q: What is the bucket pattern?**
A: Group many small records, such as sensor readings, into one document per time window instead of one document per reading. It cuts document and index count (MongoDB also has native time series collections).

**Q: What is the ESR rule for compound indexes?**
A: Order index fields as Equality, then Sort, then Range. This lets one index filter, sort and range-scan efficiently.

**Q: Which MongoDB index types are useful besides single-field?**
A: Compound, multikey (indexes each element of an array), text, TTL (auto-deletes documents after a time, checked about every minute), geospatial, partial, unique and wildcard.

**Q: How do you see whether a Mongo query uses an index?**
A: Run `explain("executionStats")`. `IXSCAN` means an index was used and `COLLSCAN` means a full collection scan. Compare `totalDocsExamined` with `nReturned`: a big gap means a poor index.

**Q: Why can `$lookup` be slow and what do you do about it?**
A: It is a left outer join between collections and is slow without an index on the foreign field. If you need it on many hot queries, consider embedding the data instead.

**Q: What is a good ordering for aggregation stages?**
A: Put `$match` and `$sort` early so they can use indexes and reduce documents, then `$group` and `$project`. Example: `db.orders.aggregate([{ $match: { status: "paid" } }, { $group: { _id: "$customerId", total: { $sum: "$amount" } } }])`.

**Q: What does `$unwind` do?**
A: It splits an array field so each element becomes its own output document, copying the other fields. It is often used before `$group` to aggregate over array items.

**Q: Does MongoDB support transactions?**
A: Yes, multi-document ACID transactions on replica sets (4.0+) and sharded clusters (4.2+). Single-document writes are already atomic, so a good embedded schema often avoids transactions, which carry extra cost.

**Q: Replica set vs sharding in MongoDB?**
A: A replica set keeps copies of the same data (one primary, several secondaries) for high availability and automatic failover. Sharding splits data across shards by a shard key for scale.

**Q: How do you pick a shard key?**
A: Choose a high-cardinality key that spreads writes evenly and matches common query filters. Avoid a monotonically increasing key like a timestamp, which creates a hot shard; a hashed key helps.

**Q: What are write concern and read concern?**
A: Write concern says how many nodes must acknowledge a write (`w: "majority"` waits for most of the replica set). Read concern says what level of committed data a read may see. Defaults vary by version, so check the docs.

**Q: How do you enforce structure in a schemaless database?**
A: Use collection validation with `$jsonSchema`, or an ODM such as Mongoose at the app level. Validation protects against bad writes without a full schema migration system.

**Q: What does Mongoose `populate` actually do?**
A: It replaces stored ids with documents by running extra queries on the client side. It is not a database join, so heavy use can create an N+1 problem.

## 10. Python

### Data model and dunder methods

**Q: What is the difference between `__str__` and `__repr__`?**
A: `__repr__` is the unambiguous developer view, ideally something you could paste back into code. `__str__` is the readable user view. `print()` uses `__str__` and falls back to `__repr__`, and containers show the `repr` of their items.

**Q: `__new__` vs `__init__`?**
A: `__new__` creates and returns the instance, then `__init__` sets it up. You override `__new__` mainly for immutable types (subclassing `int` or `tuple`) and for singletons.

**Q: What happens if you define `__eq__` but not `__hash__`?**
A: Python sets `__hash__` to `None`, so instances become unhashable and cannot be set members or dict keys. Objects that compare equal must have the same hash.

**Q: Which methods make a class behave like a container?**
A: `__len__` for `len()`, `__getitem__` for indexing, `__iter__` for loops and `__contains__` for `in`. With them your class works with `for`, `list()`, `sorted()` and more.

**Q: What does `__slots__` do?**
A: It fixes the allowed attributes and removes the per-instance `__dict__`, which saves memory and catches typos in attribute names. The cost is no dynamic attributes.

**Q: What do `@property`, `@staticmethod` and `@classmethod` do?**
A: `@property` makes a method read like an attribute (with optional setter). `@staticmethod` is a plain function in the class namespace. `@classmethod` receives the class as first argument, which suits alternative constructors like `from_json`.

**Q: What is a descriptor?**
A: An object with `__get__`, and optionally `__set__` or `__delete__`, that controls attribute access on another class. `property`, methods and `classmethod` are all built on descriptors.

### Mutability, identity and copying

**Q: Which built-in types are immutable and which are mutable?**
A: Immutable: `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `None`. Mutable: `list`, `dict`, `set`, `bytearray` and most custom objects.

**Q: Can a tuple's contents change?**
A: The tuple itself cannot be reassigned, but a mutable item inside it can change: after `t = (1, [2]); t[1].append(3)`, `t` is `(1, [2, 3])`. `t[0] = 5` raises `TypeError`.

**Q: What is the output of `rows = [[0] * 3] * 2; rows[0][0] = 1; print(rows)`?**
A: `[[1, 0, 0], [1, 0, 0]]`, because the outer `*` repeats a reference to the same inner list. Build rows with `[[0] * 3 for _ in range(2)]`.

**Q: Why is `x = my_list.sort()` a bug?**
A: `list.sort()` sorts in place and returns `None`, so `x` is `None`. Use `sorted(my_list)` to get a new sorted list.

**Q: Why must dict keys be hashable?**
A: A dict finds the slot from the key's hash, so the hash must never change. Lists, dicts and sets are unhashable; tuples of hashable items are fine.

**Q: Why is `a is b` sometimes `True` for equal integers but not reliable?**
A: CPython caches small ints and may reuse equal constants, but that is an implementation detail. Use `==` for values and `is` only for `None` and sentinel objects.

### Scope and closures

**Q: What is the LEGB rule?**
A: Python looks up a name in Local, Enclosing function, Global and Built-in scope, in that order.

**Q: Can you give a small example of a closure in Python?**
A: `def counter(): n = 0` then an inner `def inc()` that uses `nonlocal n`, `n += 1` and returns `n`, and `counter` returns `inc`. Each call to `counter()` makes a separate private count; decorators and callbacks rely on the same idea.

**Q: `nonlocal` vs `global`?**
A: `nonlocal x` rebinds `x` in the nearest enclosing function, and `global x` rebinds it at module level. Without them, assigning to a name inside a function creates a new local variable.

**Q: What is the output of `fs = [lambda: i for i in range(3)]; print([f() for f in fs])`?**
A: `[2, 2, 2]`. Closures capture the variable, not its value, so every lambda sees the final `i`. Fix with a default argument: `lambda i=i: i`.

**Q: Why does `x = 1` followed by `def f(): print(x); x = 2` raise `UnboundLocalError`?**
A: Assigning to `x` anywhere in the function makes `x` local for the whole function, so the `print` reads a local that has no value yet.

**Q: Why does `def log(msg, ts=datetime.now())` always print the same time?**
A: Default values are evaluated once, when the function is defined. Use `ts=None` and call `datetime.now()` inside the function.

### Decorators

**Q: Why use `functools.wraps` in a decorator?**
A: It copies the original function's name, docstring and metadata onto the wrapper. Without it, debugging, `help()`, and tools that inspect functions (pytest, FastAPI) see the wrapper instead.

**Q: How do you write a decorator that takes arguments, like `@retry(times=3)`?**
A: Use three layers: the outer function takes the arguments and returns the real decorator, which takes the function and returns the wrapper.

**Q: In what order do stacked decorators apply?**
A: `@a` above `@b` above `def f` means `f = a(b(f))`. `b` is applied first, but `a` is the outermost wrapper, so its code runs first on a call.

**Q: What does `functools.lru_cache` do and what are its caveats?**
A: It caches results by arguments, which must be hashable. It has no time-based expiry, `@cache` is unbounded, and putting it on instance methods keeps `self` alive in the cache.

**Q: How do you decorate an `async def` function correctly?**
A: The wrapper must also be `async def` and `await` the original call. A plain wrapper would return the un-awaited coroutine and skip your timing, retry or logging logic.

### Iterators and generators

**Q: Iterable vs iterator?**
A: An iterable has `__iter__` that returns an iterator (a list is one). An iterator has `__next__` and raises `StopIteration` at the end. A `for` loop calls `iter()` once and then `next()` repeatedly.

**Q: What is the output of `g = (x for x in range(3)); print(list(g), list(g))`?**
A: `[0, 1, 2] []`. A generator is exhausted after one pass, so the second `list(g)` is empty.

**Q: When does a generator function's body start running?**
A: Not at the call. Calling `gen()` only creates a generator object; the body runs on the first `next()`, up to the first `yield`.

**Q: What does `yield from` do?**
A: It delegates to another iterable or generator, passing its values through, and gives you that sub-generator's return value. It replaces a manual `for x in sub: yield x` loop.

**Q: What does `generator.send(value)` do?**
A: It resumes the generator and makes the paused `yield` expression evaluate to `value`. Start the generator with `next()` first.

**Q: What does `itertools.groupby` need to work correctly?**
A: Input sorted by the grouping key, because it groups only consecutive equal items. Otherwise the same key appears in several groups.

### OOP

**Q: What is the MRO and how does it solve the diamond problem?**
A: The Method Resolution Order is the linear order Python searches classes for a method, computed by C3 linearisation (see `Cls.__mro__`). Each class appears once and always before its parents, so the diamond is unambiguous.

**Q: What does `super()` really do?**
A: It returns a proxy to the next class in the MRO, which is not always the direct parent. This is what makes cooperative multiple inheritance work when every class calls `super()`.

**Q: What is an abstract base class?**
A: A class using `abc.ABC` with `@abstractmethod` methods. It cannot be instantiated until subclasses implement all abstract methods, so it defines an enforced interface.

**Q: `typing.Protocol` vs an ABC?**
A: A Protocol is structural: any class with the right methods matches, with no inheritance, and type checkers verify it. An ABC is nominal: a class must inherit from it or be registered.

**Q: Are there private attributes in Python?**
A: Not truly. `_x` is a convention for "internal", and `__x` triggers name mangling to `_ClassName__x` to avoid clashes in subclasses; it does not give real security.

**Q: What is the output of `class A: items = []`, then `a, b = A(), A(); a.items.append(1); print(b.items)`?**
A: `[1]`. `items` is a class attribute shared by all instances. Create per-instance lists in `__init__`.

**Q: What is a metaclass?**
A: The class of a class (the default is `type`), used to customise class creation. It is rarely needed; frameworks like ORMs and Pydantic use them, and `__init_subclass__` often covers simple cases.

**Q: EAFP vs LBYL?**
A: EAFP means "easier to ask forgiveness than permission": try the operation and catch the exception. LBYL means "look before you leap": check conditions first. Python style prefers EAFP, and it avoids race conditions.

### Dataclasses

**Q: Why does `tags: list = []` fail in a dataclass and what is the fix?**
A: A mutable default would be shared by all instances, so dataclasses raise `ValueError`. Use `tags: list = field(default_factory=list)`.

**Q: What do `frozen=True`, `slots=True` and `order=True` do?**
A: `frozen=True` makes instances immutable (and hashable with `eq`). `slots=True` (3.10+) uses `__slots__` to save memory. `order=True` generates `<`, `<=`, `>` and `>=` comparisons.

**Q: Dataclass vs Pydantic model vs NamedTuple?**
A: A dataclass is a plain container with no runtime validation. A Pydantic model validates and converts data, so use it at I/O boundaries like API requests. A NamedTuple is an immutable tuple with named fields.

### Typing

**Q: Does `Optional[int]` mean the argument is optional?**
A: No. It only means the value can be `int` or `None`, same as `int | None` (the `|` syntax needs Python 3.10+). The argument is optional only if it has a default.

**Q: `list[int]` vs `typing.List[int]`?**
A: Since Python 3.9 you can use the built-in generics (`list[int]`, `dict[str, int]`) directly. The `typing.List` aliases are the older style.

**Q: What are `TypeVar` and generics for?**
A: They link types together, for example `def first(items: list[T]) -> T` says the return type matches the list's item type. Python 3.12 also allows `def first[T](items: list[T]) -> T`.

**Q: `Any` vs `object`?**
A: `Any` switches type checking off for that value. `object` accepts any value, but you can only use `object`'s methods until you narrow the type with `isinstance`.

**Q: What is `Annotated` used for?**
A: It attaches metadata to a type, such as `Annotated[int, Field(gt=0)]`. Pydantic and FastAPI read that metadata for validation and dependencies.

### Exceptions

**Q: In what order do `try`, `except`, `else` and `finally` run?**
A: `try` runs first. If it raises, a matching `except` runs; if it does not raise, `else` runs. `finally` always runs last, even after a `return`.

**Q: What does `def f(): try: return 1 finally: return 2` return?**
A: `2`. A `return` in `finally` overrides the earlier return (and can even swallow exceptions), so avoid it.

**Q: Why is a bare `except:` bad?**
A: It also catches `KeyboardInterrupt` and `SystemExit`, hiding real problems. Catch specific exceptions, and use `except Exception` only at boundaries where you log and handle.

**Q: `raise` vs `raise X from e`?**
A: A bare `raise` inside `except` re-raises the same exception with its traceback. `raise X from e` raises a new exception and records `e` as its cause; `from None` hides the original.

**Q: What does `try: int("x")` then `except ValueError as e: pass` then `print(e)` do?**
A: It raises `NameError`. The name bound by `as e` is deleted when the `except` block ends.

### Context managers

**Q: How do you write a context manager with `contextlib.contextmanager`?**
A: Write a generator that does setup, then `yield`s, then cleans up inside `finally`, and decorate it with `@contextmanager`. The code before `yield` acts as `__enter__`, the yielded value is bound by `as`, and the `finally` part acts as `__exit__`.

**Q: What does the return value of `__exit__` mean?**
A: If it returns `True`, the exception raised in the `with` block is suppressed. If it returns a falsy value, the exception propagates.

**Q: What are `contextlib.suppress`, `ExitStack` and `async with` for?**
A: `suppress(Err)` ignores a specific exception. `ExitStack` manages a dynamic number of context managers. `async with` uses `__aenter__` and `__aexit__` for async resources like HTTP clients and DB sessions.

### asyncio

**Q: What happens if you call an `async def` function without `await`?**
A: You get a coroutine object and the body does not run. Python warns "coroutine ... was never awaited".

**Q: `asyncio.gather` vs `asyncio.TaskGroup`?**
A: `gather` runs awaitables concurrently and returns results in order (`return_exceptions=True` collects errors). `TaskGroup` (3.11+) gives structured concurrency: if one task fails, the others are cancelled and the errors are raised together.

**Q: What is the gotcha with `asyncio.create_task`?**
A: The event loop keeps only a weak reference, so a task you do not store may be garbage collected mid-run. Keep a reference, and await it or handle its exceptions.

**Q: How do you call blocking code from async code?**
A: `await asyncio.to_thread(func, arg)` runs it in a worker thread. Calling `time.sleep()` or `requests.get()` directly would block the whole event loop; use `await asyncio.sleep()` or an async client.

**Q: How do you limit concurrent calls, for example to an LLM API?**
A: Use `asyncio.Semaphore(n)` and wrap each call in `async with sem:`. This caps concurrency and helps stay under rate limits.

**Q: How do timeouts and cancellation work?**
A: `asyncio.timeout(5)` (3.11+) or `wait_for` cancels the work after the limit. Cancellation raises `CancelledError` at the next `await`; it derives from `BaseException`, so do not swallow it with a broad `except`.

**Q: Why does `asyncio.run()` fail inside Jupyter or an already running loop?**
A: You cannot start a second event loop in a thread that already has one running. In Jupyter use top-level `await`; in an async app just `await` the coroutine.

### Threads, processes and the GIL

**Q: When do you pick asyncio, threads or processes?**
A: asyncio for many I/O waits with async libraries, threads for blocking I/O libraries, and processes for CPU-bound work that needs real parallelism.

**Q: Does the GIL make Python code thread-safe?**
A: No. `counter += 1` is several bytecode steps, so threads can interleave and lose updates. Use `threading.Lock` or a `queue.Queue` to share data safely.

**Q: `ThreadPoolExecutor` vs `ProcessPoolExecutor`?**
A: Both come from `concurrent.futures` with the same `submit` and `map` API. Threads share memory and suit I/O. Processes avoid the GIL for CPU work but need data to be pickled between them.

**Q: What are the common problems when using `multiprocessing`?**
A: Arguments and results must be picklable (lambdas are not), and on Windows and macOS (spawn start method) the entry code needs an `if __name__ == "__main__":` guard. Process start-up and data copying also have a cost.

**Q: What is the free-threaded Python build?**
A: An optional build (PEP 703) that runs without the GIL, introduced as experimental in 3.13. Its support level and library compatibility keep evolving, so check the current release notes.

### Packaging, venv and uv

**Q: What is `uv` and why do people use it?**
A: A very fast Python package and project manager written in Rust. `uv add`, `uv sync` and `uv run` manage the venv, dependencies and a lock file (`uv.lock`) in one tool.

**Q: `requirements.txt` vs `pyproject.toml`?**
A: `pyproject.toml` is the standard place for project metadata, dependency ranges and tool config. A requirements file or lock file pins exact versions for reproducible installs.

**Q: How do you fix a circular import?**
A: Move shared code to a third module, import the module instead of its names, or import inside the function that needs it. Often the real fix is changing the structure so dependencies point one way.

### pytest

**Q: How do fixture scopes and `yield` fixtures work?**
A: A fixture runs per test by default; `scope="module"` or `"session"` shares it longer. Code after `yield` is teardown, such as closing a DB connection.

**Q: Where should you patch with `unittest.mock.patch`?**
A: Patch the name where it is looked up, not where it is defined. If `app.services` does `from llm import call`, patch `app.services.call`, not `llm.call`.

**Q: How do you test async functions with pytest?**
A: Install a plugin such as `pytest-asyncio` or use `anyio`, and mark tests with `@pytest.mark.asyncio` (or configure auto mode). Then write `async def test_...` and `await` inside.

**Q: How do you assert that code raises an error?**
A: `with pytest.raises(ValueError, match="invalid"):` around the call. The `match` argument checks the message with a regex.

### Memory and performance

**Q: How does CPython manage memory?**
A: With reference counting, which frees an object when its count hits zero, plus a cyclic garbage collector for reference cycles.

**Q: What commonly causes memory leaks in Python programs?**
A: Lingering references: global caches or lists that only grow, closures or callbacks holding large objects, and unclosed resources. Use `tracemalloc` to find them and `weakref` for caches that should not keep objects alive.

**Q: What is the time complexity of common list, set and dict operations?**
A: `list.append` is O(1) amortised, `list.insert(0, x)` and `x in list` are O(n), and `x in set` or `d[key]` are O(1) on average. For queues use `collections.deque`, where `popleft` is O(1).

### Built-ins and standard library

**Q: `defaultdict` vs `dict.setdefault` vs `Counter`?**
A: `defaultdict(list)` creates missing values automatically, `d.setdefault(k, [])` does it per call, and `Counter(words).most_common(3)` counts items and returns the top ones.

**Q: What does `zip` do with lists of different lengths?**
A: It stops at the shortest one and silently drops the rest. Use `zip(a, b, strict=True)` (3.10+) to raise an error on a mismatch.

**Q: How do you sort by multiple keys, one descending?**
A: `sorted(users, key=lambda u: (-u.age, u.name))`. Sorting is stable, so equal keys keep their original order.

**Q: How do you merge two dicts?**
A: `a | b` (3.9+) or `{**a, **b}`. In both, keys from the right side win.

**Q: What is the walrus operator?**
A: `:=` assigns inside an expression, for example `if (n := len(items)) > 10:` or `while chunk := f.read(1024):`. Use it sparingly for readability.

**Q: Why use `logging` instead of `print`?**
A: Logging has levels, formats, handlers and per-module loggers (`logging.getLogger(__name__)`), so you can send output to files or services and turn verbosity up or down without changing code.

**Q: Why does `json.dumps` fail on a `datetime`?**
A: JSON has no date type, so the encoder raises `TypeError`. Convert to a string first, or pass `default=str` or a custom encoder.

### Gotchas and output questions

**Q: What is the output of `print(0.1 + 0.2 == 0.3)`?**
A: `False`, because binary floats cannot store 0.1 exactly. Use `math.isclose` or `decimal.Decimal` for money.

**Q: What do `bool("False")`, `bool([])` and `[] == False` give?**
A: `True`, `False`, `False`. A non-empty string is truthy, an empty list is falsy, but a list never equals `False` with `==`.

**Q: What is the output of `print(-7 // 2, -7 % 2)`?**
A: `-4 1`. Floor division rounds toward minus infinity, and the modulo result takes the sign of the divisor.

**Q: What is the output of `print(round(2.5), round(3.5))`?**
A: `2 4`. Python uses round-half-to-even (banker's rounding).

**Q: What is wrong with `for i in x: x.remove(i)` where `x = [1, 2, 3, 4]`?**
A: Modifying a list while iterating skips items, so `x` ends as `[2, 4]`. Iterate over a copy (`x[:]`) or build a new list.

**Q: What is the output of `print({1, 1.0, True})`?**
A: `{1}`. The three values are equal and have the same hash, so the set keeps one. Also `True + True` is `2` because `bool` is a subclass of `int`.

**Q: What does `[1, 2, 3][5:]` return?**
A: `[]`. Slicing out of range does not raise an error, while indexing `[1, 2, 3][5]` raises `IndexError`.

**Q: What does `if __name__ == "__main__":` do?**
A: It runs the code only when the file is executed directly, not when it is imported as a module.

## 11. FastAPI

### Pydantic v2 validation

**Q: Which method names changed from Pydantic v1 to v2?**
A: `.dict()` became `model_dump()`, `.json()` became `model_dump_json()`, `parse_obj` became `model_validate`, `@validator` became `@field_validator`, `@root_validator` became `@model_validator`, and `orm_mode` became `from_attributes`.

**Q: In Pydantic v2, what does `name: str | None` with no default mean?**
A: The field is required but may be `None`. In v1 an `Optional` field implicitly defaulted to `None`; in v2 you must write `= None` to make it optional.

**Q: Lax vs strict mode in Pydantic v2?**
A: By default (lax) compatible input is converted, so the string `"5"` becomes the int `5`. Strict mode rejects such conversions and raises a validation error.

**Q: How do you write a custom field validator?**
A: Use `@field_validator("email")` on a classmethod that receives the value and returns the cleaned value or raises `ValueError`. `mode="before"` runs it before type coercion.

**Q: How do you validate across fields, such as password and confirm password?**
A: Use `@model_validator(mode="after")`, check the fields on `self`, raise `ValueError` if they do not match and return `self`.

**Q: How do you build a PATCH endpoint with partial updates?**
A: Make an update schema with optional fields and apply `data.model_dump(exclude_unset=True)`. Only the fields the client actually sent are changed.

**Q: Why use separate Pydantic schemas for create, update and read?**
A: Input and output differ: create needs a password, read must never return it, and read adds the `id` and timestamps. Separate models also prevent clients from setting fields they should not (mass assignment).

**Q: What does `ConfigDict(from_attributes=True)` do?**
A: It lets Pydantic read values from object attributes, such as SQLAlchemy models, via `Model.model_validate(orm_obj)`. That is what allows a route to return an ORM object with a `response_model`.

**Q: How do you validate query and path parameters?**
A: With `Annotated` and `Query` or `Path`: `size: Annotated[int, Query(ge=1, le=100)] = 20` and `id: Annotated[int, Path(gt=0)]`. Failures return 422 automatically.

**Q: What does a 422 error body look like?**
A: A JSON object with a `detail` list. Each item has `loc` (where, such as `["body", "email"]`), `msg` and `type`, so a frontend can map errors to form fields.

**Q: How do you use Pydantic to get structured output from an LLM?**
A: Define a model, send its `model_json_schema()` in the prompt or tool definition, then parse the reply with `model_validate_json()`. On `ValidationError`, retry or ask the model to fix its output.

### Dependencies

**Q: How do dependencies with `yield` work?**
A: Code before `yield` runs before the route and the yielded value is injected. Code after `yield` runs after the response is produced, which makes it the place for cleanup such as closing a DB session.

**Q: If a dependency is used in several places in one request, how often does it run?**
A: Once. Results are cached per request by default (`use_cache=True`), so the route and its sub-dependencies share one `get_current_user` call. Pass `use_cache=False` to disable this.

**Q: How do you apply auth to every route of a router?**
A: Use `APIRouter(dependencies=[Depends(get_current_user)])`, or `FastAPI(dependencies=[...])` for the whole app. This works when you do not need the dependency's return value.

**Q: How do you pass parameters into a dependency, such as a required role?**
A: Write a factory function `require_role(role)` that returns an inner dependency (which itself uses `Depends(get_current_user)`), then use `Depends(require_role("admin"))`. A class with `__call__` also works.

### Async vs sync

**Q: What happens when a plain `def` route calls a slow blocking library?**
A: FastAPI runs plain `def` routes in a thread pool, so the event loop stays free. The pool is limited in size (AnyIO's default is 40 threads), so heavy blocking can still exhaust it.

**Q: Why is `requests.get()` inside an `async def` route a problem?**
A: It blocks the event loop, so every other request waits. Use `httpx.AsyncClient`, or declare the route with plain `def`.

**Q: How do you handle CPU-heavy work such as PDF parsing in a FastAPI app?**
A: Do not run it on the event loop. Use a process pool or a task queue (Celery, ARQ), or a separate worker or inference service, and return a job id the client can poll.

**Q: When should DB access use `async def`?**
A: Only with an async driver (asyncpg, async SQLAlchemy). With a sync driver such as psycopg2, use plain `def` routes so the work runs in the thread pool.

### Auth and security

**Q: What is inside a JWT and is it secret?**
A: Three base64url parts: header, payload (claims such as `sub` and `exp`) and signature. It is signed, not encrypted, so anyone can read the payload. Never put secrets in it, and always verify the signature and expiry.

**Q: What does `OAuth2PasswordBearer(tokenUrl="token")` actually do?**
A: It reads the bearer token from the `Authorization` header (401 if missing) and tells Swagger UI where to log in. You still decode and verify the token yourself.

**Q: Why does the login endpoint use form data instead of JSON?**
A: `OAuth2PasswordRequestForm` follows the OAuth2 password flow, which sends `username` and `password` as form fields, and Swagger's Authorize button uses it. It needs the `python-multipart` package.

**Q: Which status codes should a FastAPI auth dependency raise?**
A: Raise 401 with a `WWW-Authenticate: Bearer` header for a missing, invalid or expired token. Raise 403 when the user is known but lacks the role or permission.

**Q: How would you implement refresh tokens in a FastAPI API?**
A: Login returns a short access token and a refresh token (httpOnly cookie, or stored hashed in the DB). A `/refresh` route verifies it, rotates it and issues a new access token; deleting the stored record revokes it.

**Q: Where should a browser app keep its JWT?**
A: An httpOnly, Secure cookie is safer against XSS than `localStorage`, but then you need CSRF protection (`SameSite`, CSRF tokens). Any script on the page can read `localStorage`.

### Middleware, CORS and lifespan

**Q: What is the lifespan handler and why is it preferred over `on_event`?**
A: It is an async context manager passed as `FastAPI(lifespan=lifespan)`. Code before `yield` runs at startup (create DB engine, HTTP client, load a model) and code after runs at shutdown. `on_event("startup")` is deprecated.

**Q: Where do you keep shared resources like an HTTP client or ML model?**
A: Create them once in the lifespan handler and store them on `app.state`, then read them through a dependency. Do not create a new client or load a model per request.

**Q: What are common CORS mistakes in a FastAPI app?**
A: Using `allow_origins=["*"]` together with credentials, forgetting that the browser sends a preflight `OPTIONS` request, and thinking CORS protects the API. It only controls which browser origins may read responses. List explicit origins in `CORSMiddleware`.

**Q: In what order does middleware run?**
A: The last middleware added is the outermost: it sees the request first and the response last.

**Q: How would you add a request id and timing log to every request?**
A: Use `@app.middleware("http")`: create an id, `response = await call_next(request)`, set an `X-Request-ID` header, and log the duration with the id. Use a dependency instead for things like auth that need route-level control.

### Background tasks, WebSockets and streaming

**Q: Can a background task safely use the request's DB session?**
A: Not reliably, because the request-scoped session may already be closed when the task runs (behaviour also depends on the FastAPI version). Open a fresh session inside the task.

**Q: How does a basic WebSocket endpoint work?**
A: Declare `@app.websocket("/ws")`, call `await websocket.accept()`, then loop with `receive_text()` and `send_text()`. Catch `WebSocketDisconnect` to clean up.

**Q: How do you authenticate a WebSocket connection?**
A: The browser WebSocket API cannot set custom headers, so pass the token in the query string, a cookie, the subprotocol or a first message. Validate it and close the connection if it is invalid.

**Q: Why does a WebSocket chat break with several workers and how do you fix it?**
A: Each worker process knows only its own connections. Use a shared broker such as Redis pub/sub to broadcast messages between workers.

**Q: SSE vs WebSocket?**
A: SSE is one-way (server to client) over plain HTTP, with automatic reconnect in `EventSource`, and is simpler to deploy. WebSocket is two-way. LLM token streaming usually uses SSE.

**Q: How do you stream LLM tokens from FastAPI?**
A: Return `StreamingResponse(gen(), media_type="text/event-stream")`, where `gen` is an async generator yielding `data: ...\n\n` chunks. The frontend reads it with `fetch` and a stream reader or `EventSource`.

**Q: Why might streaming work locally but not behind nginx?**
A: The proxy buffers the response. Disable `proxy_buffering` for that route or send the `X-Accel-Buffering: no` header. Also handle client disconnects, because the generator is cancelled and you should stop the upstream LLM call.

### SQLAlchemy sessions and Alembic

**Q: How should you manage the SQLAlchemy session in FastAPI?**
A: One session per request from a `yield` dependency: commit explicitly, roll back on error and close at the end. Never share one global session across requests.

**Q: How do you set up async SQLAlchemy?**
A: `create_async_engine("postgresql+asyncpg://...")`, then `async_sessionmaker(engine, expire_on_commit=False)`, and use `await session.execute(select(User))` inside an `AsyncSession`.

**Q: Why do people set `expire_on_commit=False` with async sessions?**
A: After a commit, attributes are expired and touching them triggers a lazy refresh, which is not allowed in async code. Turning it off keeps loaded values available to build the response.

**Q: What causes the `MissingGreenlet` error?**
A: Lazy-loading a relationship in an async session outside an awaited call. Load it up front with `selectinload` or `joinedload` in the query.

**Q: `selectinload` vs `joinedload`?**
A: `joinedload` fetches related rows in one query with a JOIN, which suits many-to-one. `selectinload` runs a second `SELECT ... WHERE id IN (...)`, which suits collections and avoids duplicated parent rows.

**Q: What are the limits of Alembic autogenerate?**
A: It compares models with the database and misses things like renames (it sees drop plus add) and some constraint or default changes. Always review the generated script, and make sure models are imported in `env.py` for `target_metadata`.

**Q: Where should migrations run in deployment?**
A: As a separate release step (job or init container running `alembic upgrade head`) before the new app version starts, not from every app instance at startup, to avoid races.

### Testing

**Q: `TestClient` vs `httpx.AsyncClient` for testing?**
A: `TestClient` is synchronous and simple. For async tests use `httpx.AsyncClient` with `ASGITransport(app=app)`. Lifespan events run with `TestClient` only when you use it as a context manager (`with TestClient(app)`).

**Q: How do you isolate the database between tests?**
A: Override `get_db` with a test session and roll back a transaction after each test, or recreate a clean schema. Prefer the same database engine as production, because SQLite differs from PostgreSQL.

**Q: How do you test routes that call an LLM?**
A: Inject the LLM client as a dependency and override it with a fake that returns canned responses. Test your parsing, retry and error paths without real calls, and keep quality checks in separate evals.

### Deployment and performance

**Q: Uvicorn vs Gunicorn for FastAPI?**
A: Uvicorn is the ASGI server. Gunicorn can act as a process manager running several Uvicorn workers, or you can use Uvicorn's own `--workers`. In Kubernetes many teams run one worker per container and scale replicas; check the current FastAPI deployment docs.

**Q: What settings matter behind a reverse proxy or load balancer?**
A: `--proxy-headers` and `--forwarded-allow-ips` (trust only your proxy) so the app sees the real scheme and client IP from `X-Forwarded-*`. Set `root_path` if the app is served under a URL prefix.

**Q: Why does in-memory state (a dict cache or counter) break with several workers?**
A: Each worker is a separate process with its own memory, so state is not shared and is lost on restart. Use Redis or a database for shared state.

**Q: Liveness vs readiness health checks?**
A: Liveness answers "is the process up", so it must be cheap. Readiness answers "can it serve traffic" and may check the database or other dependencies.

**Q: What are the top FastAPI performance fixes?**
A: Never block the event loop, use pooled async DB access, add indexes and pagination, avoid N+1 queries, cache hot data in Redis, return only needed fields with `response_model`, and profile before tuning.

### Error handling and responses

**Q: Do you `return` or `raise` an `HTTPException`?**
A: Raise it, for example `raise HTTPException(status_code=404, detail="Not found")`. FastAPI turns it into the JSON error response.

**Q: How do you add a custom exception handler?**
A: Use `@app.exception_handler(MyError)` with a function that takes the request and exception and returns a `JSONResponse`. This keeps error format and status codes consistent in one place.

**Q: How do you change the format of validation errors?**
A: Register a handler for `RequestValidationError` and return your own JSON shape, such as `{ field: message }`, so the React frontend gets one consistent error format.

**Q: 422 vs 400 vs 409?**
A: FastAPI returns 422 for schema validation failures. Use 400 for other bad requests and 409 for conflicts, such as a duplicate email. Use 201 for created and 204 for no content.

**Q: What does a `ResponseValidationError` mean?**
A: Your route returned data that does not match its `response_model`. It is a server bug and produces a 500, so fix the code or the schema.

### Routing and OpenAPI

**Q: How do you organise and version routes?**
A: Use `APIRouter(prefix="/api/v1/orders", tags=["orders"])` per feature and include each with `app.include_router`. Versioning by URL prefix keeps old clients working.

**Q: How can a React app use FastAPI's OpenAPI schema?**
A: Generate a typed client or TypeScript types from `/openapi.json` with a tool such as openapi-typescript, so frontend types stay in sync with backend schemas.
