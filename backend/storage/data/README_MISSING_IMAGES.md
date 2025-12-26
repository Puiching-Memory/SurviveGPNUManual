# 缺失图片文件说明

## 问题描述

文档中引用了 116 个图片文件，但本地只有 31 个文件存在，缺失 85 个图片文件。

## 缺失图片列表

所有缺失的图片文件名已保存在 `missing_images.txt` 文件中。

## 解决方案

这些图片原本位于 GitHub 仓库的以下路径：
```
docs/blog/posts/assets/tieba-9839420997/
```

### 方法 1：从 GitHub 下载

1. 访问原 GitHub 仓库：
   - https://github.com/Puiching-Memory/SurviveGPNUManual

2. 下载图片文件：
   - 导航到 `docs/blog/posts/assets/tieba-9839420997/` 目录
   - 下载所有缺失的图片文件
   - 将图片文件放到 `backend/storage/data/assets/shared/` 目录

### 方法 2：使用 Git LFS 克隆

如果仓库使用 Git LFS 存储图片：

```bash
git lfs pull
```

然后将图片文件从相应目录复制到 `backend/storage/data/assets/shared/`。

### 方法 3：批量下载脚本（可选）

可以使用以下 PowerShell 脚本批量下载（需要根据实际 URL 调整）：

```powershell
$baseUrl = "https://raw.githubusercontent.com/Puiching-Memory/SurviveGPNUManual/main/docs/blog/posts/assets/tieba-9839420997/"
$missingFiles = Get-Content "missing_images.txt"
$targetDir = "backend\storage\data\assets\shared"

foreach ($file in $missingFiles) {
    $url = $baseUrl + $file
    $targetPath = Join-Path $targetDir $file
    try {
        Invoke-WebRequest -Uri $url -OutFile $targetPath
        Write-Host "下载成功: $file"
    } catch {
        Write-Warning "下载失败: $file - $_"
    }
}
```

## 验证

下载完成后，可以运行以下命令验证：

```powershell
$missing = Get-Content "missing_images.txt"
$missingCount = 0
foreach ($file in $missing) {
    if (-not (Test-Path "backend\storage\data\assets\shared\$file")) {
        $missingCount++
    }
}
Write-Host "仍缺失的图片数量: $missingCount"
```

