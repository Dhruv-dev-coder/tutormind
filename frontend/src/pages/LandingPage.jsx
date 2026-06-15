import React from 'react'
import { Link } from 'react-router-dom'

export default function LandingPage(){
  return (
    <div className="py-12">
      <h1 className="text-4xl text-white font-bold">Welcome to TutorMind</h1>
      <p className="mt-4 text-gray-600">AI-powered autonomous learning platform.</p>
      <div className="mt-6">
        <Link to="/register" className="px-4 py-2 bg-blue-600 text-white rounded">Get started</Link>
        <Link to="/login" className="ml-4 px-4 py-2 border rounded text-white">Sign in</Link>
      </div>
    </div>
  )
}
