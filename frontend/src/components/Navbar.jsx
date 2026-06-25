import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import authService from '../services/authService'

export default function Navbar(){
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const unsubscribe = authService.onAuthStateChange((currentUser) => {
      setUser(currentUser)
    })
    return () => unsubscribe()
  }, [])

  const handleLogout = async () => {
    await authService.signOut()
    navigate('/login')
  }

  return (
    <nav className="bg-gray-900 border-b border-gray-800 shadow-md">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
        <div>
          <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent hover:opacity-90 transition">
            TutorMind
          </Link>
        </div>
        {user && (
          <div className="space-x-6 flex items-center">
            <Link to="/dashboard" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Dashboard
            </Link>
            <Link to="/planner" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Planner
            </Link>
            <Link to="/ai-classroom" className="text-sm font-medium text-gray-300 hover:text-white transition">
              AI Classroom
            </Link>
            <Link to="/quiz" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Quizzes
            </Link>
            <Link to="/notes/review" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Notes
            </Link>
            <button onClick={handleLogout} className="text-sm font-medium text-red-400 hover:text-red-300 transition">
              Logout
            </button>
          </div>
        )}
        {!user && (
          <div className="space-x-4 flex items-center">
            <Link to="/login" className="text-sm font-medium text-gray-300 hover:text-white transition">
              Sign In
            </Link>
            <Link to="/register" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition">
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
