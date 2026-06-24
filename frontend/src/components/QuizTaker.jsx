import React, { useState } from 'react'

export default function QuizTaker({ quiz, onSubmit, submitting }) {
  const [answers, setAnswers] = useState({})

  if (!quiz?.questions) return null

  const setAnswer = (questionId, value) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }))
  }

  const handleSubmit = () => {
    const formatted = quiz.questions.map((q) => ({
      question_id: q.id,
      answer: answers[q.id] ?? (q.type === 'true_false' ? false : ''),
    }))
    onSubmit(formatted, quiz.questions)
  }

  const allAnswered = quiz.questions.every((q) => {
    const val = answers[q.id]
    if (q.type === 'short_answer' || q.type === 'essay') return val && String(val).trim().length > 0
    return val !== undefined && val !== null && val !== ''
  })

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white">{quiz.title}</h3>
        <p className="text-gray-400 text-sm mt-1">{quiz.description}</p>
        <div className="flex gap-4 mt-3 text-sm text-gray-300">
          <span>{quiz.total_questions} questions</span>
          <span>{quiz.total_marks} marks</span>
          <span className="capitalize">{quiz.difficulty}</span>
          <span>{quiz.time_limit_minutes} min</span>
        </div>
      </div>

      {quiz.questions.map((q, idx) => (
        <div key={q.id} className="bg-gray-800 rounded-lg p-6">
          <p className="text-white font-medium">
            {idx + 1}. {q.question}
            <span className="text-gray-400 text-sm ml-2">({q.marks} marks)</span>
          </p>
          {q.topic && <p className="text-indigo-400 text-xs mt-1">Topic: {q.topic}</p>}

          {q.type === 'multiple_choice' && (
            <div className="mt-3 space-y-2">
              {q.options?.map((opt, i) => (
                <label key={i} className="flex items-center gap-2 text-gray-200 cursor-pointer">
                  <input
                    type="radio"
                    name={q.id}
                    checked={answers[q.id] === i}
                    onChange={() => setAnswer(q.id, i)}
                    className="text-indigo-600"
                  />
                  {opt}
                </label>
              ))}
            </div>
          )}

          {q.type === 'true_false' && (
            <div className="mt-3 flex gap-4">
              {[true, false].map((val) => (
                <label key={String(val)} className="flex items-center gap-2 text-gray-200 cursor-pointer">
                  <input
                    type="radio"
                    name={q.id}
                    checked={answers[q.id] === val}
                    onChange={() => setAnswer(q.id, val)}
                    className="text-indigo-600"
                  />
                  {val ? 'True' : 'False'}
                </label>
              ))}
            </div>
          )}

          {(q.type === 'short_answer' || q.type === 'essay') && (
            <textarea
              value={answers[q.id] || ''}
              onChange={(e) => setAnswer(q.id, e.target.value)}
              placeholder="Type your answer..."
              className="mt-3 w-full p-3 rounded bg-gray-700 border border-gray-600 text-white min-h-24"
            />
          )}
        </div>
      ))}

      <button
        type="button"
        onClick={handleSubmit}
        disabled={!allAnswered || submitting}
        className="w-full px-4 py-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white rounded-lg font-semibold"
      >
        {submitting ? 'Submitting...' : 'Submit Quiz'}
      </button>
    </div>
  )
}
