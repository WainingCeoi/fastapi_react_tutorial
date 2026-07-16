import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"

// dev: talk to the backend cross-origin (CORS). prod build (single-server, `make start`):
// same-origin relative path — this app and the API are served by one process.
const API = import.meta.env.DEV ? "http://localhost:8000/api" : "/api"

function ContactDetail() {
  const { id } = useParams()
  const [contact, setContact] = useState(null)
  const [notes, setNotes] = useState([])
  const [noteText, setNoteText] = useState("")
  const [error, setError] = useState(null) // fatal: contact failed to load → full-page
  const [noteError, setNoteError] = useState(null) // recoverable: notes area only → inline

  useEffect(() => {
    const controller = new AbortController()

    // reset for the new id — drop the previous contact's data and any old errors
    setContact(null)
    setNotes([])
    setError(null)
    setNoteError(null)

    fetch(`${API}/contacts/${id}`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Contact not found") // 404 → a real error, not a "contact"
        return response.json()
      })
      .then((data) => setContact(data))
      .catch((err) => {
        if (err.name !== "AbortError") setError(err.message)
      })

    fetch(`${API}/contacts/${id}/notes`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Server error: ${response.status}`)
        return response.json()
      })
      .then((data) => setNotes(data))
      .catch((err) => {
        if (err.name !== "AbortError") setNoteError("Couldn't load notes.")
      })

    // cleanup: cancel in-flight fetches when id changes (or we leave the page),
    // so a slow response for the OLD contact can't overwrite the NEW one
    return () => controller.abort()
  }, [id])

  function handleAddNote(event) {
    event.preventDefault()
    setNoteError(null)
    fetch(`${API}/contacts/${id}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: noteText }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`Server error: ${response.status}`)
        return response.json()
      })
      .then((newNote) => {
        setNotes((prev) => [...prev, newNote]) // functional update — no stale closure
        setNoteText("")
      })
      .catch(() => setNoteError("Couldn't save that note — try again.")) // recoverable, page stays
  }

  // fatal: we couldn't load the contact at all, so there's nothing to show
  if (error) {
    return (
      <div>
        <Link to="/">← Back</Link>
        <p>Something went wrong: {error}</p>
      </div>
    )
  }

  if (contact === null) return <p>Loading...</p>

  return (
    <div>
      <Link to="/">← Back</Link>
      <h1>{contact.name}</h1>
      <p>{contact.email}</p>

      <h2>Notes</h2>
      {noteError && <p>{noteError}</p>}
      <form onSubmit={handleAddNote}>
        <input value={noteText} onChange={(e) => setNoteText(e.target.value)} placeholder="New note" required />
        <button type="submit">Add note</button>
      </form>
      <ul>
        {notes.map((note) => (
          <li key={note.id}>{note.text}</li>
        ))}
      </ul>
    </div>
  )
}

export default ContactDetail
