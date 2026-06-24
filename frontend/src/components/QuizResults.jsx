import React from 'react'

export default function QuizResults({ evaluation }) {
  if (!evaluation) return null

  const { total_score, total_marks, percentage, passed, weak_areas, recommendations, details } = evaluation

  return (
    <div className="space-y-6">
      <div className={`rounded-lg p-6 ${passed ? 'bg-green-900/40 border border-green-700' : 'bg-red-900/40 border border-red-700'}`}>
        <h3 className="text-2xl font-bold text-white">
          {total_score} / {total_marks} ({percentage?.toFixed?.(1) ?? percentage}%)
        </h3>
        <p className={`mt-1 font-medium ${passed ? 'text-green-300' : 'text-red-300'}`}>
          {passed ? 'Passed!' : 'Keep practicing — you can do better!'}
        </p>
      </div>

      {weak_areas?.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-2">Weak Areas</h4>
          <ul className="list-disc list-inside text-red-300">
            {weak_areas.map((area, i) => (
              <li key={i}>{area}</li>
            ))}
          </ul>
        </div>
      )}

      {recommendations?.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-2">Recommendations</h4>
          <ul className="list-disc list-inside text-indigo-300">
            {recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      {details?.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-3">Question Breakdown</h4>
          <div className="space-y-3">
            {details.map((d, i) => (
              <div key={i} className={`p-3 rounded ${d.is_correct ? 'bg-green-900/30' : 'bg-red-900/30'}`}>
                <p className="text-white text-sm font-medium">
                  Q{i + 1}: {d.is_correct ? 'Correct' : 'Incorrect'} ({d.marks_obtained}/{d.total_marks} marks)
                </p>
                {d.feedback && <p className="text-gray-300 text-sm mt-1">{d.feedback}</p>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
