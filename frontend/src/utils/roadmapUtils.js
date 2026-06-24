const ACTIVITY_TYPE_MAP = {
  'new concept learning': 'concept_learning',
  'practice problems': 'practice',
  'review and notes': 'revision',
}

export function inferSessionType(session) {
  if (session?.type) return session.type
  const activity = (session?.activity || '').toLowerCase()
  return ACTIVITY_TYPE_MAP[activity] || 'concept_learning'
}

export function getSessionTopic(session, dayPlan) {
  if (session?.topic) return session.topic
  if (dayPlan?.focus) return dayPlan.focus
  return 'General Review'
}

export function getActionRoute(sessionType, topic) {
  const encoded = encodeURIComponent(topic)
  switch (sessionType) {
    case 'concept_learning':
      return `/ai-classroom?topic=${encoded}`
    case 'practice':
      return `/quiz?topic=${encoded}`
    case 'revision':
      return `/notes/review?topic=${encoded}`
    default:
      return `/ai-classroom?topic=${encoded}`
  }
}

export function getSessionActionLabel(sessionType) {
  switch (sessionType) {
    case 'concept_learning':
      return 'Start Learning'
    case 'practice':
      return 'Practice Now'
    case 'revision':
      return 'Review Notes'
    default:
      return 'Open'
  }
}

export function getTodayPlan(roadmap) {
  if (!roadmap?.daily_plan?.length) return null
  const today = new Date().toISOString().slice(0, 10)
  return roadmap.daily_plan.find((day) => day.date === today) || roadmap.daily_plan[0]
}
