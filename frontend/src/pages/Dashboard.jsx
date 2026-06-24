import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import aiService from '../services/aiService'
import { loadRoadmap } from '../services/roadmapService'
import { getStudentId } from '../utils/userUtils'
import { getTodayPlan } from '../utils/roadmapUtils'
import LearningSessionBlock from '../components/LearningSessionBlock'

export default function Dashboard() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const [history, setHistory] = useState({ notes: [], quizzes: [] })
  const navigate = useNavigate()

  useEffect(() => {
    async function init() {
      const data = await loadRoadmap()
      setRoadmap(data)

      const studentId = getStudentId()
      if (studentId) {
        try {
          const [notesResp, quizResp] = await Promise.all([
            aiService.getNotes(studentId),
            aiService.getQuizHistory(studentId),
          ])
          setHistory({
            notes: notesResp.notes || [],
            quizzes: (quizResp.attempts || []).filter((a) => a.status === 'submitted'),
          })
        } catch {
          // history is optional
        }
      }
    }
    init()
  }, [])

  const ask = async () => {
    if (!query) return
    setLoading(true)
    try {
      const resp = await aiService.queryRag(query, 5)
      setResult(resp.result)
    } catch (e) {
      setResult({ error: e?.message || 'Request failed' })
    } finally {
      setLoading(false)
    }
  }

  const todayPlan = getTodayPlan(roadmap)

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Dashboard</h2>
      <p className="mt-2 text-gray-400">Your AI-powered learning hub — click any session to start learning.</p>

      {roadmap && (
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard value={roadmap.total_chapters} label="Total Chapters" gradient="from-blue-900 to-blue-700" textColor="text-blue-200" />
          <MetricCard value={Math.round(roadmap.total_estimated_hours)} label="Study Hours" gradient="from-green-900 to-green-700" textColor="text-green-200" />
          <MetricCard value={roadmap.days_remaining} label="Days Remaining" gradient="from-purple-900 to-purple-700" textColor="text-purple-200" />
          <MetricCard
            value={(roadmap.total_estimated_hours / roadmap.days_remaining).toFixed(1)}
            label="Hours/Day"
            gradient="from-yellow-900 to-yellow-700"
            textColor="text-yellow-200"
          />
        </div>
      )}

      {todayPlan && (
        <div className="mt-8 bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-white">
              Today&apos;s Study Plan
              <span className="text-gray-400 text-sm font-normal ml-2">Day {todayPlan.day} · {todayPlan.date}</span>
            </h3>
            <span className="text-indigo-300 text-sm">Focus: {todayPlan.focus}</span>
          </div>
          <div className="space-y-3">
            <LearningSessionBlock label="Morning" session={todayPlan.morning_session} dayPlan={todayPlan} />
            <LearningSessionBlock label="Afternoon" session={todayPlan.afternoon_session} dayPlan={todayPlan} />
            <LearningSessionBlock label="Evening" session={todayPlan.evening_session} dayPlan={todayPlan} />
          </div>
        </div>
      )}

      {(history.notes.length > 0 || history.quizzes.length > 0) && (
        <div className="mt-8 grid md:grid-cols-2 gap-6">
          {history.quizzes.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-3">Recent Quiz Results</h3>
              <div className="space-y-2">
                {history.quizzes.slice(0, 5).map((attempt, i) => (
                  <div key={i} className="flex justify-between items-center bg-gray-700/50 rounded p-3">
                    <div>
                      <p className="text-white text-sm">{attempt.topic}</p>
                      <p className="text-gray-400 text-xs">{attempt.created_at?.slice(0, 10)}</p>
                    </div>
                    <span className="text-yellow-300 font-semibold">
                      {attempt.evaluation?.percentage?.toFixed?.(0) ?? '—'}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {history.notes.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-3">Saved Notes</h3>
              <div className="space-y-2">
                {history.notes.slice(0, 5).map((note, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => navigate(`/notes/review?topic=${encodeURIComponent(note.topic)}`)}
                    className="w-full flex justify-between items-center bg-gray-700/50 hover:bg-gray-700 rounded p-3 text-left transition"
                  >
                    <p className="text-white text-sm">{note.topic}</p>
                    <span className="text-indigo-400 text-xs">Review →</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="mt-8 max-w-xl">
        <label className="block text-sm text-gray-300">Ask the AI Assistant (RAG)</label>
        <div className="flex mt-2">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about your studies..."
            className="flex-1 p-2 rounded-l border bg-gray-700 text-white border-gray-600"
          />
          <button onClick={ask} className="px-4 bg-blue-600 text-white rounded-r" disabled={loading}>
            {loading ? '...' : 'Ask'}
          </button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100 min-h-20">
          {result ? (
            <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(result, null, 2)}</pre>
          ) : (
            <span className="text-gray-400">Ask a question to get insights...</span>
          )}
        </div>
      </div>
    </div>
  )
}

function MetricCard({ value, label, gradient, textColor }) {
  return (
    <div className={`bg-gradient-to-br ${gradient} rounded-lg p-4`}>
      <div className={`text-3xl font-bold ${textColor}`}>{value}</div>
      <div className={`text-sm ${textColor} opacity-80 mt-1`}>{label}</div>
    </div>
  )
}
