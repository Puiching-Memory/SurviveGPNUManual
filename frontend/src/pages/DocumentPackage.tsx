import { useState } from 'react'
import { packageApi } from '../lib/api'
import { ImportResult, ImportOptions } from '../types/document'
import { Button } from '../components/ui/Button'
import { Spinner } from '../components/ui/Spinner'

export default function DocumentPackage() {
  const [importFile, setImportFile] = useState<File | null>(null)
  const [importOptions, setImportOptions] = useState<ImportOptions>({
    conflict_strategy: 'skip',
    import_assets: true,
    import_attachments: true,
  })
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<ImportResult | null>(null)
  const [exporting, setExporting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImportFile(file)
      setImportResult(null)
      setError(null)
    }
  }

  const handleImport = async () => {
    if (!importFile) {
      setError('请选择文件')
      return
    }

    try {
      setImporting(true)
      setError(null)
      const result = await packageApi.importPackage(importFile, importOptions)
      setImportResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : '导入失败')
    } finally {
      setImporting(false)
    }
  }

  const handleExport = async () => {
    try {
      setExporting(true)
      setError(null)
      const blob = await packageApi.exportPackage()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `documents-${new Date().toISOString().split('T')[0]}.gpnu`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err instanceof Error ? err.message : '导出失败')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">文档包管理</h1>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
          {error}
        </div>
      )}

      {/* Import Section */}
      <div className="p-6 border rounded-lg space-y-4">
        <h2 className="text-2xl font-semibold">导入文档包</h2>

        <div>
          <label className="block text-sm font-medium mb-2">选择 .gpnu 文件</label>
          <input
            type="file"
            accept=".gpnu"
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-2">冲突处理策略</label>
            <select
              value={importOptions.conflict_strategy}
              onChange={(e) =>
                setImportOptions({
                  ...importOptions,
                  conflict_strategy: e.target.value as 'skip' | 'overwrite' | 'rename',
                })
              }
              className="w-full px-4 py-2 border rounded-md"
            >
              <option value="skip">跳过已存在的文档</option>
              <option value="overwrite">覆盖已存在的文档</option>
              <option value="rename">重命名新文档</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="import_assets"
              checked={importOptions.import_assets}
              onChange={(e) =>
                setImportOptions({ ...importOptions, import_assets: e.target.checked })
              }
            />
            <label htmlFor="import_assets">导入资源文件</label>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="import_attachments"
              checked={importOptions.import_attachments}
              onChange={(e) =>
                setImportOptions({ ...importOptions, import_attachments: e.target.checked })
              }
            />
            <label htmlFor="import_attachments">导入附件</label>
          </div>
        </div>

        <Button onClick={handleImport} disabled={!importFile || importing}>
          {importing ? (
            <>
              <Spinner className="mr-2" />
              导入中...
            </>
          ) : (
            '导入'
          )}
        </Button>

        {importResult && (
          <div
            className={`p-4 rounded-md ${
              importResult.success
                ? 'bg-green-50 border border-green-200 text-green-800'
                : 'bg-yellow-50 border border-yellow-200 text-yellow-800'
            }`}
          >
            <h3 className="font-semibold mb-2">导入结果</h3>
            <div className="space-y-1 text-sm">
              <p>总计: {importResult.total}</p>
              <p>成功: {importResult.imported}</p>
              <p>跳过: {importResult.skipped}</p>
              <p>失败: {importResult.failed}</p>
              {importResult.errors.length > 0 && (
                <div className="mt-2">
                  <p className="font-semibold">错误:</p>
                  <ul className="list-disc list-inside">
                    {importResult.errors.map((err, idx) => (
                      <li key={idx}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Export Section */}
      <div className="p-6 border rounded-lg space-y-4">
        <h2 className="text-2xl font-semibold">导出文档包</h2>
        <p className="text-gray-600">导出所有文档为 .gpnu 格式的压缩包</p>
        <Button onClick={handleExport} disabled={exporting}>
          {exporting ? (
            <>
              <Spinner className="mr-2" />
              导出中...
            </>
          ) : (
            '导出文档包'
          )}
        </Button>
      </div>
    </div>
  )
}

