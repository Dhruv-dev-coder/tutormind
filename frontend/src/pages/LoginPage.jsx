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
      await authService.signInWithEmail(email, password)
      navigate('/dashboard')
    }catch(err){
      alert('Login failed')
    }
  }

  const handleGoogle = async () => {
    try{
      await authService.signInWithGoogle()
      navigate('/dashboard')
    }catch(err){
      alert('Google sign-in failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-12">
      <h2 className="text-2xl font-semibold">Sign in</h2>
      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="w-full p-2 border rounded" />
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" className="w-full p-2 border rounded" />
        <div className="flex items-center justify-between">
          <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Sign in</button>
          <button type="button" onClick={handleGoogle} className="px-4 py-2 border rounded">Google</button>
        </div>
      </form>
    </div>
  )
}
