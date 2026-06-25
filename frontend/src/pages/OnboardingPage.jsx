import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiService'
import authService from '../services/authService'

export default function OnboardingPage() {
  const [step, setStep] = useState(1) // 1: instructions, 2: syllabus, 3: datesheet, 4: generating
  const [syllabusText, setSyllabusText] = useState('')
  const [subjects, setSubjects] = useState([])
  const [examDates, setExamDates] = useState({}) // format: { "Subject": "YYYY-MM-DD" }
  const [loading, setLoading] = useState(false)
  const [profileLoading, setProfileLoading] = useState(true)
  const [error, setError] = useState(null)
  const [userInfo, setUserInfo] = useState(() => {
    return JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
  })
  const navigate = useNavigate()

  const studentId = profileLoading ? null : userInfo.student_id

  useEffect(() => {
    let cancelled = false

    async function refreshUserProfile() {
      try {
        const verifiedUser = await authService.verifyWithBackend()
        if (!cancelled && verifiedUser) {
          setUserInfo(verifiedUser)
        }
      } catch (e) {
        if (!cancelled) {
          setUserInfo({})
          setError('Please sign in again before starting onboarding.')
        }
      } finally {
        if (!cancelled) {
          setProfileLoading(false)
        }
      }
    }

    refreshUserProfile()
    return () => {
      cancelled = true
    }
  }, [])

  const handleNext = async () => {
    if (step === 1) {
      setStep(2)
    } else if (step === 2) {
      setLoading(true)
      setError(null)
      try {
        const resp = await api.post('/api/onboarding/parse_syllabus', {
          syllabus_text: syllabusText
        })
        setSubjects(resp.data.subjects || [])
        // Initialize date selections
        const initialDates = {}
        ;(resp.data.subjects || []).forEach(subj => {
          initialDates[subj] = ''
        })
        setExamDates(initialDates)
        setStep(3)
      } catch (e) {
        setError(e?.response?.data?.detail || e?.message || 'Failed to parse syllabus')
      } finally {
        setLoading(false)
      }
    } else {
      submitOnboarding()
    }
  }

  const submitOnboarding = async () => {
    console.log('ONBOARDING USER:', userInfo)

    if (profileLoading || !studentId) {
      setError('Student profile is still loading. Please wait a moment and try again.')
      return
    }

    // Format the exam dates into structured datesheet text format
    const constructedDatesheet = Object.entries(examDates)
      .map(([subj, date]) => `${subj} - ${date || new Date().toISOString().slice(0, 10)}`)
      .join('\n')

    setLoading(true)
    setError(null)
    try {
      const resp = await api.post('/api/onboarding/initialize', {
        student_id: studentId,
        syllabus_text: syllabusText,
        datesheet_text: constructedDatesheet
      })
      
      // Store roadmap in session
      sessionStorage.setItem('tutormind_roadmap', JSON.stringify(resp.data.roadmap))
      
      // Update onboarding status in session storage to prevent ProtectedRoute from redirecting back
      const user = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
      user.onboarded = true
      sessionStorage.setItem('tutormind_user', JSON.stringify(user))
      
      // Navigate to dashboard
      navigate('/dashboard')
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to initialize')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white">
      <div className="max-w-3xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Welcome to TutorMind</h1>
          <p className="text-gray-300">Let's create your personalized learning roadmap</p>
        </div>

        {/* Step Indicator */}
        <div className="flex gap-2 mb-12">
          {[1, 2, 3].map(s => (
            <div key={s} className={`h-2 flex-1 rounded-full transition ${s <= step ? 'bg-indigo-500' : 'bg-gray-700'}`} />
          ))}
        </div>

        {/* Step 1: Instructions */}
        {step === 1 && (
          <div className="bg-gray-800/50 rounded-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">Step 1: Understanding Your Learning Path</h2>
            <div className="space-y-4 mb-8">
              <div className="flex gap-4">
                <div className="text-indigo-400 text-2xl">📚</div>
                <div>
                  <h3 className="font-semibold mb-1">Syllabus Analysis</h3>
                  <p className="text-gray-300">Paste your course syllabus or curriculum. We'll break it down into manageable topics.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="text-indigo-400 text-2xl">📅</div>
                <div>
                  <h3 className="font-semibold mb-1">Exam Schedule</h3>
                  <p className="text-gray-300">Share your exam dates and deadlines for optimized scheduling.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="text-indigo-400 text-2xl">🎯</div>
                <div>
                  <h3 className="font-semibold mb-1">Personalized Roadmap</h3>
                  <p className="text-gray-300">Get a custom daily, weekly, and monthly study plan tailored to your needs.</p>
                </div>
              </div>
            </div>
            <button 
              onClick={handleNext}
              className="w-full bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-lg font-semibold transition"
            >
              Get Started →
            </button>
          </div>
        )}

        {/* Step 2: Syllabus */}
        {step === 2 && (
          <div className="bg-gray-800/50 rounded-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">Step 2: Your Syllabus</h2>
            <p className="text-gray-300 mb-4">Paste your course syllabus, topics, or curriculum details:</p>
            <textarea 
              value={syllabusText}
              onChange={e => setSyllabusText(e.target.value)}
              placeholder="Chapter 1: Introduction to...&#10;Chapter 2: Core Concepts...&#10;Chapter 3: Advanced Topics..."
              className="w-full h-64 p-4 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-indigo-500"
            />
            <div className="flex gap-3 mt-6">
              <button 
                onClick={() => setStep(1)}
                className="flex-1 border border-gray-600 hover:border-indigo-500 px-6 py-3 rounded-lg font-semibold transition"
              >
                Back
              </button>
              <button 
                onClick={handleNext}
                disabled={!syllabusText.trim()}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition"
              >
                Next →
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Datesheet */}
        {step === 3 && (
          <div className="bg-gray-800/50 rounded-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">Step 3: Your Exam Schedule</h2>
            <p className="text-gray-300 mb-6">Assign exam dates for the subjects extracted from your syllabus:</p>
            
            <div className="space-y-4 max-h-80 overflow-y-auto mb-8 pr-2">
              {subjects.map((subj, idx) => (
                <div key={idx} className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 bg-gray-700/30 rounded-lg border border-gray-700">
                  <span className="font-semibold text-white truncate max-w-xs">{subj}</span>
                  <input
                    type="date"
                    value={examDates[subj] || ''}
                    onChange={(e) => setExamDates({ ...examDates, [subj]: e.target.value })}
                    className="p-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-indigo-500 transition"
                  />
                </div>
              ))}
              {subjects.length === 0 && (
                <p className="text-gray-400 italic">No subjects found in syllabus. Proceed to generate roadmap.</p>
              )}
            </div>
            
            <div className="flex gap-3 mt-6">
              <button 
                onClick={() => setStep(2)}
                className="flex-1 border border-gray-600 hover:border-indigo-500 px-6 py-3 rounded-lg font-semibold transition"
              >
                Back
              </button>
              <button 
                onClick={handleNext}
                disabled={loading || profileLoading || !studentId}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition"
              >
                {loading ? 'Generating...' : studentId ? 'Generate Roadmap →' : 'Loading Profile...'}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-900/20 border border-red-600 text-red-200 rounded-lg p-4 mt-6">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}
