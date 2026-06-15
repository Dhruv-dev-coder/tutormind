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
    const cred = await signInWithEmailAndPassword(auth, email, password)
    // verify with backend and attach auth header
    try{ await authService.verifyWithBackend() }catch(e){}
    return cred
  },
  signUpWithEmail: async (email, password, profile = {}) => {
    ensureFirebase()
    const userCred = await createUserWithEmailAndPassword(auth, email, password)
    try{ await authService.verifyWithBackend() }catch(e){}
    return userCred
  },
  signInWithGoogle: async () => {
    ensureFirebase()
    const cred = await signInWithPopup(auth, provider)
    try{ await authService.verifyWithBackend() }catch(e){}
    return cred
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
    if(!auth || !auth.currentUser) return null
    const idToken = await auth.currentUser.getIdToken()
    // send to backend verify endpoint
    try{
      const resp = await api.post('/auth/verify', { id_token: idToken })
      // attach token for subsequent API calls
      setAuthToken(idToken)
      return resp.data
    }catch(err){
      return null
    }
  }
}

export default authService
