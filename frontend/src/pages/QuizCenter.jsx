import React, { useState } from 'react'
import aiService from '../services/aiService'

export default function QuizCenter(){
  const [subject, setSubject] = useState('')
  const [loading, setLoading] = useState(false)
  const [quiz, setQuiz] = useState(null)

  const generate = async () => {
    if(!subject) return
    setLoading(true)
    try{
      const resp = await aiService.generateQuiz('me', subject, 'medium')
      setQuiz(resp.quiz)
    }catch(e){
      setQuiz({ error: e?.message || 'Failed' })
    }finally{ setLoading(false) }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Quiz Center</h2>
      <p className="mt-2 text-gray-600">Take quizzes, view past results, and track improvement.</p>

      <div className="mt-6 max-w-2xl">
        <label className="block text-sm text-gray-300">Subject or topic</label>
        <div className="flex mt-2">
          <input value={subject} onChange={e=>setSubject(e.target.value)} placeholder="e.g. Algebra" className="flex-1 p-2 rounded-l border" />
          <button onClick={generate} className="px-4 bg-yellow-600 text-white rounded-r" disabled={loading}>{loading ? '...' : 'Generate Quiz'}</button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100">
          {quiz ? <pre className="whitespace-pre-wrap">{JSON.stringify(quiz, null, 2)}</pre> : <span className="text-gray-400">No quiz generated yet.</span>}
        </div>
      </div>
    </div>
  )
}
