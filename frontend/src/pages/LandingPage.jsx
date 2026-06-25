import React from 'react'
import { Link } from 'react-router-dom'

export default function LandingPage(){
  return (
    <div className="py-20 text-center max-w-3xl mx-auto flex flex-col items-center justify-center">
      <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-pulse">
        Welcome to TutorMind
      </h1>
      <p className="mt-6 text-lg md:text-xl text-gray-400 leading-relaxed max-w-2xl">
        An intelligent, autonomous AI-powered learning platform that generates personalized study roadmaps, provides adaptive instruction, interactive quizzes, and tracks your progress.
      </p>
      <div className="mt-10 flex gap-4 justify-center">
        <Link to="/register" className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-indigo-500/20 transition transform hover:-translate-y-0.5">
          Get Started
        </Link>
        <Link to="/login" className="px-8 py-3 bg-gray-900 hover:bg-gray-800 text-gray-200 border border-gray-800 font-semibold rounded-lg shadow-lg transition transform hover:-translate-y-0.5">
          Sign In
        </Link>
      </div>
    </div>
  )
}
