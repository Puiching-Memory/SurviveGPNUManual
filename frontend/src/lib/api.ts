const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Handle 401 errors by redirecting to login
export function handleUnauthorized() {
  // Clear token and redirect to login
  localStorage.removeItem('token')
  // Dispatch logout event to update auth context
  window.dispatchEvent(new CustomEvent('auth:logout'))
  // Only redirect if not already on login page
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

// Global fetch wrapper that handles 401 errors
export async function apiFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = localStorage.getItem('token')
  
  // Add authorization header if token exists
  const headers = new Headers(options.headers)
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  })
  
  // Handle 401 errors globally
  if (response.status === 401) {
    handleUnauthorized()
    throw new Error('认证已过期，请重新登录')
  }
  
  return response
}

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    // Handle 401 Unauthorized - token expired or invalid
    if (response.status === 401) {
      handleUnauthorized()
      throw new Error('认证已过期，请重新登录')
    }
    
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || `HTTP error! status: ${response.status}`)
  }
  return response.json()
}

// Filesystem Document API (直接从文件系统读取)
export const documentApi = {
  async list(params?: {
    category?: string
    tags?: string
    published?: boolean
    skip?: number
    limit?: number
  }): Promise<any[]> {
    const queryParams = new URLSearchParams()
    if (params?.category) queryParams.append('category', params.category)
    if (params?.tags) queryParams.append('tags', params.tags)
    if (params?.published !== undefined) queryParams.append('published', String(params.published))
    if (params?.skip) queryParams.append('skip', String(params.skip))
    if (params?.limit) queryParams.append('limit', String(params.limit))

    const response = await apiFetch(`${API_URL}/api/filesystem-documents?${queryParams}`)
    const data = await handleResponse<{ documents: any[]; total: number }>(response)
    return data.documents || []
  },

  async getBySlug(slug: string): Promise<any> {
    const response = await apiFetch(`${API_URL}/api/filesystem-documents/${slug}`)
    return handleResponse(response)
  },

  async getContent(slug: string): Promise<string> {
    const response = await apiFetch(`${API_URL}/api/filesystem-documents/${slug}/content`)
    if (!response.ok) {
      throw new Error('Failed to fetch content')
    }
    return response.text()
  },

  async create(data: any): Promise<any> {
    const response = await apiFetch(`${API_URL}/api/documents`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    })
    return handleResponse(response)
  },

  async update(id: string, data: any): Promise<any> {
    const response = await apiFetch(`${API_URL}/api/documents/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    })
    return handleResponse(response)
  },

  async delete(id: string): Promise<void> {
    const response = await apiFetch(`${API_URL}/api/documents/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    })
    if (!response.ok) {
      throw new Error('Failed to delete document')
    }
  },
}


