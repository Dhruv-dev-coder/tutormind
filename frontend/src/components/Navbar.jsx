import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import authService from '../services/authService'

export default function Navbar(){
  const navigate = useNavigate()

  const handleLogout = async () => {
    await authService.signOut()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        <div>
          <Link to="/" className="text-xl font-bold">TutorMind</Link>
        </div>
        <div className="space-x-4">
          <Link to="/dashboard" className="text-sm text-gray-700">Dashboard</Link>
          <Link to="/planner" className="text-sm text-gray-700">Planner</Link>
          <Link to="/ai-classroom" className="text-sm text-gray-700">AI Classroom</Link>
          <Link to="/quiz" className="text-sm text-gray-700">Quizzes</Link>
          <Link to="/notes/review" className="text-sm text-gray-700">Notes</Link>
          <button onClick={handleLogout} className="text-sm text-red-500">Logout</button>
        </div>
      </div>
    </nav>
  )
}
