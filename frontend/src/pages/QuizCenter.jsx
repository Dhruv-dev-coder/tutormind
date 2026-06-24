import React, { useState, useEffect, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import aiService from '../services/aiService'
import { getStudentId } from '../utils/userUtils'
import QuizTaker from '../components/QuizTaker'
import QuizResults from '../components/QuizResults'

export default function QuizCenter() {
  const [searchParams] = useSearchParams()
  const [subject, setSubject] = useState('')
  const [difficulty, setDifficulty] = useState('medium')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [quiz, setQuiz] = useState(null)
  const [evaluation, setEvaluation] = useState(null)
  const [error, setError] = useState(null)
  const topicPrefilled = useRef(false)

  useEffect(() => {
    const topicParam = searchParams.get('topic')
    if (topicParam && !topicPrefilled.current) {
      topicPrefilled.current = true
      setSubject(topicParam)
    }
  }, [searchParams])

  const generate = async () => {
    if (!subject.trim()) return

    const studentId = getStudentId()
    if (!studentId) {
      setError('Please sign in to generate a quiz.')
      return
    }

    setLoading(true)
    setError(null)
    setEvaluation(null)
    try {
      const resp = await aiService.generateQuiz(studentId, subject.trim(), difficulty)
      setQuiz(resp.quiz)
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to generate quiz')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (answers, questions) => {
    const studentId = getStudentId()
    setSubmitting(true)
    try {
      const resp = await aiService.submitQuizAnswers(
        quiz.quiz_id,
        answers,
        questions,
        studentId,
        subject.trim(),
      )
      setEvaluation(resp.evaluation)
      setQuiz(null)
    } catch (e) {
      setError(e?.response?.data?.detail || e?.message || 'Failed to submit quiz')
    } finally {
      setSubmitting(false)
    }
  }

  const reset = () => {
    setQuiz(null)
    setEvaluation(null)
    setError(null)
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Quiz Center</h2>
      <p className="mt-2 text-gray-400">
        Practice problems from your roadmap. Topic is auto-filled when launched from the dashboard.
      </p>

      {!quiz && !evaluation && (
        <div className="mt-6 max-w-2xl">
          <label className="block text-sm text-gray-300">Subject or topic</label>
          <div className="flex mt-2 gap-2">
            <input
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. Binary Trees"
              className="flex-1 p-2 rounded border bg-gray-700 text-white border-gray-600"
            />
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="p-2 rounded bg-gray-700 text-white border border-gray-600"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
            <button
              onClick={generate}
              className="px-4 bg-yellow-600 hover:bg-yellow-700 text-white rounded"
              disabled={loading || !subject.trim()}
            >
              {loading ? 'Generating...' : 'Generate Quiz'}
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 max-w-2xl p-3 bg-red-900/40 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {quiz && (
        <div className="mt-6 max-w-3xl">
          <QuizTaker quiz={quiz} onSubmit={handleSubmit} submitting={submitting} />
        </div>
      )}

      {evaluation && (
        <div className="mt-6 max-w-3xl">
          <QuizResults evaluation={evaluation} />
          <button
            type="button"
            onClick={reset}
            className="mt-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
          >
            Take Another Quiz
          </button>
        </div>
      )}

      {!quiz && !evaluation && !loading && (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg text-gray-400 text-center max-w-2xl">
          {subject ? (
            <p>Topic &ldquo;{subject}&rdquo; is ready. Click Generate Quiz to start.</p>
          ) : (
            <p>Enter a topic or launch from your dashboard roadmap.</p>
          )}
        </div>
      )}
    </div>
  )
}
