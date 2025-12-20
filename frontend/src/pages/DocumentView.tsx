import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { documentApi } from '../lib/api'
import { Document } from '../types/document'
import { useAuth } from '../context/AuthContext'
import { Spinner } from '../components/ui/Spinner'
import { Button } from '../components/ui/Button'

export default function DocumentView() {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuth()
  const [document, setDocument] = useState<Document | null>(null)
  const [content, setContent] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const isAdmin = user?.role === 'admin' || user?.role === 'superuser'

  useEffect(() => {
    if (slug) {
      loadDocument()
    }
  }, [slug])

  const loadDocument = async () => {
    try {
      setLoading(true)
      const [doc, contentData] = await Promise.all([
        documentApi.getBySlug(slug!),
        documentApi.getContent(slug!),
      ])
      setDocument(doc)
      setContent(contentData.content)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载文档失败')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Spinner />
      </div>
    )
  }

  if (error || !document) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error || '文档未找到'}</p>
        <Link to="/docs" className="mt-4 inline-block text-blue-500 hover:underline">
          返回文档列表
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <Link to="/docs" className="text-blue-500 hover:underline mb-4 inline-block">
            ← 返回文档列表
          </Link>
          <h1 className="text-4xl font-bold mb-4">{document.title}</h1>
          {document.category && (
            <span className="inline-block px-3 py-1 bg-gray-200 rounded-full text-sm mb-4">
              {document.category}
            </span>
          )}
          {document.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {document.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
        {isAdmin && (
          <Button
            onClick={() => navigate(`/docs/${document.id}/edit`)}
            variant="outline"
          >
            编辑
          </Button>
        )}
      </div>

      <div className="prose prose-lg max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>

      {document.relations.length > 0 && (
        <div className="mt-8 pt-6 border-t">
          <h3 className="text-xl font-semibold mb-4">相关文档</h3>
          <ul className="space-y-2">
            {document.relations.map((relation, idx) => (
              <li key={idx}>
                <Link
                  to={`/docs/${relation.target_slug}`}
                  className="text-blue-500 hover:underline"
                >
                  {relation.description || relation.target_slug}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="text-sm text-gray-500 pt-4 border-t">
        最后更新: {new Date(document.updated_at).toLocaleString('zh-CN')}
      </div>
    </div>
  )
}

