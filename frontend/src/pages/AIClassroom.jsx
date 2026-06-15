import React, { useState } from 'react'
import aiService from '../services/aiService'

export default function AIClassroom(){
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [lesson, setLesson] = useState(null)

  const teach = async () => {
    if(!topic) return
    setLoading(true)
    try{
      const resp = await aiService.teachConcept('me', topic, 'beginner')
      setLesson(resp.result)
    }catch(e){
      setLesson({ error: e?.message || 'Failed' })
    }finally{ setLoading(false) }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">AI Classroom</h2>
      <p className="mt-2 text-gray-600">Interactive lessons, explanations, and practice sessions powered by the AI Tutor.</p>

      <div className="mt-6 max-w-2xl">
        <label className="block text-sm text-gray-300">Enter topic to teach</label>
        <div className="flex mt-2">
          <input value={topic} onChange={e=>setTopic(e.target.value)} placeholder="e.g. Newton's Laws" className="flex-1 p-2 rounded-l border" />
          <button onClick={teach} className="px-4 bg-indigo-600 text-white rounded-r" disabled={loading}>{loading ? '...' : 'Teach'}</button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100">
          {lesson ? <pre className="whitespace-pre-wrap">{JSON.stringify(lesson, null, 2)}</pre> : <span className="text-gray-400">No lesson yet.</span>}
        </div>
      </div>
    </div>
  )
}
