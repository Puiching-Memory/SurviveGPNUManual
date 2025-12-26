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
  const { user } = useAuth()
  const [document, setDocument] = useState<Document | null>(null)
  const [content, setContent] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const isAdmin = user?.role === 'admin' || user?.is_superuser === true

  useEffect(() => {
    if (slug) {
      loadDocument()
    }
  }, [slug])

  const loadDocument = async () => {
    try {
      setLoading(true)
      const [doc, contentText] = await Promise.all([
        documentApi.getBySlug(slug!),
        documentApi.getContent(slug!),
      ])
      setDocument(doc)
      setContent(contentText)
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
          {document.tags && document.tags.length > 0 && (
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
            onClick={() => navigate(`/docs/${document.slug}/edit`)}
            variant="outline"
          >
            编辑
          </Button>
        )}
      </div>

      <div className="prose prose-lg max-w-none markdown-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            table: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <div className="overflow-x-auto my-4 -mx-4 px-4">
                <table className="w-full border-collapse border border-border rounded-lg" {...props}>
                  {children}
                </table>
              </div>
            ),
            thead: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <thead className="bg-muted" {...props}>
                {children}
              </thead>
            ),
            tbody: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <tbody {...props}>
                {children}
              </tbody>
            ),
            tr: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <tr className="border-b border-border hover:bg-muted/50 transition-colors" {...props}>
                {children}
              </tr>
            ),
            th: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <th className="border border-border px-4 py-2 text-left font-semibold bg-muted" {...props}>
                {children}
              </th>
            ),
            td: ({ children, ...props }: { children?: React.ReactNode; [key: string]: any }) => (
              <td className="border border-border px-4 py-2" {...props}>
                {children}
              </td>
            ),
            img: ({ src, alt, ...props }: { src?: string; alt?: string; [key: string]: any }) => {
              // 转换图片路径为完整的 API URL
              const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
              let imageSrc = src || ''
              
              if (!src) {
                return <img src="" alt={alt || ''} {...props} className="max-w-full h-auto" />
              }
              
              // 处理 HTTP/HTTPS 外部链接（保持原样）
              if (src.startsWith('http://') || src.startsWith('https://')) {
                imageSrc = src
              }
              // 处理 /api 开头的路径（直接转换为完整 URL）
              else if (src.startsWith('/api')) {
                imageSrc = `${apiUrl}${src}`
              }
              // 处理相对路径 ./ 或 ../
              else if (src.startsWith('./') || src.startsWith('../')) {
                // 移除 ./ 或 ../ 前缀，转换为共享资源路径
                const filename = src.replace(/^\.\.?\//, '')
                imageSrc = `${apiUrl}/api/documents/assets/shared/${filename}`
              }
              // 处理其他路径（文件名或路径）
              else if (!src.startsWith('/')) {
                // 直接文件名或相对路径，转换为共享资源路径
                imageSrc = `${apiUrl}/api/documents/assets/shared/${src}`
              }
              // 处理绝对路径（以 / 开头但不是 /api）
              else {
                // 其他绝对路径，尝试转换为共享资源路径
                const filename = src.replace(/^\//, '')
                imageSrc = `${apiUrl}/api/documents/assets/shared/${filename}`
              }
              
              return (
                <img
                  src={imageSrc}
                  alt={alt || ''}
                  {...props}
                  className="max-w-full h-auto"
                  onError={(e) => {
                    // 图片加载失败时的处理
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                    console.warn(`Failed to load image: ${imageSrc}`)
                  }}
                />
              )
            },
          }}
        >
          {content}
        </ReactMarkdown>
      </div>

      {document.relations && document.relations.length > 0 && (
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

