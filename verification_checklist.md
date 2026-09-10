# Mandatory Verification Checklist for AI-Generated Code

### 1. Invariants & Off-by-One Boundaries
* [ ] Zero, empty, and single-item inputs tested.
* [ ] Boundary operators (`<` vs `<=`, slice endpoints) mathematically inspected.
* [ ] Array indexing checked against index out of bounds.

### 2. Concurrency, Race Conditions & Locks
* [ ] Does the code share mutable state across processes or pods?
* [ ] Is lock acquisition strictly ordered to prevent deadlocks?
* [ ] Are distributed locks used instead of local in-memory mutexes where appropriate?

### 3. Resource Lifetime & Leaks
* [ ] Are all database connections, sockets, and file descriptors managed via `with` context managers?
* [ ] Are event listeners, callbacks, and subscriptions unregistered upon teardown?

### 4. Security & Authentication
* [ ] Are cryptographic nonces, salts, and tokens generated with `secrets` (not `random`)?
* [ ] Are CSRF `state` tokens validated using constant-time string comparison (`compare_digest`)?
* [ ] Are SQL queries strictly parameterized?

### 5. Reviewer Ownership Rule
* [ ] Can the engineer explain every line to a senior architect without citing "the AI wrote it"?
