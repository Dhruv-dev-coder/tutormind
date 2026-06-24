import api from './apiService'

export async function loadRoadmap() {
  const user = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
  if (user.student_id) {
    try {
      const resp = await api.get(`/api/roadmap/${user.student_id}`)
      if (resp.data?.roadmap) {
        sessionStorage.setItem('tutormind_roadmap', JSON.stringify(resp.data.roadmap))
        return resp.data.roadmap
      }
    } catch {
      // fall through to session storage
    }
  }

  const stored = sessionStorage.getItem('tutormind_roadmap')
  return stored ? JSON.parse(stored) : null
}
