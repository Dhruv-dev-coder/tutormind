import React, { useState, useEffect, useCallback } from 'react'
import { useSearchParams, useNavigate, Link } from 'react-router-dom'
import aiService from '../services/aiService'
import { getStudentId } from '../utils/userUtils'

export default function NotesReview() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [topic, setTopic] = useState('')
  const [allNotes, setAllNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [summarizing, setSummarizing] = useState(false)

  const fetchNotes = useCallback(async (topicValue) => {
    const studentId = getStudentId()
    if (!studentId) {
      setError('Please sign in to view notes.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const resp = await aiService.getNotes(studentId, topicValue || undefined)
      setAllNotes(resp.notes || [])
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to load notes')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    const topicParam = searchParams.get('topic')
    if (topicParam) {
      setTopic(topicParam)
    }
    fetchNotes(topicParam || null)
  }, [searchParams, fetchNotes])

  const handleSearch = (e) => {
    e.preventDefault()
    const trimmed = topic.trim()
    if (trimmed) {
      navigate(`/notes/review?topic=${encodeURIComponent(trimmed)}`)
    } else {
      navigate('/notes/review')
      fetchNotes(null)
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

      await fetchNotes(searchParams.get('topic') || null)
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to summarize notes')
    } finally {
      setSummarizing(false)
    }
  }

  const topicFilter = searchParams.get('topic')
  const notes = allNotes

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
          placeholder="Filter by topic (leave empty for all notes)..."
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

      {topicFilter && (
        <button
          type="button"
          onClick={() => { setTopic(''); navigate('/notes/review'); fetchNotes(null) }}
          className="mt-2 text-sm text-indigo-400 hover:text-indigo-300"
        >
          Show all notes
        </button>
      )}

      {error && (
        <div className="mt-4 max-w-2xl p-3 bg-red-900/40 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <p className="mt-8 text-gray-400">Loading notes...</p>
      )}

      {!loading && notes.length === 0 && !error && (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg text-center max-w-2xl">
          <p className="text-gray-400">
            {topicFilter
              ? `No notes found for "${topicFilter}".`
              : 'No notes yet. Complete an AI Classroom session to generate notes automatically.'}
          </p>
          <Link
            to={topicFilter ? `/ai-classroom?topic=${encodeURIComponent(topicFilter)}` : '/ai-classroom'}
            className="inline-block mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded"
          >
            Start a Classroom Session
          </Link>
        </div>
      )}

      {!loading && notes.length > 0 && (
        <p className="mt-4 text-gray-400 text-sm">{notes.length} note{notes.length !== 1 ? 's' : ''} found</p>
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
                  {section.points?.filter(Boolean).map((point, j) => (
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
