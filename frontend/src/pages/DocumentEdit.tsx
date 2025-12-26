import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { documentApi } from '../lib/api'
import { Document } from '../types/document'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/input'
import { Spinner } from '../components/ui/Spinner'

export default function DocumentEdit() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [document, setDocument] = useState<Document | null>(null)
  const [content, setContent] = useState('')
  const [title, setTitle] = useState('')
  const [slug, setSlug] = useState('')
  const [category, setCategory] = useState('')
  const [tags, setTags] = useState<string[]>([])
  const [tagInput, setTagInput] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      loadDocument()
    }
  }, [id])

  const loadDocument = async () => {
    try {
      setLoading(true)
      const doc = await documentApi.getBySlug(id!)
      const contentText = await documentApi.getContent(id!)
      setDocument(doc)
      setTitle(doc.title)
      setSlug(doc.slug)
      setCategory(doc.category || '')
      setTags(doc.tags || [])
      setContent(contentText)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载文档失败')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!document || !document.id) {
      setError('文档 ID 不存在')
      return
    }

    try {
      setSaving(true)
      setError(null)

      // Update document metadata
      await documentApi.update(document.id, {
        title,
        slug,
        category: category || null,
        tags,
      })

      // Update content (this would need a separate endpoint or be included in update)
      // For now, we'll just update metadata
      navigate(`/docs/${slug}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : '保存文档失败')
    } finally {
      setSaving(false)
    }
  }

  const handleAddTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()])
      setTagInput('')
    }
  }

  const handleRemoveTag = (tag: string) => {
    setTags(tags.filter((t) => t !== tag))
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Spinner />
      </div>
    )
  }

  if (error && !document) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error}</p>
        <Button onClick={() => navigate('/docs')} className="mt-4">
          返回文档列表
        </Button>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">编辑文档</h1>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => navigate(`/docs/${document?.slug}`)}>
            取消
          </Button>
          <Button onClick={handleSave} disabled={saving}>
            {saving ? '保存中...' : '保存'}
          </Button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">标题</label>
          <Input value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Slug</label>
          <Input value={slug} onChange={(e) => setSlug(e.target.value)} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">分类</label>
          <Input value={category} onChange={(e) => setCategory(e.target.value)} />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">标签</label>
          <div className="flex gap-2 mb-2">
            <Input
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddTag()}
              placeholder="输入标签后按回车"
            />
            <Button onClick={handleAddTag} size="sm">
              添加
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm flex items-center gap-2"
              >
                {tag}
                <button
                  onClick={() => handleRemoveTag(tag)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">内容</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full min-h-[400px] px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
          />
        </div>
      </div>
    </div>
  )
}

