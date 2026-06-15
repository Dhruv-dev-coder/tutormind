import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import authService from '../services/authService'

export default function ProtectedRoute({ children }){
  const user = authService.getCurrentUser()
  const location = useLocation()
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  // Check onboarding status from session
  const userInfo = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
  const isOnboarded = userInfo.onboarded || false
  const isFirstTime = userInfo.is_first_time || false
  
  // If user is not onboarded and not already on onboarding page, redirect
  if (!isOnboarded && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />
  }
  
  return children
}
