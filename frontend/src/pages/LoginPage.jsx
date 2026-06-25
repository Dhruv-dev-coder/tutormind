import React, { useState } from 'react'
import authService from '../services/authService'
import { useNavigate } from 'react-router-dom'

export default function LoginPage(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try{
      const user = await authService.signInWithEmail(email, password)
      if (user && user.is_first_time) {
        navigate('/onboarding')
      } else {
        navigate('/dashboard')
      }
    }catch(err){
      alert('Login failed')
    }
  }

  const handleGoogle = async () => {
    try{
      const user = await authService.signInWithGoogle()
      if (user && user.is_first_time) {
        navigate('/onboarding')
      } else {
        navigate('/dashboard')
      }
    }catch(err){
      alert('Google sign-in failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 p-8 bg-gray-900 border border-gray-800 rounded-xl shadow-2xl">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">Sign In</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Email Address</label>
          <input 
            type="email"
            value={email} 
            onChange={e=>setEmail(e.target.value)} 
            placeholder="email@example.com" 
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition" 
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={e=>setPassword(e.target.value)} 
            placeholder="••••••••" 
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition" 
          />
        </div>
        <div className="flex items-center justify-between pt-4 gap-4">
          <button type="submit" className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-indigo-500/20 transition">Sign In</button>
          <button type="button" onClick={handleGoogle} className="flex-1 py-3 bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 font-semibold rounded-lg transition">Google</button>
        </div>
      </form>
    </div>
  )
}
