import React, { useState, useEffect } from 'react'
import aiService from '../services/aiService'

export default function Dashboard(){
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [roadmap, setRoadmap] = useState(null)

  useEffect(() => {
    // Retrieve roadmap from session storage
    const stored = sessionStorage.getItem('tutormind_roadmap')
    if (stored) {
      setRoadmap(JSON.parse(stored))
    }
  }, [])

  const ask = async () => {
    if(!query) return
    setLoading(true)
    try{
      const resp = await aiService.queryRag(query, 5)
      setResult(resp.result)
    }catch(e){
      setResult({ error: e?.message || 'Request failed' })
    }finally{ setLoading(false) }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Dashboard</h2>
      <p className="mt-2 text-gray-600">Your AI-powered learning hub and daily updates.</p>

      {/* Roadmap Summary */}
      {roadmap && (
        <div className="mt-8 grid grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-900 to-blue-700 rounded-lg p-4">
            <div className="text-3xl font-bold text-blue-200">{roadmap.total_chapters}</div>
            <div className="text-sm text-blue-300 mt-1">Total Chapters</div>
          </div>
          <div className="bg-gradient-to-br from-green-900 to-green-700 rounded-lg p-4">
            <div className="text-3xl font-bold text-green-200">{Math.round(roadmap.total_estimated_hours)}</div>
            <div className="text-sm text-green-300 mt-1">Study Hours</div>
          </div>
          <div className="bg-gradient-to-br from-purple-900 to-purple-700 rounded-lg p-4">
            <div className="text-3xl font-bold text-purple-200">{roadmap.days_remaining}</div>
            <div className="text-sm text-purple-300 mt-1">Days Remaining</div>
          </div>
          <div className="bg-gradient-to-br from-yellow-900 to-yellow-700 rounded-lg p-4">
            <div className="text-lg font-bold text-yellow-200">{(roadmap.total_estimated_hours / roadmap.days_remaining).toFixed(1)}</div>
            <div className="text-sm text-yellow-300 mt-1">Hours/Day</div>
          </div>
        </div>
      )}

      {/* Today's Study Plan */}
      {roadmap && roadmap.daily_plan && roadmap.daily_plan.length > 0 && (
        <div className="mt-8 bg-gray-800 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-white mb-4">Today's Study Plan</h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="bg-blue-600 rounded px-3 py-1 text-sm font-semibold text-white">Morning</div>
              <div className="flex-1">
                <p className="text-white">{roadmap.daily_plan[0]?.morning_session?.activity}</p>
                <p className="text-gray-400 text-sm">{roadmap.daily_plan[0]?.morning_session?.duration}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="bg-purple-600 rounded px-3 py-1 text-sm font-semibold text-white">Afternoon</div>
              <div className="flex-1">
                <p className="text-white">{roadmap.daily_plan[0]?.afternoon_session?.activity}</p>
                <p className="text-gray-400 text-sm">{roadmap.daily_plan[0]?.afternoon_session?.duration}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="bg-indigo-600 rounded px-3 py-1 text-sm font-semibold text-white">Evening</div>
              <div className="flex-1">
                <p className="text-white">{roadmap.daily_plan[0]?.evening_session?.activity}</p>
                <p className="text-gray-400 text-sm">{roadmap.daily_plan[0]?.evening_session?.duration}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Assistant */}
      <div className="mt-8 max-w-xl">
        <label className="block text-sm text-gray-300">Ask the AI Assistant (RAG)</label>
        <div className="flex mt-2">
          <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Ask about your studies..." className="flex-1 p-2 rounded-l border" />
          <button onClick={ask} className="px-4 bg-blue-600 text-white rounded-r" disabled={loading}>{loading ? '...' : 'Ask'}</button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100 min-h-20">
          {result ? <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(result, null, 2)}</pre> : <span className="text-gray-400">Ask a question to get insights...</span>}
        </div>
      </div>
    </div>
  )
}
