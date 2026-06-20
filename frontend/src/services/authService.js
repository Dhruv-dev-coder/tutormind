import { initializeApp } from 'firebase/app'
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup, signOut as firebaseSignOut } from 'firebase/auth'
import api, { setAuthToken } from './apiService'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
}

let app = null
let auth = null

function ensureFirebase(){
  if (!app) {
    app = initializeApp(firebaseConfig)
    auth = getAuth(app)
  }
}

const provider = new GoogleAuthProvider()

const authService = {
  signInWithEmail: async (email, password) => {
    ensureFirebase()
    await signInWithEmailAndPassword(auth, email, password)
    return await authService.verifyWithBackend()
  },
  signUpWithEmail: async (email, password, profile = {}) => {
    ensureFirebase()
    await createUserWithEmailAndPassword(auth, email, password)
    return await authService.verifyWithBackend()
  },
  signInWithGoogle: async () => {
    ensureFirebase()
    await signInWithPopup(auth, provider)
    return await authService.verifyWithBackend()
  },
  signOut: async () => {
    ensureFirebase()
    return await firebaseSignOut(auth)
  },
  getCurrentUser: () => {
    try{
      ensureFirebase()
      return auth.currentUser
    }catch(e){
      return null
    }
  },
  verifyWithBackend: async () => {
    ensureFirebase()
    if(!auth || !auth.currentUser) {
      throw new Error('No authenticated Firebase user')
    }
    const idToken = await auth.currentUser.getIdToken()
    // send to backend verify endpoint
    const resp = await api.post('/api/auth/verify', { id_token: idToken })
    // attach token for subsequent API calls
    setAuthToken(idToken)
    // store user info including onboarding status
    sessionStorage.setItem('tutormind_user', JSON.stringify(resp.data))
    return resp.data
  }
}

export default authService
