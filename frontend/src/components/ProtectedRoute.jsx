import React, { useState, useEffect } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import authService from '../services/authService'

export default function ProtectedRoute({ children }){
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const location = useLocation()

  useEffect(() => {
    const unsubscribe = authService.onAuthStateChange(async (currentUser) => {
      if (currentUser) {
        // If we have a Firebase user, check if we need to verify with the backend (e.g. on new tab or reload)
        const storedUser = sessionStorage.getItem('tutormind_user')
        if (!storedUser) {
          try {
            await authService.verifyWithBackend()
          } catch (e) {
            console.error('Failed to verify user with backend on auth change:', e)
          }
        }
        setUser(currentUser)
      } else {
        setUser(null)
      }
      setLoading(false)
    })
    return () => unsubscribe()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          <span className="text-gray-400 text-sm font-medium">Securing connection...</span>
        </div>
      </div>
    )
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  // Check onboarding status from session
  const userInfo = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
  const isOnboarded = userInfo.onboarded || false
  
  // If user is not onboarded and not already on onboarding page, redirect
  if (!isOnboarded && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />
  }
  
  // If user is already onboarded and tries to access onboarding page, redirect to dashboard
  if (isOnboarded && location.pathname === '/onboarding') {
    return <Navigate to="/dashboard" replace />
  }
  
  return children
}
