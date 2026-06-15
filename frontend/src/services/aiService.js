import api from './apiService'

const aiService = {
  queryRag: async (query, top_k = 5) => {
    const resp = await api.post('/api/rag/query', { query, top_k })
    return resp.data
  },
  generateRoadmap: async (student_id, syllabus_text = '', datesheet_text = '') => {
    const resp = await api.post('/api/planner/generate_roadmap', { student_id, syllabus_text, datesheet_text })
    return resp.data
  },
  teachConcept: async (student_id, topic, level = 'beginner') => {
    const resp = await api.post('/api/teaching/teach', { student_id, topic, level })
    return resp.data
  },
  generateQuiz: async (student_id, subject_id, difficulty = 'medium') => {
    const resp = await api.post('/api/quiz/generate', { student_id, subject_id, difficulty })
    return resp.data
  },
  submitQuizAnswers: async (quiz_id, answers, questions = []) => {
    const resp = await api.post('/api/quiz/submit', { quiz_id, answers, questions })
    return resp.data
  }
}

export default aiService
