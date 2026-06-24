import React, { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import aiService from '../services/aiService'
import { getStudentId } from '../utils/userUtils'

export default function NotesReview() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [topic, setTopic] = useState('')
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [summarizing, setSummarizing] = useState(false)

  useEffect(() => {
    const topicParam = searchParams.get('topic')
    if (topicParam) {
      setTopic(topicParam)
      fetchNotes(topicParam)
    }
  }, [searchParams])

  const fetchNotes = async (topicValue) => {
    const studentId = getStudentId()
    if (!studentId) {
      setError('Please sign in to view notes.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const resp = await aiService.getNotes(studentId, topicValue || undefined)
      setNotes(resp.notes || [])
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to load notes')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    if (topic.trim()) {
      navigate(`/notes/review?topic=${encodeURIComponent(topic.trim())}`)
      fetchNotes(topic.trim())
    }
  }

  const handleSummarize = async (note) => {
    const studentId = getStudentId()
    if (!studentId) return

    setSummarizing(true)
    try {
      const headings = note.notes?.headings || []
      const summaryPoints = headings.flatMap((h) => h.points || []).slice(0, 5)
      const summaryText = summaryPoints.join(' ') || note.notes?.summary || `Summary of ${note.topic}`

      await aiService.saveNotes(studentId, note.topic, {
        title: `${note.topic} — Quick Summary`,
        headings: [
          { heading: 'Summary', points: [summaryText] },
          ...(headings.length > 0 ? [{ heading: 'Key Points', points: summaryPoints }] : []),
        ],
        summary: summaryText,
      }, note.lesson)

      await fetchNotes(note.topic)
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to summarize notes')
    } finally {
      setSummarizing(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Review & Notes</h2>
      <p className="mt-2 text-gray-400">
        Revisit AI-generated notes from your classroom sessions.
      </p>

      <form onSubmit={handleSearch} className="mt-6 max-w-2xl flex gap-2">
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Search by topic..."
          className="flex-1 p-2 rounded border bg-gray-700 text-white border-gray-600"
        />
        <button
          type="submit"
          className="px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Search'}
        </button>
      </form>

      {error && (
        <div className="mt-4 max-w-2xl p-3 bg-red-900/40 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <p className="mt-8 text-gray-400">Loading notes...</p>
      )}

      {!loading && notes.length === 0 && topic && !error && (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg text-center max-w-2xl">
          <p className="text-gray-400">No notes found for &ldquo;{topic}&rdquo;.</p>
          <button
            type="button"
            onClick={() => navigate(`/ai-classroom?topic=${encodeURIComponent(topic)}`)}
            className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded"
          >
            Start a Classroom Session
          </button>
        </div>
      )}

      <div className="mt-8 space-y-6 max-w-3xl">
        {notes.map((note) => (
          <div key={note._id} className="bg-gray-800 rounded-lg p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="text-xl font-semibold text-white">{note.notes?.title || note.topic}</h3>
                <p className="text-gray-400 text-sm mt-1">
                  {note.topic} · {note.created_at?.slice(0, 10)} · {note.source || 'ai_classroom'}
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleSummarize(note)}
                disabled={summarizing}
                className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-indigo-300 rounded shrink-0"
              >
                {summarizing ? 'Saving...' : 'Summarize'}
              </button>
            </div>

            {note.notes?.headings?.map((section, i) => (
              <div key={i} className="mt-4">
                <h4 className="text-indigo-300 font-medium">{section.heading}</h4>
                <ul className="list-disc list-inside text-gray-300 text-sm mt-1 space-y-1">
                  {section.points?.map((point, j) => (
                    <li key={j}>{point}</li>
                  ))}
                </ul>
              </div>
            ))}

            {note.notes?.summary && (
              <p className="mt-4 text-gray-300 text-sm italic border-t border-gray-700 pt-4">
                {note.notes.summary}
              </p>
            )}

            {note.lesson?.explanation?.overview && (
              <div className="mt-4 border-t border-gray-700 pt-4">
                <h4 className="text-white font-medium text-sm mb-2">Original Explanation</h4>
                <p className="text-gray-400 text-sm">{note.lesson.explanation.overview}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
