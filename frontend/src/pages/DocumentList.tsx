import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { documentApi } from '../lib/api'
import { Document } from '../types/document'
import { Card } from '../components/ui/Card'
import { Spinner } from '../components/ui/Spinner'

export default function DocumentList() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [category, setCategory] = useState<string>('')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadDocuments()
  }, [category])

  const loadDocuments = async () => {
    try {
      setLoading(true)
      const data = await documentApi.list({
        category: category || undefined,
        published: true,
      })
      setDocuments(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载文档失败')
    } finally {
      setLoading(false)
    }
  }

  const filteredDocuments = documents.filter((doc) => {
    if (!searchTerm) return true
    const term = searchTerm.toLowerCase()
    return (
      doc.title.toLowerCase().includes(term) ||
      doc.content_summary?.toLowerCase().includes(term) ||
      doc.tags.some((tag) => tag.toLowerCase().includes(term))
    )
  })

  const categories = Array.from(new Set(documents.map((d) => d.category).filter(Boolean)))

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Spinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error}</p>
        <button
          onClick={loadDocuments}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          重试
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <h1 className="text-3xl font-bold">文档</h1>
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="搜索文档..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">所有分类</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {/* Document Grid */}
      {filteredDocuments.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>暂无文档</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocuments.map((doc) => (
            <Link key={doc.id} to={`/docs/${doc.slug}`}>
              <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{doc.title}</h3>
                  {doc.content_summary && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {doc.content_summary}
                    </p>
                  )}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {doc.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="text-xs text-gray-500">
                    更新于 {new Date(doc.updated_at).toLocaleDateString('zh-CN')}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

