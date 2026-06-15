import React, { useState } from 'react'
import aiService from '../services/aiService'

export default function Dashboard(){
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

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
      <p className="mt-2 text-gray-600">Your study summary and recommendations will appear here.</p>

      <div className="mt-6 max-w-xl">
        <label className="block text-sm text-gray-300">Ask the AI (RAG)</label>
        <div className="flex mt-2">
          <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Ask a question..." className="flex-1 p-2 rounded-l border" />
          <button onClick={ask} className="px-4 bg-blue-600 text-white rounded-r" disabled={loading}>{loading ? '...' : 'Ask'}</button>
        </div>
        <div className="mt-4 p-3 bg-gray-800 rounded text-gray-100">
          {result ? <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre> : <span className="text-gray-400">No response yet.</span>}
        </div>
      </div>
    </div>
  )
}
