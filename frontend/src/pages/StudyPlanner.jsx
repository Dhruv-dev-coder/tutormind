import React, { useState, useEffect } from 'react'
import aiService from '../services/aiService'
import { loadRoadmap } from '../services/roadmapService'
import LearningSessionBlock from '../components/LearningSessionBlock'

export default function StudyPlanner(){
  const [roadmap, setRoadmap] = useState(null)
  const [viewMode, setViewMode] = useState('semester') // semester, monthly, weekly, daily
  const [syllabusText, setSyllabusText] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadRoadmap().then(setRoadmap)
  }, [])

  const regenerate = async () => {
    setLoading(true)
    try{
      const userInfo = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
      const resp = await aiService.generateRoadmap(userInfo.student_id, syllabusText, '')
      setRoadmap(resp.roadmap)
      sessionStorage.setItem('tutormind_roadmap', JSON.stringify(resp.roadmap))
    }catch(e){
      console.error('Failed to regenerate roadmap:', e)
    }finally{ setLoading(false) }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-white">Study Planner</h2>
      <p className="mt-2 text-gray-600">Your personalized learning roadmap.</p>

      {roadmap && (
        <div className="mt-8">
          {/* View Mode Toggle */}
          <div className="flex gap-2 mb-6">
            {['semester', 'monthly', 'weekly', 'daily'].map(mode => (
              <button 
                key={mode}
                onClick={() => setViewMode(mode)}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  viewMode === mode 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>

          {/* Semester Plan */}
          {viewMode === 'semester' && (
            <div className="space-y-4">
              {roadmap.semester_plan?.map((phase, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-white mb-2">{phase.phase}</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-400 text-sm">Weeks</p>
                      <p className="text-white">{phase.weeks}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm">Focus</p>
                      <p className="text-white">{phase.focus}</p>
                    </div>
                    <div className="col-span-2">
                      <p className="text-gray-400 text-sm">Chapters</p>
                      <div className="flex flex-wrap gap-2 mt-1">
                        {phase.chapters?.map((ch, j) => (
                          <span key={j} className="bg-indigo-900 text-indigo-200 px-2 py-1 rounded text-sm">{ch}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Monthly Plan */}
          {viewMode === 'monthly' && (
            <div className="space-y-4">
              {roadmap.monthly_plan?.map((month, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-white mb-2">{month.month}</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-400 text-sm">Hours/Week</p>
                      <p className="text-white">{month.hours_per_week.toFixed(1)}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm">Assessment</p>
                      <p className="text-white">{month.assessment_type}</p>
                    </div>
                    <div className="col-span-2">
                      <p className="text-gray-400 text-sm">Topics</p>
                      <div className="flex flex-wrap gap-2 mt-1">
                        {month.chapters?.map((ch, j) => (
                          <span key={j} className="bg-green-900 text-green-200 px-2 py-1 rounded text-sm">{ch}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Weekly Plan */}
          {viewMode === 'weekly' && (
            <div className="space-y-4">
              {roadmap.weekly_plan?.map((week, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-white mb-2">Week {week.week}</h3>
                  <div className="space-y-2">
                    <div>
                      <p className="text-gray-400 text-sm">Focus</p>
                      <p className="text-white">{week.focus_chapter}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm">Daily Hours</p>
                      <p className="text-white">{week.daily_hours}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-sm">Quiz</p>
                      <p className="text-white">{week.quiz}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Daily Plan */}
          {viewMode === 'daily' && (
            <div className="space-y-4">
              {roadmap.daily_plan?.map((day, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-white mb-1">
                    Day {day.day} - {day.date}
                  </h3>
                  <p className="text-indigo-300 text-sm mb-4">Focus: {day.focus}</p>
                  <div className="space-y-3">
                    <LearningSessionBlock label="Morning" session={day.morning_session} dayPlan={day} />
                    <LearningSessionBlock label="Afternoon" session={day.afternoon_session} dayPlan={day} />
                    <LearningSessionBlock label="Evening" session={day.evening_session} dayPlan={day} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Regenerate Section */}
      <div className="mt-12 max-w-2xl bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-4">Regenerate Roadmap</h3>
        <textarea 
          value={syllabusText}
          onChange={e => setSyllabusText(e.target.value)}
          placeholder="Paste updated syllabus..."
          className="w-full h-32 p-3 rounded bg-gray-700 border border-gray-600 text-white mb-3"
        />
        <button 
          onClick={regenerate}
          disabled={loading || !syllabusText.trim()}
          className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg font-semibold"
        >
          {loading ? 'Generating...' : 'Regenerate Roadmap'}
        </button>
      </div>
    </div>
  )
}
