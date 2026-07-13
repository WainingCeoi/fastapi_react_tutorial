import { useState, useEffect } from "react"
import { Link } from "react-router-dom"

const API = "http://localhost:8000"

function ContactList() {
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")

  useEffect(() => {
    fetch(`${API}/contacts`)
      .then((response) => {
        if (!response.ok) throw new Error(`Server error: ${response.status}`)
        return response.json()
      })
      .then((data) => setContacts(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  function handleSubmit(event) {
    event.preventDefault()
    fetch(`${API}/contacts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`Server error: ${response.status}`)
        return response.json()
      })
      .then((newContact) => {
        setContacts((prev) => [...prev, newContact]) // functional update — no stale closure
        setName("")
        setEmail("")
      })
      .catch((err) => setError(err.message))
  }

  function handleDelete(id) {
    fetch(`${API}/contacts/${id}`, { method: "DELETE" })
      .then((response) => {
        if (!response.ok) throw new Error(`Server error: ${response.status}`)
        setContacts((prev) => prev.filter((c) => c.id !== id)) // only remove on success
      })
      .catch((err) => setError(err.message))
  }

  if (loading) return <p>Loading...</p>

  return (
    <div>
      <h1>My Contacts</h1>
      {error && <p>Something went wrong: {error}</p>}
      <form onSubmit={handleSubmit}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <button type="submit">Add</button>
      </form>
      <ul>
        {contacts.map((contact) => (
          <li key={contact.id}>
            <Link to={`/contacts/${contact.id}`}>{contact.name}</Link> - {contact.email}
            <button onClick={() => handleDelete(contact.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ContactList
