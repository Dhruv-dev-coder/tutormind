import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import aiService from '../services/aiService'
import { getStudentId } from '../utils/userUtils'
import { loadRoadmap } from '../services/roadmapService'
import LessonDisplay from '../components/LessonDisplay'

export default function AIClassroom() {
  const [searchParams] = useSearchParams()
  const [topic, setTopic] = useState('')
  const [level, setLevel] = useState('beginner')
  const [loading, setLoading] = useState(false)
  const [session, setSession] = useState(null)
  const [error, setError] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const autoStarted = useRef(false)

  const startSession = useCallback(async (topicValue) => {
    const trimmed = (topicValue || '').trim()
    if (!trimmed) return

    const studentId = getStudentId()
    if (!studentId) {
      setError('Please sign in to start a classroom session.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const resp = await aiService.generateClassroomSession(studentId, trimmed, level)
      setSession({
        prompt: resp.prompt,
        lesson: resp.lesson,
        notes: resp.notes,
      })
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to start session')
    } finally {
      setLoading(false)
    }
  }, [level])

  useEffect(() => {
    loadRoadmap().then((data) => {
      setRoadmap(data)
      const topicParam = searchParams.get('topic')
      if (topicParam) {
        autoStarted.current = true
        setTopic(topicParam)
        startSession(topicParam)
      } else if (data && data.chapters && data.chapters.length > 0 && !topic) {
        const defaultTopic = data.chapters[0].topics?.[0] || data.chapters[0].name
        setTopic(defaultTopic)
      }
    })
  }, [searchParams, startSession, topic])

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">AI Classroom</h2>
      <p className="mt-2 text-gray-400">
        Interactive lessons powered by your roadmap. Topics from the dashboard start automatically.
      </p>

      <div className="mt-6 max-w-3xl">
        <label className="block text-sm text-gray-300">Topic</label>
        <div className="flex mt-2 gap-2">
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="flex-1 p-2 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {roadmap && roadmap.chapters?.map((ch, idx) => (
              <optgroup key={idx} label={ch.subject || 'General'}>
                <option value={ch.name}>{ch.name}</option>
                {ch.topics?.map((top, tIdx) => (
                  <option key={`${idx}-${tIdx}`} value={top}>{top}</option>
                ))}
              </optgroup>
            ))}
            {!roadmap && <option value="">Loading topics...</option>}
          </select>
          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            className="p-2 rounded bg-gray-700 text-white border border-gray-600"
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <button
            onClick={() => startSession(topic)}
            className="px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded"
            disabled={loading || !topic.trim()}
          >
            {loading ? 'Teaching...' : 'Start Session'}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-900/40 border border-red-700 rounded text-red-200 text-sm">
            {error}
          </div>
        )}

        {loading && !session && (
          <div className="mt-8 text-center text-gray-400">
            <p className="text-lg">Preparing your lesson on &ldquo;{topic}&rdquo;...</p>
            <p className="text-sm mt-2">Generating explanation, examples, and notes.</p>
          </div>
        )}

        {session && (
          <div className="mt-8">
            <LessonDisplay
              lesson={session.lesson}
              notes={session.notes}
              prompt={session.prompt}
              onSelectTopic={(t) => {
                setTopic(t)
                startSession(t)
              }}
            />
          </div>
        )}

        {!loading && !session && !error && (
          <div className="mt-8 p-6 bg-gray-800 rounded-lg text-gray-400 text-center">
            Enter a topic or click a roadmap session from your dashboard to begin.
          </div>
        )}
      </div>
    </div>
  )
}
