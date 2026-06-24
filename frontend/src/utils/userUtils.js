export function getStudentId() {
  try {
    const user = JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
    return user.student_id || null
  } catch {
    return null
  }
}

export function getUserInfo() {
  try {
    return JSON.parse(sessionStorage.getItem('tutormind_user') || '{}')
  } catch {
    return {}
  }
}
