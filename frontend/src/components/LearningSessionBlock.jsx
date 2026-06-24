import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  getSessionTopic,
  inferSessionType,
  getActionRoute,
  getSessionActionLabel,
} from '../utils/roadmapUtils'

const LABEL_COLORS = {
  Morning: 'bg-blue-600',
  Afternoon: 'bg-purple-600',
  Evening: 'bg-indigo-600',
}

const TYPE_ICONS = {
  concept_learning: '📖',
  practice: '✏️',
  revision: '📝',
}

export default function LearningSessionBlock({ label, session, dayPlan }) {
  const navigate = useNavigate()
  const topic = getSessionTopic(session, dayPlan)
  const sessionType = inferSessionType(session)
  const colorClass = LABEL_COLORS[label] || 'bg-gray-600'

  const handleClick = () => {
    navigate(getActionRoute(sessionType, topic))
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className="w-full flex items-start gap-3 p-3 rounded-lg bg-gray-700/50 hover:bg-gray-700 border border-gray-600 hover:border-indigo-500 transition text-left group"
    >
      <div className={`${colorClass} rounded px-3 py-1 text-sm font-semibold text-white shrink-0`}>
        {label}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-lg">{TYPE_ICONS[sessionType]}</span>
          <p className="text-white font-medium">{session?.activity}</p>
        </div>
        <p className="text-indigo-300 text-sm mt-0.5 truncate">{topic}</p>
        <p className="text-gray-400 text-sm">{session?.duration}</p>
        <p className="text-indigo-400 text-xs mt-1 opacity-0 group-hover:opacity-100 transition">
          {getSessionActionLabel(sessionType)} →
        </p>
      </div>
    </button>
  )
}
