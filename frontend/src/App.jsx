import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Dashboard from './pages/Dashboard'
import StudyPlanner from './pages/StudyPlanner'
import AIClassroom from './pages/AIClassroom'
import QuizCenter from './pages/QuizCenter'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'

export default function App(){
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <div className="max-w-6xl mx-auto p-6">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/planner" element={<ProtectedRoute><StudyPlanner /></ProtectedRoute>} />
            <Route path="/classroom" element={<ProtectedRoute><AIClassroom /></ProtectedRoute>} />
            <Route path="/quizzes" element={<ProtectedRoute><QuizCenter /></ProtectedRoute>} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}
