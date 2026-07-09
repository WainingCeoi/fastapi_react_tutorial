# Step 3 — First React Page

> **Goal:** a React page that fetches the contacts from the API and renders them, handling
> the loading and error moments gracefully.

## The big idea: UI = f(state)

```
   STATE (your data)        COMPONENT            WHAT YOU SEE
   ┌────────────┐         (a function)          ┌───────────────┐
   │ contacts=[]│ ────────►  App()  ───────────►│  (empty list) │
   └────────────┘                               └───────────────┘
         ▲                                               │
         │        setContacts([...])         data arrives│
         └───────────────────────────────────────────────┘
     change state  →  React re-runs App()  →  screen re-paints
```

You never update the screen by hand. You write a function (a **component**) that turns
**state** into UI. Change the state → React re-runs the function → the screen updates.

## React vs Streamlit (where the code runs)

| | Streamlit | React + FastAPI |
|---|---|---|
| UI code runs on | the **server** (Python) | the **browser** (JavaScript) |
| Processes | one | two (browser app + API server) |
| To get data | call a Python function | an **HTTP request** to the API |

This is *why* there are two servers, and why fetching data crosses a network boundary —
which is where **CORS** appears.

## The building blocks

- **Component** — a JS function that returns UI. Name is **Capitalized**.
- **JSX** — HTML-shaped syntax inside a component (compiled to JS). Must return **one root element**.
- **`{ }`** — inside JSX, switch back to JavaScript: `{contact.name}`.
- **`.map()` + `key`** — turn a list of data into a list of `<li>`; each item needs a unique `key`.
- **`useState`** — reactive data: `const [x, setX] = useState(initial)`. Calling `setX(...)` re-renders.
- **`useEffect(fn, [])`** — run a *side effect* (like fetching) **once, after the first render**. The `[]` means "run once."

## The fetch lifecycle

```
1st render:  contacts = []          → screen: "Loading…"
                 │  (after paint) useEffect fires
                 ▼
             fetch → :8000/contacts → JSON
                 │
                 ▼  setContacts(data)   ← state changes
2nd render:  contacts = [ …3… ]      → screen: the list
```

```jsx
const [contacts, setContacts] = useState([])
const [loading, setLoading]   = useState(true)
const [error, setError]       = useState(null)

useEffect(() => {
  fetch("http://localhost:8000/contacts")
    .then((response) => {
      if (!response.ok) throw new Error(`Server error: ${response.status}`)
      return response.json()
    })
    .then((data) => setContacts(data))
    .catch((err) => setError(err.message))
    .finally(() => setLoading(false))
}, [])

if (loading) return <p>Loading…</p>
if (error)   return <p>Something went wrong: {error}</p>
// else: render the list with contacts.map(...)
```

**Every fetch is in one of three states — handle all three:**

```
   LOADING ──success──► the list
      │
      └──failure──► error message
```

## CORS: the browser's bouncer

```
  BROWSER (origin localhost:5173)                    SERVER (localhost:8000)
        │  1. React: fetch(:8000/contacts)                    │
        │ ─────────────── request ──────────────────────────►│
        │                                                     │ 2. FastAPI → 200 + JSON
        │ ◄────────────── response (200 OK) ──────────────────│
        │  3. Browser: "any Access-Control-Allow-Origin       │
        │      header for localhost:5173?"  → NONE            │
        │      → 🚫 block JS from reading it                   │
        └── your .then() never runs. Console: CORS error. ────┘
```

- **Same-origin policy:** browsers block JS from *reading* responses from a **different origin** (scheme + host + port). `:5173` → `:8000` differ by port → cross-origin.
- **Why:** security — stop `evil.com`'s JS from reading `bank.com` using your logged-in session.
- **CORS is enforced by the *browser*, not the server.** The server returned `200 OK`; the browser refused to hand the result to your JS. (That's the `net::ERR_FAILED 200 (OK)` clue.)
- **Fix:** FastAPI `CORSMiddleware` stamps an `Access-Control-Allow-Origin` header onto every response:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # who's allowed in
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- **Middleware** = a station that *every* request/response passes through. CORS is one such station (adds the stamp); logging, auth, and timing are others.

## Gotchas & takeaways

- **CORS is browser-enforced** — `200 OK` on the server, yet blocked in the browser.
- **`fetch` does NOT reject on `4xx`/`5xx`** — only on *network* failure. A `404`/`500` still "succeeds"; check **`response.ok`** and `throw` yourself.
- **Template literals need backticks:** `` `Server error: ${x}` `` is JS's f-string. Plain quotes won't interpolate.
- Errors hide in two places: **browser console** (frontend) vs. **server terminal** (backend).
- React **StrictMode** runs effects **twice** in dev (a bug-surfacing aid; harmless).

---
**← [Step 2](step-2-first-api.md) · Next → [Step 4 — A Database](step-4-a-database.md)**
