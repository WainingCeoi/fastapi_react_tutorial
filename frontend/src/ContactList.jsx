import { useState, useEffect } from "react"
import { Link } from "react-router-dom"

function ContactList() {
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")

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

  function handleSubmit(event) {
    event.preventDefault()
    fetch("http://localhost:8000/contacts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email }),
    })
      .then((response) => response.json())
      .then((newContact) => {
        setContacts([...contacts, newContact])
        setName("")
        setEmail("")
      })
  }

  function handleDelete(id) {
    fetch(`http://localhost:8000/contacts/${id}`, { method: "DELETE" })
      .then(() => setContacts(contacts.filter((c) => c.id !== id)))
  }

  if (loading) return <p>Loading...</p>
  if (error) return <p>Something went wrong: {error}</p>

  return (
    <div>
      <h1>My Contacts</h1>
      <form onSubmit={handleSubmit}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
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
