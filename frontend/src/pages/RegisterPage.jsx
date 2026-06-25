import React, { useState } from 'react'
import authService from '../services/authService'
import { useNavigate } from 'react-router-dom'

export default function RegisterPage(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try{
      const user = await authService.signUpWithEmail(email, password, { displayName: name })
      if (user && user.is_first_time) {
        navigate('/onboarding')
      } else {
        navigate('/dashboard')
      }
    }catch(err){
      // show Firebase/backend error to help debugging
      const msg = err?.message || (err?.response && err.response.data) || 'Registration failed'
      alert(`Registration failed: ${msg}`)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 p-8 bg-gray-900 border border-gray-800 rounded-xl shadow-2xl">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">Create Account</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Full Name</label>
          <input 
            value={name} 
            onChange={e=>setName(e.target.value)} 
            placeholder="John Doe" 
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition" 
          />
        </div>
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
        <div className="pt-4">
          <button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-indigo-500/20 transition">Create Account</button>
        </div>
      </form>
    </div>
  )
}
