# Step 7 — Config, Auth & Migrations

> **Goal:** take the working-but-naive backend to *production shape* — get secrets out of the
> source, put a real authentication wall in front of the API, and gain the ability to evolve the
> database schema without losing data. Plus the mindset (strangler-fig) for evolving real systems.
>
> *(This is the merged Step 7 + 8 — one "make it production-ready" arc, built in four parts.)*

---

## Part A — Configuration: code vs. config

Values were hard-coded in the source (`create_engine("sqlite:///database.db")`, the CORS origin).
That breaks the moment the app runs anywhere but your laptop — and it turns fatal once a **secret**
(the JWT signing key) enters the picture: a secret in the source is a secret in **git**.

**The split:** *code* is identical everywhere; anything that **changes per environment** *or* is a
**secret** lives in the **environment**, and the app reads it at startup.

```
   CODE  (in git, identical everywhere)      CONFIG  (per-environment, NEVER in git)
   routes · models · logic          ──reads──►   DATABASE_URL · SECRET_KEY · ...
                                                  (env vars, or a gitignored .env file)
```

**`pydantic-settings`** = Pydantic pointed at the environment. Declare typed fields; it fills them
from env vars / `.env`, validates, and **fails loudly at startup** if a required one is missing.

```python
# config.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str                                # required — no default → crash if missing
    frontend_origin: str = "http://localhost:5173"   # safe dev default
    secret_key: str                                  # required (a secret!)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()                                # built once; imported everywhere
```

- **Required vs optional = default or no default.** Secrets and prod-critical values get *no*
  default (force an explicit choice; fail fast). Safe dev values get one.
- **`.env` is gitignored** — the secret never gets committed. Generate a real key with
  `openssl rand -hex 32` (32 bytes of randomness; must be unguessable).
- **Fail-fast is a feature:** a missing `SECRET_KEY` crashing at boot beats silently signing tokens
  with an empty key.

---

## Part B — Authentication

Two independent problems: **store passwords safely**, and **prove identity on every request.**

### ① Password hashing (`pwdlib` + Argon2)

Never store the plaintext password. Store a **one-way hash**; at login, hash what they typed and
compare.

- **Salt:** each hash mixes in a random value, so the *same* password yields a *different* hash every
  time. That defeats precomputed "hash → password" tables (rainbow tables) and hides which users
  share a password. `pwdlib` stores the salt *inside* the `$argon2id$…` string, so `verify` re-reads
  it.
- **Argon2** is deliberately *slow* — brute-forcing each hash individually is expensive.

```python
password_hash = PasswordHash.recommended()
h = password_hash.hash("hunter2")          # $argon2id$v=19$m=...
password_hash.verify("hunter2", h)          # True   (wrong password → False)
```

### The three-model split

A user's password wears three hats — so three models keep them apart:

```
  CLIENT sends        SERVER stores          SERVER returns
  UserCreate          User (table)           UserPublic
  username            id                     id
  password ──hash──►  hashed_password        username
                      username               (NO password field → can't leak)
```

The **response model** (`UserPublic`) is a leak-proof gate: even though `User` holds the hash,
returning `UserPublic` guarantees it never reaches the client.

### ② Proving identity: JWT

HTTP is **stateless** — the server doesn't remember you between requests. So login hands back a
**signed token** the client sends on every later request.

```
  1. POST /token   (username + password)  ──►  verify vs. the stored hash, then sign a JWT
  2. ◄── the token
  3. GET /users/me   Authorization: Bearer <token>  ──►  verify signature + expiry, load user
  4. ◄── the data  (only if the signature checks out)
```

A **JWT** is three base64 parts: `header.payload.signature`.
- It is **signed, not encrypted** — anyone can *read* the payload (`{"sub": "alice"}`); the signature
  (keyed by `SECRET_KEY`) stops anyone *altering* it. Change one byte → signature fails → rejected.
- **Bearer token:** whoever holds a valid token *is* that user — so use **HTTPS** (no sniffing) and a
  short **expiry** (a stolen token dies fast).
- The signature turns *"I claim to be user 1"* into *"I can prove I'm user 1."*

### The login endpoint & the guard

- **`POST /token`** uses `OAuth2PasswordRequestForm` (the OAuth2 standard — *form* data, not JSON;
  makes `/docs`' **Authorize** button work). Look up by *username*, `verify_password`, and on success
  `create_access_token({"sub": username})`. Bad user *or* bad password → the **same** vague `401`
  (never leak which usernames exist).
- **`get_current_user`** is a dependency that extracts the bearer token, `jwt.decode`s it (verifying
  signature *and* expiry), and loads the user — or `401`. Wrapped as
  `CurrentUserDep = Annotated[User, Depends(get_current_user)]`, **protecting a route is one
  parameter:**

```python
@router.get("/users/me")
def read_current_user(current_user: CurrentUserDep) -> UserPublic:
    return current_user
```

That's the **dependency-injection payoff from Step 6**: the "vending machine" now dispenses *the
authenticated user*, and 401s automatically — without one line of token-parsing in the endpoint.

---

## Part C — Migrations (Alembic)

`create_all` has exactly one power: **create missing tables.** It is blind to *changes* in tables
that already exist — add a column and it silently does nothing. Without migrations your only escapes
are both bad: drop-and-recreate (lose data) or hand-written `ALTER TABLE`.

**A migration = one versioned, reversible schema change** — an `upgrade()` and a `downgrade()`,
numbered and chained into a history. *Git for your schema.*

```
   MODELS (Python)          MIGRATIONS (history)          DATABASE (real tables)
   what it SHOULD be   ─autogenerate─►  0002_add_phone  ─upgrade─►  contact GAINS phone
                                        0001_initial                (existing rows kept!)
```

**Alembic** (by the SQLAlchemy author) can **autogenerate** a migration by diffing your *models*
against the *database*. The wiring lives in `alembic/env.py`:

- `target_metadata = SQLModel.metadata` (+ import your models so they register — else Alembic thinks
  every table should be *dropped*).
- `config.set_main_option("sqlalchemy.url", settings.database_url)` — same DB as the app, from `.env`.
- `render_as_batch=True` — **critical for SQLite**: it can't `ALTER TABLE` in place, so Alembic does
  make-new-table → copy → swap ("batch mode").
- `user_module_prefix="sqlmodel.sql.sqltypes."` + `import sqlmodel.sql.sqltypes` in `script.py.mako`
  — so generated migrations can reference SQLModel's column types (`AutoString`) without a `NameError`.

**The workflow:**
```bash
uv run alembic revision --autogenerate -m "add phone to contact"   # write the migration
#   → ALWAYS read the generated file before applying
uv run alembic upgrade head                                         # apply it
uv run alembic current                                              # where is this DB?
```

- Each migration records its **parent** (`down_revision`) — a linked list, like git commits. The
  first migration has `down_revision = None`.
- Autogenerate produced a clean **`add_column`** (not a drop/recreate), `nullable=True` because the
  field was `str | None` — so existing rows survived and took `NULL`. **A schema change with zero data
  loss** — the exact thing `create_all` never could do.
- **Always review** an autogenerated migration: it detects most changes but can't tell a *rename* from
  a drop-and-add.
- **Adopting on a populated DB:** ours held only throwaway seed data, so we wiped it and let the
  initial autogenerate capture the full schema. On a real DB you can't wipe — you'd `alembic stamp` it
  as already-at-a-revision instead. *Caveat:* `stamp` only tells Alembic "this DB is at revision X" —
  it's valid **only if the DB's actual schema matches** that revision. A DB that's *between* revisions
  (e.g. this tutorial's own steps-4–6 `database.db`: has `contact`/`note` but no `user` table) matches
  none of them; there you either write a bridging migration or, for throwaway data, just delete the file.

> The philosophy switch: `create_all` and Alembic are two ways to manage schema — *"snap to the models
> now"* vs *"apply an ordered history."* Adopting Alembic means **retiring `create_all`** (we removed
> the startup call). New rule: run `alembic upgrade head` *before* the app.

---

## Part D — The Strangler-Fig pattern (concept)

How you evolve a *real* legacy system. The tempting **big-bang rewrite** — "rebuild it all, then flip
the switch" — reliably fails: a long dark period shipping nothing, then an all-or-nothing cutover you
can't half-roll-back.

**Strangler-fig** (named after the tree that grows around a host until it stands alone): put a
**facade** in front, then replace the old system one piece at a time.

```
  STAGE 1              STAGE 2                       STAGE 3
  facade → OLD         facade → OLD (most)           facade → NEW (all)
                              └─► NEW (/contacts)     (OLD deleted)
  100% legacy          migrate one route at a time    100% new
```

Each migrated piece ships today and is **reversible** (route back to the old one if it breaks). The
old system shrinks until it's fully "strangled" and you delete it.

You've already lived it: this whole project evolved in small committed steps, and **Alembic is
strangler-fig for the schema** — evolve in reversible increments, never drop-and-rebuild.

---

## Gotchas & takeaways

- **Secrets live in the environment, never in git.** `.env` is gitignored; `pydantic-settings` reads
  it and fails loudly if a required value is missing.
- **Never store a plaintext password** — hash it (Argon2, salted). **Never `==`-compare passwords:**
  the DB holds a *hash*, so look up by *username* and `verify_password` the secret separately.
- **A response model that omits the hash** (`UserPublic`) is your leak-proof gate.
- **A JWT is signed, not encrypted** — readable by anyone, forgeable by no one without `SECRET_KEY`. A
  stolen bearer token *is* dangerous → HTTPS + short expiry.
- **Protecting a route = one dependency** (`CurrentUserDep`) — the DI payoff.
- **`create_all` can't evolve a schema.** Alembic migrations = versioned, reversible history;
  autogenerate diffs models-vs-DB, but **always read the result before applying**.
- **`render_as_batch=True` for SQLite** — without it, `ALTER TABLE` migrations fail.
- **A test's body must match its name** — a copied test that still asserts the old thing is worse than
  no test. And **error responses carry `{"detail": …}`**, not the resource.
- **Latent bugs hide in unrun code paths** (the offline `env.py` function, the `Table=True` typo) — a
  clean command doesn't prove every path is correct.
- **Startup code belongs in a lifespan handler, not at module import.** A module-level `seed_data()`
  ran on *import* — crashing fresh clones (pytest collection touched an unmigrated DB) and silently
  seeding the real `database.db` from test runs. `FastAPI(lifespan=...)` runs it when the *server*
  starts instead. (Caught by the post-step multi-agent review.)
- **Verify unfamiliar tools against live sources over stale memory** — `pwdlib`/`PyJWT` are the current
  stack, not the older `passlib`/`python-jose`; `httpx2` turned out to be Pydantic's real successor.

---
**← [Step 6](step-6-backend-architecture.md) · 🎉 You've reached the end of the guided build.**
