import React, { useState } from 'react'
import aiService from '../services/aiService'

export default function StudyPlanner(){
  const [syllabus, setSyllabus] = useState('')
  const [loading, setLoading] = useState(false)
  const [roadmap, setRoadmap] = useState(null)

  const generate = async () => {
    setLoading(true)
    try{
      const resp = await aiService.generateRoadmap('me', syllabus, '')
      setRoadmap(resp.roadmap)
    }catch(e){
      setRoadmap({ error: e?.message || 'Failed' })
    }finally{ setLoading(false) }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Study Planner</h2>
      <p className="mt-2 text-gray-600">Create and view your personalized study plans here.</p>

      <div className="mt-6 max-w-2xl">
        <label className="block text-sm text-gray-300">Paste syllabus or topics</label>
        <textarea value={syllabus} onChange={e=>setSyllabus(e.target.value)} className="w-full p-2 mt-2 h-32 rounded border" />
        <div className="mt-3">
          <button onClick={generate} className="px-4 py-2 bg-green-600 text-white rounded" disabled={loading}>{loading ? 'Generating...' : 'Generate Roadmap'}</button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100">
          {roadmap ? <pre className="whitespace-pre-wrap">{JSON.stringify(roadmap, null, 2)}</pre> : <span className="text-gray-400">No roadmap yet.</span>}
        </div>
      </div>
    </div>
  )
}
