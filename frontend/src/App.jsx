import { Routes, Route, Link } from "react-router-dom"
import ContactList from "./ContactList"
import ContactDetail from "./ContactDetail"

function NotFound() {
  return (
    <div>
      <p>Page not found.</p>
      <Link to="/">← Back to contacts</Link>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/"             element={<ContactList />} />
      <Route path="/contacts/:id" element={<ContactDetail />} />
      <Route path="*"             element={<NotFound />} />
    </Routes>
  )
}

export default App
