import { Routes, Route } from "react-router-dom"
import ContactList from "./ContactList"
import ContactDetail from "./ContactDetail"

function App() {
  return (
    <Routes>
      <Route path="/"             element={<ContactList />} />
      <Route path="/contacts/:id" element={<ContactDetail />} />
    </Routes>
  )
}

export default App
