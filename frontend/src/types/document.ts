export interface DocumentAuthor {
  user_id?: number
  username?: string
  email?: string
}

export interface DocumentRelation {
  type: 'references' | 'related' | 'parent' | 'child'
  target_slug: string
  description?: string
}

export interface Document {
  id?: string  // 可选，文件系统文档可能没有 id
  slug: string
  title: string
  file_path: string
  category?: string | null
  description?: string | null
  content_summary?: string | null  // 兼容旧字段
  content_preview?: string | null  // 文件系统文档的预览
  author_id?: number | null
  published: boolean
  tags?: string[]  // 可选，文件系统文档可能为空数组
  relations?: DocumentRelation[]  // 可选
  extra_metadata?: Record<string, any>  // 可选
  frontmatter?: Record<string, any>  // 文件系统文档的前置元数据
  content?: string  // 完整内容（仅在详情页时存在）
  created_at: string
  updated_at: string
}

export interface DocumentContent {
  content: string
}


