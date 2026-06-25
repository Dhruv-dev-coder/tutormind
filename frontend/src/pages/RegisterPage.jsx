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
    <div className="max-w-md mx-auto mt-12">
      <h2 className="text-2xl font-semibold">Create account</h2>
      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Full name" className="w-full p-2 border rounded" />
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="w-full p-2 border rounded" />
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" className="w-full p-2 border rounded" />
        <div>
          <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded">Create account</button>
        </div>
      </form>
    </div>
  )
}
