import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"

function ContactDetail() {
  const { id } = useParams()
  const [contact, setContact] = useState(null)
  const [notes, setNotes] = useState([])
  const [noteText, setNoteText] = useState("")
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`http://localhost:8000/contacts/${id}`)
      .then((response) => {
        if (!response.ok) throw new Error("Contact not found")   // 404 → a real error, not a "contact"
        return response.json()
      })
      .then((data) => setContact(data))
      .catch((err) => setError(err.message))

    fetch(`http://localhost:8000/contacts/${id}/notes`)
      .then((response) => response.json())
      .then((data) => setNotes(data))
  }, [id])

  function handleAddNote(event) {
    event.preventDefault()
    fetch(`http://localhost:8000/contacts/${id}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: noteText }),
    })
      .then((response) => response.json())
      .then((newNote) => {
        setNotes([...notes, newNote])
        setNoteText("")
      })
  }

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
      <form onSubmit={handleAddNote}>
        <input value={noteText} onChange={(e) => setNoteText(e.target.value)} placeholder="New note" />
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
