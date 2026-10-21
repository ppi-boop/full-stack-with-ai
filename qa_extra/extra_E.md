## 16. Docker, Cloud and CI/CD

### Dockerfile and images

**Q: `CMD` vs `ENTRYPOINT`?**
A: `ENTRYPOINT` sets the fixed executable, and `CMD` supplies default arguments that `docker run` can override. For a simple app, a single `CMD ["node", "server.js"]` is enough.

**Q: `COPY` vs `ADD`?**
A: `COPY` only copies files. `ADD` can also unpack local archives and download URLs, which is surprising, so prefer `COPY`.

**Q: What does `.dockerignore` do?**
A: It keeps files like `node_modules`, `.git` and `.env` out of the build context. Builds get faster and secrets don't end up in the image.

**Q: `ARG` vs `ENV`?**
A: `ARG` exists only at build time, while `ENV` also stays in the running container. Neither is safe for secrets, because the values can show up in image metadata and history.

**Q: What is wrong with `RUN apt-get update` on one line and `RUN apt-get install -y curl` on the next?**
A: The `update` layer gets cached, so a later build can install from a stale package list and fail. Put both commands in one `RUN` and remove the apt lists afterwards.

**Q: Why avoid the `latest` tag, and what is an image digest?**
A: `latest` moves, so builds are not repeatable and can break when a new release lands. Pin a version tag, or a digest (`sha256:...`) that identifies exact image content.

**Q: Alpine or slim base image?**
A: Alpine is very small but uses musl instead of glibc, which can break some native packages (common with Python wheels). Debian `-slim` images are a bit bigger but usually cause less trouble.

**Q: How do you use a secret during a Docker build without leaving it in the image?**
A: Use a BuildKit secret mount (`RUN --mount=type=secret,...`). The secret is available only for that step and is not stored in a layer.

### Running containers

**Q: Container vs virtual machine?**
A: A VM runs a full guest OS on a hypervisor. A container shares the host kernel and isolates processes, so it starts faster and is lighter, but its isolation is weaker.

**Q: Data written inside a container is gone after it is recreated. Why?**
A: The writable layer is deleted with the container. Use a volume or external storage (database, S3) for data that must survive.

**Q: Why does a container exit right after starting?**
A: A container lives only as long as its main process (PID 1). If that process finishes, crashes or goes to the background, the container stops, so read `docker logs`.

**Q: Why does `docker stop` take about 10 seconds for a Node app?**
A: The app is not handling `SIGTERM`, often because a wrapper like `npm start` is PID 1, so Docker waits and then sends `SIGKILL`. Run `node server.js` directly and handle `SIGTERM` for a graceful shutdown.

**Q: What does exit code 137 usually mean?**
A: The process was killed with `SIGKILL`, commonly because the container hit its memory limit (OOM kill). Check `docker inspect` for `OOMKilled`.

### Networking, volumes and Compose

**Q: How do services in one Compose file reach each other?**
A: Compose creates a shared network where each service name works as a DNS name, for example host `db` on port 5432.

**Q: Why does `localhost:5432` fail from the app container when Postgres runs in another container?**
A: Inside a container, `localhost` means that container itself. Use the service name (`db`) and the container port.

**Q: `EXPOSE` vs `-p`?**
A: `EXPOSE` only documents a port. `-p 8080:3000` actually publishes container port 3000 on host port 8080.

**Q: Named volume vs bind mount?**
A: A named volume is managed by Docker and suits persistent data like database files. A bind mount maps a host folder and is handy in development for live code reload.

**Q: Does `depends_on` wait until the database is ready?**
A: By default it only waits for the container to start, not to be ready. Add a `healthcheck` with `condition: service_healthy`, and still retry the connection in the app.

### Container security

**Q: Why run the app as a non-root user in a container?**
A: If the app is compromised, the attacker gets fewer privileges inside the container and on the host. Add a `USER` instruction in the Dockerfile.

**Q: How do you find known vulnerabilities in your images?**
A: Run a scanner such as Trivy or Grype (or your registry's built-in scan) in CI and fail on high-severity issues. Rebuild regularly to pick up base-image patches.

**Q: Why is `--privileged` or mounting `/var/run/docker.sock` into a container dangerous?**
A: Both give the container close to root control of the host. Avoid them unless there is truly no alternative.

### Linux basics

**Q: What does `chmod 755 file` mean?**
A: The owner can read, write and execute (7), while the group and others can read and execute (5). Private SSH keys need stricter permissions such as `chmod 400`.

**Q: How do you find which process is using port 3000?**
A: Run `lsof -i :3000` or `ss -ltnp` and look for the port, then stop the process with `kill PID`.

**Q: `kill` vs `kill -9`?**
A: `kill` sends `SIGTERM`, which lets the process clean up. `kill -9` sends `SIGKILL`, which cannot be caught, so use it as a last resort.

**Q: Which commands show disk, memory and CPU usage on a Linux server?**
A: `df -h` for disk, `du -sh *` for folder sizes, `free -m` for memory, and `top` or `htop` for CPU and processes.

**Q: What is `systemd` and how do you read a service's logs?**
A: It starts and supervises services (Nginx, your app) at boot and restarts them on failure. Use `systemctl status SERVICE` and `journalctl -u SERVICE -f`.

**Q: How do you secure SSH access to a server?**
A: Use key-based login, disable password and root login, limit port 22 to known IPs in the security group, and keep the OS updated.

### Nginx, reverse proxy and TLS

**Q: What is a reverse proxy and why use one?**
A: A server in front of your app that receives requests and forwards them to it. It adds TLS, compression, static file serving, load balancing and hides the app's port.

**Q: What does a minimal Nginx reverse-proxy config look like?**
A: A `server` block with `location / { proxy_pass http://127.0.0.1:3000; }`, plus `proxy_set_header` lines for `Host`, `X-Forwarded-For` and `X-Forwarded-Proto`.

**Q: 502 vs 504 from Nginx?**
A: 502 means Nginx got no valid response from the upstream (app down, crashed or wrong port). 504 means the upstream did not answer in time.

**Q: Why does Express need `trust proxy` behind Nginx or a load balancer?**
A: Otherwise `req.ip` and `req.protocol` show the proxy's values, which breaks IP rate limiting and secure-cookie handling. Enable it only when you really sit behind a trusted proxy.

**Q: How do you get a free HTTPS certificate?**
A: Use Let's Encrypt through an ACME client such as Certbot, or AWS Certificate Manager behind a load balancer or CloudFront. Certificates are short-lived, so automate renewal and monitor expiry.

**Q: What extra Nginx config do WebSockets or SSE need?**
A: For WebSockets, pass the `Upgrade` and `Connection` headers using HTTP/1.1. For SSE and streaming (like LLM token streams), turn off proxy buffering and allow long timeouts.

### GitHub Actions

**Q: Workflow vs job vs step vs runner?**
A: A workflow is a YAML file triggered by events. It contains jobs (parallel by default), each job has steps, and a runner is the machine that executes the job.

**Q: How do you keep secrets safe in GitHub Actions?**
A: Store them as repository or environment secrets and read them as `${{ secrets.NAME }}`. They are masked in logs and are not given to workflows triggered by pull requests from forks.

**Q: `npm ci` vs `npm install` in CI?**
A: `npm ci` installs exactly what the lock file says, fails if it is out of sync, and starts from a clean `node_modules`. Builds become repeatable.

**Q: How do you speed up a slow CI pipeline?**
A: Cache dependencies (`setup-node` cache or `actions/cache`), run independent jobs in parallel, and skip work that did not change.

**Q: How can a workflow deploy to AWS without storing access keys?**
A: Use OpenID Connect (OIDC). GitHub issues a short-lived token and the workflow assumes an IAM role, so there are no long-lived keys in secrets.

**Q: How do you require approval before a production deploy?**
A: Use a GitHub Environment with required reviewers, and run the deploy job only on the main branch with `if: github.ref == 'refs/heads/main'`.

**Q: Why pin third-party actions to a version or commit SHA?**
A: A moving tag can be changed to run malicious code with access to your secrets. A full commit SHA is the safest pin.

### AWS basics

**Q: IAM user vs role vs policy?**
A: A policy is a JSON document that allows or denies actions. A user has long-lived credentials, while a role is assumed temporarily by a service or person and gets short-lived credentials.

**Q: How should an app on EC2 access S3?**
A: Attach an IAM role (instance profile) with a minimal S3 policy. The SDK picks up temporary credentials automatically, so no access keys live in code or env files.

**Q: Security group vs NACL?**
A: A security group is a stateful firewall attached to instances and has allow rules only. A network ACL works at the subnet level, is stateless and supports allow and deny rules.

**Q: Public vs private subnet?**
A: A public subnet has a route to an internet gateway. A private subnet has none and reaches the internet through a NAT gateway, so databases and workers belong there.

**Q: Which S3 basics should you know?**
A: Objects live in buckets, new buckets block public access by default, versioning protects against overwrites, lifecycle rules move or expire data, and presigned URLs grant temporary access.

**Q: RDS Multi-AZ vs read replica?**
A: Multi-AZ is for availability: a standby in another zone takes over on failure. A read replica is for scaling reads and can lag behind the primary.

**Q: What does an Application Load Balancer do?**
A: It spreads HTTP/HTTPS traffic across targets, can route by path or host, terminates TLS and runs health checks so unhealthy targets stop receiving traffic.

**Q: What do you use CloudWatch for?**
A: Collecting logs and metrics, building dashboards, and setting alarms (high 5xx rate, CPU, queue depth) that notify you, for example through SNS.

**Q: EC2 vs Lambda vs ECS/Fargate?**
A: EC2 gives you full servers to manage. Lambda runs short functions with no servers but has cold starts and time limits. ECS with Fargate runs containers without managing the servers underneath.

### Monitoring, cost and secrets

**Q: Which alerts would you set for a web app?**
A: Alert on user-facing symptoms (error rate, latency, failed health checks) plus saturation (CPU, memory, disk, DB connections, queue backlog). Every alert should need an action, or it becomes noise.

**Q: What are the four golden signals?**
A: Latency, traffic, errors and saturation. Together they give a quick health picture of almost any service.

**Q: On-demand vs savings plans/reserved vs spot instances?**
A: On-demand is pay-as-you-go. Savings plans or reserved capacity give a discount for a commitment on steady workloads. Spot uses spare capacity cheaply but can be interrupted, so it suits batch jobs.

**Q: How do you right-size servers or databases?**
A: Look at real CPU, memory and connection metrics over a few weeks. If usage stays low, move to a smaller size; if it is often saturated, scale up or out, and change one thing at a time.

**Q: Where should production secrets live on AWS?**
A: In Secrets Manager or SSM Parameter Store, read at runtime by the app's IAM role. Not in the repo, the image or plain environment files.

### Deployments, rollbacks and IaC

**Q: Rolling vs blue-green vs canary deployment?**
A: Rolling replaces instances gradually. Blue-green runs a full new environment and switches traffic, so rollback is instant. Canary sends a small share of traffic to the new version first.

**Q: How do you ship a database change with zero downtime?**
A: Use expand and contract: add the new column in a backward-compatible way, deploy code that works with both shapes, backfill, and remove the old column in a later release.

**Q: What are feature flags?**
A: Runtime switches that turn code paths on or off without redeploying. They allow gradual rollouts and a fast "off" button for a bad feature.

**Q: What is Infrastructure as Code and why use it?**
A: Describing servers, networks and databases in versioned files (Terraform, CloudFormation, Pulumi). Environments become reviewable, repeatable and recoverable instead of hand-clicked.

**Q: In Terraform, what are state, `plan` and `apply`?**
A: State records what Terraform manages. `plan` previews the changes and `apply` performs them. Teams keep state in a remote backend with locking.

**Q: What is Kubernetes in a few lines?**
A: An orchestrator that runs containers across many machines. A Pod runs containers, a Deployment keeps N replicas and handles rolling updates, and a Service gives them a stable address.

## 17. System design

### Fundamentals and estimation

**Q: Latency vs throughput?**
A: Latency is how long one request takes. Throughput is how many requests the system handles per second, and improving one can hurt the other (batching raises throughput but also latency).

**Q: What does 99.9% availability mean?**
A: Roughly 8.8 hours of allowed downtime per year, or about 44 minutes per month. Each extra nine is ten times stricter and costs much more.

**Q: Back-of-envelope: how many requests per second is 1 million requests per day?**
A: About 12 per second on average (1,000,000 divided by 86,400). Design for peak, which can be 5 to 10 times the average.

**Q: Why should application servers be stateless?**
A: Any instance can serve any request, so you can add or remove instances behind a load balancer. Keep sessions and state in Redis, the database or a signed token.

**Q: L4 vs L7 load balancer?**
A: L4 balances TCP traffic by IP and port and is very fast. L7 understands HTTP, so it can route by path, host or header and terminate TLS.

**Q: Polling vs long polling vs SSE vs WebSockets?**
A: Polling asks repeatedly. Long polling holds a request open until data arrives. SSE is a one-way server-to-client stream over HTTP, and WebSockets give a two-way persistent connection (chat, games).

**Q: Synchronous vs asynchronous communication between services?**
A: Sync calls (HTTP/gRPC) are simple and immediate but tie your availability and latency to the other service. Async messaging decouples services and absorbs spikes, but results are not immediate.

### Caching

**Q: Cache-aside vs write-through vs write-behind?**
A: Cache-aside: the app reads the cache and on a miss loads from the database and fills the cache. Write-through writes cache and database together. Write-behind writes the cache first and the database later, which is fast but can lose data.

**Q: What is a cache stampede and how do you prevent it?**
A: Many requests miss at once (for example a hot key expires) and all hit the database. Use a per-key lock or single flight, add jitter to TTLs, or serve stale data while refreshing.

**Q: How do you keep a cache reasonably consistent with the database?**
A: Set a TTL, delete the key after a write instead of updating it, or publish invalidation events. Accept brief staleness unless the data must be exact.

**Q: What is the danger of caching user-specific data?**
A: If the cache key does not include the user ID, one user can receive another user's data. The same applies to a CDN caching an authenticated response.

**Q: What does a CDN cache well?**
A: Static assets such as JS, CSS, images and fonts, and sometimes public API or HTML responses. Use content-hashed file names so assets can be cached for a long time.

**Q: Besides caching, what is Redis commonly used for?**
A: Sessions, rate-limit counters, leaderboards (sorted sets), pub/sub, simple queues and distributed locks.

### Queues and async work

**Q: At-most-once vs at-least-once vs exactly-once delivery?**
A: At-most-once can lose messages, at-least-once can deliver duplicates, and true exactly-once is hard in practice. Most systems use at-least-once with idempotent consumers.

**Q: What is a dead-letter queue?**
A: A queue where messages land after failing too many retries. A poison message then does not block others, and you can inspect and replay it.

**Q: Queue vs pub/sub topic?**
A: A queue gives each message to one consumer, which shares work. Pub/sub delivers each message to every subscriber, which broadcasts events.

**Q: How do you keep messages in order?**
A: Ordering is usually guaranteed only within one partition or queue. Use a partition key such as the order or user ID so related messages go to the same place.

**Q: What is the outbox pattern?**
A: Write the business change and an "event to publish" row in the same database transaction, and let a separate worker publish it. This avoids saving data but losing the message.

**Q: Kafka vs SQS or RabbitMQ in one line?**
A: Kafka is a durable, replayable log for high-throughput event streams. SQS and RabbitMQ are classic queues for distributing tasks; check current features before comparing in detail.

### Database scaling

**Q: What problem do read replicas introduce?**
A: Replication is usually asynchronous, so a read right after a write may return old data (replication lag). Read critical or just-written data from the primary.

**Q: How do you choose a shard key?**
A: Pick a high-cardinality key with an even spread that matches your main queries, such as user ID. A bad key causes hot shards and expensive cross-shard queries.

**Q: What is consistent hashing?**
A: Keys and nodes are placed on a ring, so adding or removing a node moves only a small share of keys. With plain `hash % N`, almost every key moves.

**Q: Why do you hit "too many connections" when you scale app instances?**
A: Each instance opens its own pool, so total connections can exceed the database limit. Cap pool sizes, use a pooler such as PgBouncer and keep transactions short.

**Q: SQL or NoSQL when scale grows?**
A: Start with a relational database, which goes far with indexes, replicas and caching. Move to NoSQL for specific needs like huge write volume, flexible documents or key-value access.

### Rate limiting, retries and idempotency

**Q: Token bucket vs fixed window vs sliding window rate limiting?**
A: Fixed window counts requests per time slot (simple, but allows bursts at boundaries). Sliding window is smoother. Token bucket refills tokens at a steady rate and allows short bursts.

**Q: How do you rate limit across many app servers?**
A: Keep counters in a shared store such as Redis using atomic operations (`INCR` with expiry, or a Lua script). Key by user, API key or IP, and return 429 with a `Retry-After` header.

**Q: How do you implement an idempotency key?**
A: The client sends a unique key with the request. The server stores the key and result under a unique constraint, and a repeated request returns the stored result instead of repeating the action.

**Q: What is a retry storm and how do you avoid it?**
A: Many clients retry at the same moment and overload a recovering service. Use exponential backoff with random jitter, retry limits and a circuit breaker.

**Q: What is a circuit breaker?**
A: After repeated failures calling a dependency, it stops calling for a while and fails fast or uses a fallback, then lets a few test calls through before closing again.

**Q: Which failures are safe to retry?**
A: Timeouts, 429, 502/503/504 and network errors, as long as the operation is idempotent. Do not blindly retry 400-level client errors or non-idempotent POSTs without an idempotency key.

### Consistency and data integrity

**Q: Strong vs eventual consistency, with an example?**
A: Strong consistency means every read sees the latest write (bank balance). Eventual means replicas catch up after a delay (like counts, feeds). Choose per feature.

**Q: Two users try to buy the last item. How do you prevent overselling?**
A: Make check and decrement atomic, for example `UPDATE products SET stock = stock - 1 WHERE id = 5 AND stock > 0` and check the affected row count. Or lock the row in a transaction.

**Q: Optimistic vs pessimistic locking?**
A: Pessimistic locks the row while you work (`SELECT ... FOR UPDATE`). Optimistic checks a version number at save time and retries or returns 409 on conflict, which suits low contention.

**Q: Saga vs two-phase commit?**
A: Two-phase commit locks resources across systems and is rarely used in web apps. A saga runs local transactions in sequence and uses compensating actions (refund, release stock) when a step fails.

**Q: Why are distributed locks tricky?**
A: A lock can expire while its holder is paused or slow, so two workers both think they own it. Use leases with fencing tokens, and prefer database constraints when you can.

### Observability and operations

**Q: SLI vs SLO vs SLA?**
A: An SLI is a measurement (such as the percent of requests under 300 ms). An SLO is the internal target for it, and an SLA is the customer contract, usually with penalties.

**Q: How do you trace one request across services?**
A: Create a trace or request ID at the edge, pass it in headers (for example W3C `traceparent`), and put it in every log line. A tool such as OpenTelemetry collects the spans.

**Q: What is graceful degradation?**
A: When a dependency fails, the app keeps working with fewer features (cached data, no recommendations, no AI summary) instead of showing an error page.

**Q: Why load test before a launch?**
A: To find limits and bottlenecks (database, connection pools, memory) under realistic traffic using tools like k6 or Locust, before real users find them.

### Common designs (short outlines)

**Q: Design a URL shortener (outline).**
A: `POST /urls` creates a short code and `GET /{code}` redirects (302 if you want click analytics). Generate codes from a unique ID in base62, or random codes with a collision check, and keep `code -> long URL` under a unique index. The system is read-heavy, so cache hot codes in Redis and count clicks asynchronously through a queue.

**Q: Design a chat application (outline).**
A: Clients keep WebSocket connections to chat servers, and a pub/sub layer (Redis or Kafka) routes messages between servers. Store messages with conversation ID, sequence number and timestamp, deliver to offline users on reconnect or by push, and track presence with heartbeats.

**Q: Design a notification system (outline).**
A: An API accepts events and puts them on queues per channel (email, SMS, push). Workers apply user preferences, templates, dedupe and rate limits, call the provider, retry with backoff, send failures to a dead-letter queue and record delivery status.

**Q: Design a file upload service (outline).**
A: The client asks the API for a presigned URL (after auth, size and type checks) and uploads straight to object storage, using multipart for large files. A storage event triggers a queue for virus scan and processing, metadata and status go in the database, and downloads use presigned URLs or a CDN.

**Q: Design the checkout flow of an e-commerce site (outline).**
A: Create the order as pending with an idempotency key, reserve stock atomically with an expiry, then start payment. A verified, idempotent payment webhook moves the order to paid, while failure or timeout releases the stock (a saga). Use an order state machine and an outbox for emails and fulfilment events.

**Q: Design a news feed (outline).**
A: Fan-out on write precomputes each follower's feed when someone posts (fast reads, heavy for users with millions of followers). Fan-out on read builds the feed at request time (cheap writes, slower reads). Real systems mix both.

**Q: Design a multi-tenant RAG document assistant (outline).**
A: Ingest through a queue: parse, chunk, embed, and store vectors with tenant ID, document ID and a content hash. Always filter by tenant and permissions inside the retrieval query, re-embed only changed documents, delete vectors when a document is removed, and track cost and retrieval quality per tenant.

**Q: Design an LLM gateway for several teams (outline).**
A: A service in front of the model providers that handles auth, per-team budgets and rate limits, logging, response caching, retries and fallback to another model. Apps never hold provider keys, and you get one place to track cost and latency.

## 18. Data structures and algorithms (realistic scope)

### Big-O and complexity traps

**Q: Complexity of `Set.has` or a dict lookup vs `array.includes` or `x in list`?**
A: Hash lookups are O(1) on average. Searching an unsorted array or list is O(n).

**Q: What is wrong with `for i in range(n): for j in range(n): if a[i] + a[j] == t`?**
A: It is O(n²) and it can pair an element with itself (`i == j`). Use a hash map for O(n), or sort and use two pointers.

**Q: What is wrong with `result = [...result, x]` inside a loop?**
A: Each spread copies the whole array, so the loop becomes O(n²). Use `result.push(x)` for O(n) overall.

**Q: What is amortized O(1)?**
A: Appending to a dynamic array is usually O(1), with an occasional O(n) resize. Averaged over many appends, each one is O(1).

**Q: What does `[10, 9, 1].sort()` return in JavaScript?**
A: `[1, 10, 9]`. The default sort compares items as strings, so use `sort((a, b) => a - b)` for numbers.

**Q: Best, average and worst case of quicksort?**
A: Average O(n log n), worst O(n²) with consistently bad pivots. Merge sort is O(n log n) in every case but needs O(n) extra space.

### Arrays and strings

**Q: How do you check if a string is a palindrome?**
A: Use two pointers from both ends moving inward, comparing characters (skip non-alphanumerics if asked). O(n) time, O(1) space.

**Q: How do you check if two strings are anagrams?**
A: Count characters of both with a map or array and compare the counts. O(n), or O(n log n) if you sort both.

**Q: Rotate an array by k positions.**
A: Reverse the whole array, then reverse the first `k % n` items and the remaining items. O(n) time, O(1) space.

**Q: Move all zeroes to the end, keeping the order of other items.**
A: Keep a write pointer, copy each non-zero value forward, then fill the rest with zeroes. O(n), in place.

**Q: Maximum subarray sum (Kadane).**
A: Keep the best sum ending at the current item with `cur = max(x, cur + x)` and track the overall maximum. O(n).

**Q: Merge overlapping intervals.**
A: Sort by start, then extend the last merged interval whenever the next one starts before it ends. O(n log n).

### Hash maps and sets

**Q: Two Sum.**
A: Loop once and store `value -> index` in a map. For each item check whether `target - value` is already there. O(n) time and space.

**Q: Group anagrams.**
A: Use the sorted letters (or a 26-count tuple) as a map key and collect words under it. O(n * k log k) for n words of length k.

**Q: Longest consecutive sequence in an unsorted array.**
A: Put numbers in a set and only start counting from numbers whose predecessor `x - 1` is missing, then walk forward. O(n).

**Q: Count subarrays whose sum equals k.**
A: Keep a running prefix sum and a map of how often each prefix appeared. For each position add the count of `prefix - k`. O(n).

**Q: Top K frequent elements.**
A: Count with a map, then keep a min-heap of size k (O(n log k)) or use bucket sort by frequency (O(n)).

**Q: How does a hash map handle collisions?**
A: Chaining keeps a small list in each bucket, and open addressing probes for another free slot. A good hash function and resizing keep operations close to O(1).

### Two pointers and sliding window

**Q: Two Sum on a sorted array.**
A: Put pointers at both ends. If the sum is too small move the left one up, if too big move the right one down. O(n) time, O(1) space.

**Q: 3Sum.**
A: Sort, fix one number, then use two pointers on the rest, skipping duplicate values. O(n²).

**Q: Container with most water.**
A: Start with pointers at both ends, compute the area, then move the pointer at the shorter line inward. O(n).

**Q: Longest substring without repeating characters.**
A: Sliding window with a set or a map of last-seen indexes. When a repeat appears, move the left edge past it. O(n).

**Q: Maximum sum of k consecutive items.**
A: Compute the first window sum, then slide: add the new item and subtract the one leaving. O(n).

**Q: Minimum window substring.**
A: Expand the right edge until the window has all needed characters, then shrink from the left while it stays valid, tracking the smallest window. O(n).

### Stacks and queues

**Q: Valid parentheses.**
A: Push opening brackets and, on a closing bracket, pop and check that it matches. The string is valid only if the stack is empty at the end (O(n)).

**Q: Design a stack that returns the minimum in O(1).**
A: Keep a second stack (or store pairs) holding the minimum at each level, so `getMin` reads the top.

**Q: Implement a queue using two stacks.**
A: Push onto an input stack. To pop, if the output stack is empty move everything from the input stack over, which reverses the order. Amortized O(1).

**Q: Daily temperatures or next greater element.**
A: Use a monotonic stack of indexes. While the current value is greater than the value at the top, pop and record the answer for that index. O(n).

**Q: Why use `collections.deque` instead of a list for a queue in Python?**
A: `list.pop(0)` is O(n) while `deque.popleft()` is O(1). Use a deque for BFS and queues.

### Linked lists

**Q: Reverse a linked list.**
A: Walk the list with `prev`, `curr` and `next` pointers, pointing `curr.next` back to `prev` at each step. O(n) time, O(1) space.

**Q: Detect a cycle in a linked list.**
A: Floyd's method: a slow pointer moves one step and a fast pointer moves two. If they ever meet, there is a cycle.

**Q: Find the middle of a linked list.**
A: Use slow and fast pointers. When the fast one reaches the end, the slow one is at the middle.

**Q: Merge two sorted linked lists.**
A: Use a dummy head and a tail pointer, and keep attaching the smaller of the two current nodes. O(n + m).

**Q: Array vs linked list trade-offs?**
A: Arrays give O(1) index access and cache-friendly memory. Linked lists give O(1) insert or delete at a known node, but O(n) search and extra memory for pointers.

### Trees and graphs

**Q: What does an inorder traversal of a BST give?**
A: The values in sorted order (left, node, right).

**Q: Maximum depth of a binary tree.**
A: Recurse: `1 + max(depth(left), depth(right))`, returning 0 for an empty node. O(n).

**Q: Level-order traversal of a binary tree.**
A: BFS with a queue, processing one level's worth of nodes (the current queue size) at a time.

**Q: Validate a binary search tree.**
A: Pass down allowed (min, max) bounds for each node, or check that an inorder walk is strictly increasing. Comparing only with direct children is wrong.

**Q: Lowest common ancestor.**
A: In a BST, go left or right depending on where both values lie. In a general tree, recurse and return the node where both sides report a find. O(h) for a BST, O(n) otherwise.

**Q: Number of islands in a grid.**
A: Scan the grid, and for each unvisited land cell run DFS or BFS to mark connected land, counting each start. O(rows * cols).

**Q: Can all courses be finished given prerequisites?**
A: Model it as a directed graph. It is possible only if there is no cycle, which you detect with DFS state marking or Kahn's topological sort.

### Heaps, sorting and searching

**Q: Kth largest element in an array.**
A: Keep a min-heap of size k. The top is the answer, in O(n log k). Quickselect gives O(n) on average.

**Q: Merge k sorted lists.**
A: Put the head of each list in a min-heap, pop the smallest, and push that list's next node. O(N log k) for N total items.

**Q: Heap basics and Python's `heapq`?**
A: `heapq` is a min-heap (negate values for a max-heap). Push and pop are O(log n), peek is O(1) and `heapify` is O(n).

**Q: What are Python's and JavaScript's built-in sorts like?**
A: Both run in O(n log n) and are stable, meaning equal items keep their original order (Python uses Timsort; JavaScript's sort has been required to be stable since ES2019).

**Q: What are common binary search bugs?**
A: Off-by-one errors and infinite loops. Pick one convention (such as `lo <= hi` with `mid + 1` and `mid - 1`) and use it consistently, and compute `mid = lo + (hi - lo) // 2` to avoid overflow in fixed-width languages.

**Q: Search in a rotated sorted array.**
A: Use binary search. At each step one half is sorted, so check whether the target lies in it and discard the other half. O(log n).

### Recursion, backtracking and DP

**Q: What does recursion need to work, and what goes wrong without it?**
A: A base case and progress toward it. Without them you get infinite recursion and a stack overflow, and even correct deep recursion costs O(depth) stack space.

**Q: Complexity of naive recursive Fibonacci, and the fix?**
A: O(2^n), because the same subproblems are recomputed. Memoization or a bottom-up loop makes it O(n).

**Q: How do you recognise a DP problem, and memoization vs tabulation?**
A: Look for overlapping subproblems and optimal substructure. Memoization caches recursive results top-down, while tabulation fills a table bottom-up with loops.

**Q: Climbing stairs (1 or 2 steps at a time).**
A: `ways(n) = ways(n - 1) + ways(n - 2)`, the Fibonacci recurrence. Keep two variables for O(1) space.

**Q: Coin change (fewest coins for an amount).**
A: `dp[a] = min(dp[a - coin] + 1)` over all coins, with `dp[0] = 0`. O(amount * coins). Greedy fails for some coin sets.

**Q: Generate all subsets of an array.**
A: Backtracking: at each index choose to include or skip the item, recurse, then undo the choice. There are 2^n subsets.

### Interview approach

**Q: What steps do you follow in a coding interview?**
A: Restate the problem, ask about inputs and limits, give a brute-force idea, improve it, state time and space complexity, then code and test with examples.

**Q: Which edge cases do you always test?**
A: Empty input, a single element, duplicates, negative numbers, all-equal values and very large inputs.

**Q: What do you do when you are stuck?**
A: Think aloud, work a small example by hand, look for a pattern (sorting, hash map, two pointers, stack), and ask for a hint instead of going silent.

## 19. Behavioural and project questions

### Introducing yourself

**Q: How do you answer "Tell me about yourself"?**
A: Give a 60 to 90 second story: your current role and strengths, one or two relevant projects or results, and why this role fits. Do not recite your CV or life history.

**Q: Why should we hire you?**
A: Match their needs with your strengths, back it with one proof (a project or result), and show that you learn fast and own your work.

**Q: What is your biggest weakness?**
A: Name a real, minor weakness you are actively fixing (for example over-engineering early) and the steps you take. Avoid fake answers like "I work too hard".

**Q: Where do you see yourself in five years?**
A: Show growth toward deeper technical ownership, such as designing systems and mentoring, in a way that fits the role and doesn't sound like you will leave soon.

**Q: You are a fresher or career switcher. How do you prove you can do the job?**
A: Show real projects: a deployed link, a repo with a README and tests, one trade-off and one failure. Explain what you built end to end, not which tutorials you finished.

### STAR stories, failure and feedback

**Q: What is the STAR method and how long should an answer be?**
A: Situation, Task, Action, Result. Spend most time on what you did, end with a measurable result and a lesson, and aim for about two minutes.

**Q: How many stories should you prepare?**
A: Five or six real ones (conflict, failure, ownership, tight deadline, learning, helping someone) that you can adapt to different questions.

**Q: Tell me about a time you failed or made a mistake.**
A: Pick a real mistake with limited damage, own it without blaming others, explain the fix, and describe the process change (test, alert, review) that prevents a repeat.

**Q: Tell me about a time you missed a deadline.**
A: Explain the cause honestly, how early you raised the risk, what you cut or renegotiated, and what you changed in your estimates afterwards.

**Q: How do you respond to critical feedback?**
A: Listen without defending, ask for a specific example, act on it and follow up. Have one real example where feedback changed how you work.

### Teamwork, conflict and ownership

**Q: How do you handle a teammate who is not delivering their part?**
A: Talk to them privately first to understand blockers and offer help, make expectations clear, and involve the lead only if delivery is still at risk.

**Q: Describe a time you took ownership beyond your assigned task.**
A: Use a real example such as fixing a flaky pipeline, writing missing docs or spotting a production issue. Show how you aligned with the team and what changed.

**Q: How do you handle unclear or changing requirements?**
A: Ask clarifying questions, write down assumptions, build a small first version for early feedback, and confirm changes in writing.

**Q: How do you work under a tight deadline?**
A: Prioritise the must-have scope, say what can be cut or delayed, raise risks early, and don't skip tests on risky parts.

**Q: When do you ask for help instead of continuing alone?**
A: After a time-boxed attempt (say 30 to 60 minutes). Bring what you tried and the exact error, and ask a clear question. Never stay silently stuck.

**Q: When do you escalate a problem to your manager?**
A: When it threatens the deadline, security or quality, needs a decision above my authority, or stays blocked after my attempts. I bring the problem with options and a recommendation.

### Estimation, planning and code review

**Q: How do you estimate a task?**
A: Break it into small pieces, include testing, review, deployment and unknowns, give a range, and compare with similar past work. Update the estimate when you learn more.

**Q: Your estimate was wrong and you will be late. What do you do?**
A: Tell the team as soon as you know, explain why, offer options (cut scope, more time, extra help), and apply the lesson to future estimates.

**Q: What do you look for in a code review?**
A: Correctness and edge cases, readability, tests, security (validation, secrets), performance red flags and consistency with the codebase. Comment on the code, not the person.

**Q: How do you handle a harsh or disagreeing review comment on your PR?**
A: Assume good intent, ask what they mean, explain your reasoning with evidence, and change the code if they are right. If it stays unresolved, involve a lead.

**Q: What makes a good pull request?**
A: It is small and focused, has a clear description (why and how to test), passes CI, includes screenshots for UI changes and contains no unrelated edits.

### Working with AI tools

**Q: How do you review code that an AI tool generated?**
A: Treat it like code from a junior developer. Check it solves the real requirement, test edge cases, review security and new dependencies, run the tests, and make sure I can explain every line.

**Q: The interviewer asks, "Did you build this project yourself or with AI?"**
A: Answer honestly: say what AI helped with and what you designed, decided and debugged yourself. Then prove it by explaining the architecture and one trade-off.

**Q: When would you avoid using AI tools?**
A: When company policy forbids sending that code or data, for security-critical logic I cannot verify, and when I am learning a concept for the first time and need to understand it myself.

**Q: How do you avoid leaking sensitive data into AI tools?**
A: Never paste secrets, customer data or proprietary code into unapproved tools. Use company-approved tools, redact examples and follow the data policy.

### HR, salary and joining questions

**Q: What is your notice period, and can it be reduced?**
A: State it honestly (often 30 to 90 days). Say whether it is negotiable or can be bought out, but promise only what your contract and employer allow.

**Q: What is your current CTC and your expected CTC?**
A: Be truthful about the current CTC, since payslips and background verification can confirm it, and explain fixed vs variable. For expected CTC, research the market for the role and city, give a reasoned range and stay open to discussing the whole package.

**Q: Why are you leaving your current company?**
A: Give a positive, forward-looking reason such as learning, scope or growth (for example moving into AI engineering). Do not criticise your employer or manager.

**Q: Are you willing to relocate or work from office?**
A: Answer clearly, including any constraints such as preferred cities or timeline. Check the remote, hybrid and relocation policy in writing.

**Q: How do you handle multiple offers or a counter-offer from your current company?**
A: Be transparent and polite, and compare growth, learning, team, stability and total compensation, not only the salary. If you take a counter-offer, ask yourself why you wanted to leave.

**Q: How do you explain a gap in your resume or a short stint?**
A: Be honest and brief about the reason, and show what you did meanwhile (learning, projects, freelancing). Keep dates accurate, because background verification checks them.

**Q: What do you check in an offer letter before accepting?**
A: The CTC breakup (fixed, variable, bonuses), probation and notice period, any bond, service agreement or clawback, work location and policy, role title and joining date. Ask questions before you sign.

**Q: Why do you want to join our company?**
A: Show you researched their product, tech stack and recent news, and connect them to your skills and what you want to learn. Avoid generic answers like "good company".

### Questions to ask the interviewer

**Q: What good questions can you ask the interviewer?**
A: What the first 90 days look like, how the team does code review, testing and deployment, what the biggest technical challenge is, and how success is measured for this role.

**Q: What should you avoid asking in the first interview round?**
A: Do not lead with salary, leave or work-from-home details. Save those for HR or the offer stage, and focus first on the work and the team.

**Q: How do you close an interview well?**
A: Ask about next steps and timeline, and ask "Do you have any concerns about my profile that I can address?" Then thank them briefly.

**Q: What can you ask in an AI engineer interview?**
A: How they evaluate LLM features, who owns prompts and versions them, how they monitor cost and quality, and how they handle data privacy and human review.

## 20. Scenario and debugging questions

### Slow pages and APIs

**Q: Users say "the page is slow". What do you do?**
A: Measure first to see if the delay is network, server or browser, using DevTools, Lighthouse and server latency metrics. Then fix the biggest piece (large images or JS, a slow API or query, too many re-renders) and measure again after each change.

**Q: An API endpoint became slow after a release.**
A: Compare latency before and after in metrics and diff the release. Look for new N+1 queries, missing indexes, extra external calls or bigger payloads, confirm with tracing or `EXPLAIN ANALYZE`, and roll back if users are hurt.

**Q: An endpoint is slow only for a few users.**
A: Find what is different about them: data volume, region, plan or a feature flag. Reproduce with their data, check the query plan, and look for missing pagination or limits.

**Q: The product list is fast locally but slow with real data.**
A: Suspect missing pagination, missing indexes, N+1 queries or loading too many rows and images. Add limits, indexes and joins or batching, and test with production-sized data.

**Q: A React page lags while typing in a search box.**
A: Profile with React DevTools. Usual causes are state kept too high in the tree, a big list re-rendering on each keystroke and heavy work during render. Move state down, debounce, memoize or virtualize the list, or use `useDeferredValue`.

**Q: Lighthouse shows a poor LCP on mobile.**
A: Identify the LCP element (often the hero image or heading). Optimise or preload it, use `next/image` with correct sizes, remove render-blocking JS and CSS, improve server response time and use a CDN.

### Errors that appear only in production

**Q: An API returns 500 only in production.**
A: Read the production logs and error tracker for the stack trace and request ID. Then compare config: environment variables, secrets, database schema, data and versions. Reproduce in staging with similar data, fix it and add a test and an alert.

**Q: A CORS error appears only after deployment.**
A: The production origin is probably missing from the server's allowed origins, or a proxy or redirect drops the headers, or the preflight `OPTIONS` request fails. Inspect the response headers in DevTools and fix the server config.

**Q: Users get 502 Bad Gateway right after a deploy.**
A: The proxy cannot get a valid response from the app. Check whether the app crashed or failed to start (logs, wrong port, missing env var), look at health checks and restarts, and roll back if needed.

**Q: Users see intermittent 504 timeouts.**
A: Something is slower than the proxy timeout. Look for slow queries, a saturated pool or database, and slow third-party calls. Add timeouts and move long work to a queue; raise the proxy timeout only after fixing the cause.

**Q: Login works locally but users are logged out in production.**
A: Check cookie flags (`Secure`, `SameSite`, domain, path), HTTPS behind a proxy (`trust proxy`, `X-Forwarded-Proto`), an in-memory session store with several instances, and different secrets between instances.

**Q: Uploading a large file fails with 413 only in production.**
A: A proxy or platform limit is rejecting the body (for example Nginx `client_max_body_size`, or a serverless payload limit). Raise it carefully, or better, upload directly to object storage with presigned URLs.

**Q: A Next.js environment variable is undefined in the browser.**
A: Browser code only sees variables prefixed with `NEXT_PUBLIC_`, and they are inlined at build time, so a change needs a rebuild. Never put secrets in them.

**Q: After a deploy, some users still see the old version.**
A: Something cached old files: the CDN or browser cached the HTML, a service worker serves old assets, or the rollout has not reached all instances. Use hashed asset names, short cache for HTML, purge the CDN and verify the rollout.

### CPU, memory, disk and connection problems

**Q: Server memory keeps growing.**
A: Confirm it on a memory graph, then take heap snapshots or profiles at two times and compare. Typical causes are unbounded caches or maps, listeners never removed and large buffers. Fix it, add limits and set an alert.

**Q: Server CPU is at 100 percent.**
A: Find the process and hot code with `top` and a profiler or flame graph. Typical causes are expensive loops, regex backtracking, huge JSON work, no caching or a traffic spike. Fix the code, cache, rate limit or scale out.

**Q: Database CPU is at 100 percent.**
A: Find the top queries (slow query log, `pg_stat_statements` or your cloud's database insights), run `EXPLAIN ANALYZE` and add missing indexes. Fix N+1 and full scans, cache, and kill runaway queries; scale up only after tuning.

**Q: The app fails with "too many connections" to the database.**
A: Pool size times instance count exceeds the database limit, or connections leak. Cap pools per instance, use a pooler such as PgBouncer, make sure connections are released and keep transactions short.

**Q: The server disk is full.**
A: Use `df -h` and `du -sh` to find the big folders. Usual culprits are logs, Docker images and volumes, and temp or uploaded files. Clean up carefully, set log rotation and alert at about 80 percent.

**Q: FastAPI endpoints hang under load.**
A: A blocking call (sync DB driver, `requests`, `time.sleep`) inside an `async def` route blocks the event loop. Use async libraries or plain `def` routes, add timeouts, and check worker count and pool size.

**Q: The job queue backlog keeps growing.**
A: Consumers are slower than producers or failing. Check worker health, error and retry rates, poison messages and slow dependencies, then fix the failing job, scale workers, use a dead-letter queue and apply backpressure.

**Q: A container keeps restarting.**
A: Check `docker logs` and the exit code. Common causes are a startup crash (missing env var, bad config, no DB connection), an OOM kill (137) or a failing health check. Fix the cause instead of raising restart limits.

### Data bugs and consistency

**Q: Customers were charged twice.**
A: Likely a retry, double click or webhook processed twice without idempotency. Refund the affected customers using payment provider records, then add idempotency keys, a unique constraint, a disabled submit button and webhook dedupe by event ID.

**Q: Users see stale data after an update.**
A: Find which layer is stale: browser cache, CDN, application cache or a read replica. Invalidate after writes, fix TTLs and cache keys, and read from the primary when read-after-write matters.

**Q: One user can see another user's data.**
A: Treat it as a security incident. Common causes are a cache key without a user ID, a CDN caching an authenticated response, a global variable shared across requests and a missing owner check. Stop the leak, find who was affected, fix it and notify as required.

**Q: A migration locked a table and the site froze.**
A: A long DDL or backfill blocked other queries. Cancel it if safe, then redo it in small steps: add a nullable column, backfill in batches, create indexes concurrently (`CREATE INDEX CONCURRENTLY` in Postgres) and run it at low traffic.

**Q: Someone deleted production data by mistake.**
A: Stop further damage and assess scope. Restore from backup or point-in-time recovery into a separate database and copy back only what is needed. Afterwards tighten access, add soft deletes and test restores regularly.

**Q: Two admins overwrote each other's edits.**
A: This is a lost update. Use optimistic locking (a version or `updated_at` check) and return 409 on conflict, or lock the row, and show the user a clear refresh or merge message.

### Security incidents

**Q: You suspect user data was leaked. What do you do?**
A: Contain first (revoke exposed keys and sessions, close the hole) and preserve logs. Then find out what data and which users were affected, fix the root cause, notify as required by law and policy with the security and legal teams, and write a postmortem.

**Q: AWS keys were exposed on GitHub and the bill spiked.**
A: Deactivate and rotate the keys immediately, check CloudTrail for what was done, and terminate unknown resources. Contact AWS support if needed, then move to IAM roles, secret scanning and budget alerts.

**Q: You see a surge of failed logins from many IPs.**
A: This looks like credential stuffing. Rate limit by account and IP, add CAPTCHA or MFA, slow or lock after repeated failures, block bad sources at the WAF, and prompt affected users to reset passwords.

**Q: A critical vulnerability is announced in a dependency you use.**
A: Check whether your version and usage are affected, upgrade or patch, run the tests and deploy quickly. If there is no fix yet, mitigate (disable the feature, add a WAF rule), and set up Dependabot or `npm audit` in CI.

**Q: You discover an S3 bucket is public.**
A: Turn on Block Public Access right away, review access logs to see what was exposed, and rotate any secrets stored there. Then serve files through presigned URLs or CloudFront and alert on public buckets.

### LLM and RAG problems

**Q: LLM answers got worse after a prompt change.**
A: Roll back to the previous prompt version, then run both versions on a saved eval set to see which cases regressed. Make targeted fixes and never ship prompt changes without running the evals.

**Q: LLM costs doubled this week.**
A: Break usage down by feature, user, model and day. Look for more traffic, longer prompts or history, retry or agent loops, or a model change, then trim context, cache, use a smaller model, set token limits and add per-user budgets and alerts.

**Q: RAG answers are wrong or off-topic.**
A: Debug retrieval before generation: log the retrieved chunks for failing questions. If chunks are wrong, fix chunking, embeddings, metadata filters, hybrid search or reranking; if chunks are right, fix the prompt and require citations.

**Q: The chatbot invents a refund policy that does not exist.**
A: Ground answers in retrieved policy text, require citations, and answer "I don't know" when retrieval is weak. Add eval cases for known policy questions and route high-risk topics to a human.

**Q: An agent loops and burns tokens.**
A: Add step, time and cost budgets, detect repeated identical tool calls, and improve tool descriptions and error messages. Trace the run to see where it loops and hand off to a human when it is stuck.

**Q: The LLM sometimes returns invalid JSON.**
A: Use the provider's structured-output or JSON-schema feature and validate with Pydantic or Zod. Retry once with the validation error, fall back gracefully and log failures to find prompt problems.

**Q: The AI feature feels too slow.**
A: Measure where the time goes (retrieval, model, tool calls). Stream the response, use a smaller or faster model, trim context, run independent calls in parallel, cache, and move non-urgent work to the background.

**Q: An uploaded document contains hidden instructions that change the bot's behaviour.**
A: This is prompt injection. Treat retrieved text as untrusted data kept separate from instructions, limit tool permissions, require approval for risky actions, log suspicious content and add adversarial test cases.

**Q: Users see snippets from other users' documents in answers.**
A: This is an access-control bug in retrieval. Disable or restrict the feature, enforce the owner or tenant filter inside the vector query, check caches and logs for exposure, and add tests with two tenants before re-enabling.

**Q: The model provider returns 429 or errors during peak traffic.**
A: Add retries with backoff and jitter, queue non-urgent requests, rate limit users, cache repeated answers and fall back to another model. Also ask the provider for higher limits.

### Deployments and incident handling

**Q: A deploy broke production. What do you do first?**
A: Restore service first by rolling back or switching off the feature flag, and tell stakeholders the status. Investigate afterwards with logs and the diff, fix forward with a test, and write a blameless postmortem.

**Q: CI is flaky or tests pass locally but fail in CI.**
A: Compare environments: versions, timezone, env vars, test order and parallelism. For flaky tests look for shared state, fixed sleeps and network calls, then fix or quarantine them instead of just re-running.

**Q: The SSL certificate expired and users see warnings.**
A: Renew or replace the certificate immediately and reload the server. Then fix automatic renewal and add expiry monitoring that alerts well before the date.

**Q: The site is down. Walk me through your first 15 minutes.**
A: Confirm the scope, declare an incident and check recent deploys and dashboards (errors, latency, health checks). Roll back if a deploy is the suspect, check dependencies (database, DNS, cloud status), post regular updates and keep a timeline.

**Q: What goes into a blameless postmortem?**
A: Timeline, impact, root cause, what went well and what did not, and action items with owners and dates. Focus on fixing systems and processes, not blaming people.
