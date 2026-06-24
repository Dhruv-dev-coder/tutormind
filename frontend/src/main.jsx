import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles/index.css'
import authService from './services/authService'
import { setAuthToken } from './services/apiService'

// Restore Firebase auth token for API calls after page refresh
authService.getCurrentUser()?.getIdToken().then((token) => {
  if (token) setAuthToken(token)
}).catch(() => {})

const container = document.getElementById('root')
const root = createRoot(container)
root.render(<App />)
