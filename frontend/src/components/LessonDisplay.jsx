import React from 'react'

export default function LessonDisplay({ lesson, notes, prompt, onSelectTopic }) {
  if (!lesson) return null

  const explanation = lesson.explanation || {}
  const resources = lesson.resources || []

  return (
    <div className="space-y-6">
      {prompt && (
        <div className="bg-indigo-900/40 border border-indigo-700 rounded-lg p-4">
          <p className="text-indigo-200 text-sm font-medium">Session prompt</p>
          <p className="text-white mt-1">{prompt}</p>
        </div>
      )}

      <div className="bg-gray-800 rounded-lg p-6">
        {lesson.subject && (
          <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider block mb-1">
            {lesson.subject}
          </span>
        )}
        <h3 className="text-2xl font-bold text-white">{lesson.topic}</h3>
        <p className="text-gray-400 text-sm mt-1">
          Level: {lesson.level} · {lesson.estimated_learning_time}
        </p>
      </div>

      {lesson.learning_objectives?.length > 0 && (
        <Section title="Learning Objectives">
          <ul className="list-disc list-inside space-y-1 text-gray-200">
            {lesson.learning_objectives.map((obj, i) => (
              <li key={i}>{obj}</li>
            ))}
          </ul>
        </Section>
      )}

      {explanation.overview && (
        <Section title="Concept Explanation">
          <p className="text-gray-200">{explanation.overview}</p>
          {explanation.definition && (
            <p className="text-gray-300 mt-2"><strong>Definition:</strong> {explanation.definition}</p>
          )}
          {explanation.why_important && (
            <p className="text-gray-300 mt-2"><strong>Why it matters:</strong> {explanation.why_important}</p>
          )}
        </Section>
      )}

      {lesson.lesson_path?.length > 0 && (
        <Section title="Step-by-Step Breakdown">
          <ol className="space-y-2">
            {lesson.lesson_path.map((step, i) => (
              <li key={i} className="flex gap-3 text-gray-200">
                <span className="bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs shrink-0">
                  {i + 1}
                </span>
                <div>
                  <p className="font-medium">{step.title}</p>
                  <p className="text-gray-400 text-sm">{step.description}</p>
                </div>
              </li>
            ))}
          </ol>
        </Section>
      )}

      {lesson.key_points?.length > 0 && (
        <Section title="Key Points">
          <ul className="list-disc list-inside space-y-1 text-gray-200">
            {lesson.key_points.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>
        </Section>
      )}

      {lesson.examples?.length > 0 && (
        <Section title="Examples">
          {lesson.examples.map((ex, i) => (
            <div key={i} className="bg-gray-700/50 rounded p-4 mb-3">
              <p className="text-white font-medium">{ex.problem}</p>
              {ex.solution_steps?.map((step, j) => (
                <p key={j} className="text-gray-300 text-sm mt-1">{step}</p>
              ))}
            </div>
          ))}
        </Section>
      )}

      {resources.length > 0 && (
        <Section title="References & Videos">
          <ul className="space-y-2">
            {resources.map((res, i) => (
              <li key={i}>
                <a
                  href={res.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-400 hover:text-indigo-300 underline"
                >
                  {res.title || res.url}
                </a>
                {res.type && <span className="text-gray-500 text-sm ml-2">({res.type})</span>}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {notes && (
        <Section title="Saved Notes">
          <p className="text-green-400 text-sm mb-2">Notes automatically saved to your account.</p>
          <h4 className="text-white font-medium">{notes.notes?.title}</h4>
          {notes.notes?.headings?.map((section, i) => (
            <div key={i} className="mt-3">
              <p className="text-indigo-300 font-medium">{section.heading}</p>
              <ul className="list-disc list-inside text-gray-300 text-sm mt-1">
                {section.points?.map((point, j) => (
                  <li key={j}>{point}</li>
                ))}
              </ul>
            </div>
          ))}
          {notes.notes?.summary && (
            <p className="text-gray-300 text-sm mt-3 italic">{notes.notes.summary}</p>
          )}
        </Section>
      )}

      {lesson.next_topics?.length > 0 && (
        <Section title="Upcoming Topics in your Roadmap">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {lesson.next_topics.map((t, i) => (
              <button
                key={i}
                type="button"
                onClick={() => {
                  if (typeof onSelectTopic === 'function') {
                    onSelectTopic(t)
                  } else {
                    window.location.href = `/ai-classroom?topic=${encodeURIComponent(t)}`
                  }
                }}
                className="p-3 bg-gray-700/40 hover:bg-gray-700 border border-gray-600 hover:border-indigo-500 rounded-lg text-left transition group"
              >
                <p className="text-white text-sm font-medium truncate">{t}</p>
                <span className="text-indigo-400 text-xs mt-1 block group-hover:underline">Start Lesson →</span>
              </button>
            ))}
          </div>
        </Section>
      )}
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h4 className="text-lg font-semibold text-white mb-3">{title}</h4>
      {children}
    </div>
  )
}
