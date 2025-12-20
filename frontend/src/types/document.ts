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
  id: string
  slug: string
  title: string
  file_path: string
  category?: string | null
  content_summary?: string | null
  author_id?: number | null
  published: boolean
  tags: string[]
  relations: DocumentRelation[]
  extra_metadata: Record<string, any>
  created_at: string
  updated_at: string
}

export interface DocumentContent {
  content: string
}

export interface PackageExportedBy {
  user_id: number
  email: string
  username: string
}

export interface PackageInfo {
  name?: string
  description?: string
  version?: string
}

export interface PackageStatistics {
  total_documents: number
  total_assets: number
  total_attachments: number
}

export interface DocumentInManifest {
  id: string
  file_path: string
  slug: string
  title: string
  category?: string | null
  tags: string[]
  authors: DocumentAuthor[]
  created_at?: string
  updated_at?: string
  published: boolean
  frontmatter: Record<string, any>
  relations: DocumentRelation[]
  assets: string[]
  attachments: string[]
}

export interface DocumentPackageManifest {
  format_version: string
  format_spec?: string
  exported_at: string
  exported_by: PackageExportedBy
  package_info?: PackageInfo
  statistics?: PackageStatistics
  documents: DocumentInManifest[]
}

export interface ImportOptions {
  conflict_strategy: 'skip' | 'overwrite' | 'rename'
  import_assets: boolean
  import_attachments: boolean
}

export interface ImportResult {
  success: boolean
  total: number
  imported: number
  skipped: number
  failed: number
  errors: string[]
}

export interface ValidationResult {
  valid: boolean
  error?: string
}

