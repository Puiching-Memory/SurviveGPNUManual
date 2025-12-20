"""
该脚本用于删除 GitHub 仓库中的所有部署
使用前请确保设置了环境变量 GITHUB_TOKEN
powershell $env:GITHUB_TOKEN = "your_token_here"
cmd set GITHUB_TOKEN=your_token_here
"""

import os
import requests

REQUEST_TIMEOUT = 10


def _format_request_error(exc):
    response = getattr(exc, "response", None)
    status_code = response.status_code if response else "unknown"
    error_body = response.text if response else "No response body"
    return f"{status_code} {error_body}"

def main():
    owner = "Puiching-Memory"
    repo = "SurviveGPNUManual"
    token = os.getenv("GITHUB_TOKEN")
    assert token is not None

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }

    # 获取部署列表
    url = f"https://api.github.com/repos/{owner}/{repo}/deployments"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"获取部署列表失败: {_format_request_error(exc)}") from exc
    deployments = response.json()

    for deployment in deployments:
        deployment_id = deployment['id']
        print(f"处理部署 {deployment_id}")
        print("="*80)

        # 将部署标记为非活动以允许删除
        status_url = f"https://api.github.com/repos/{owner}/{repo}/deployments/{deployment_id}/statuses"
        print(f"将部署 {deployment_id} 标记为非活动状态")
        try:
            status_response = requests.post(
                status_url, headers=headers, json={"state": "inactive"}, timeout=REQUEST_TIMEOUT
            )
            status_response.raise_for_status()
        except requests.RequestException as exc:
            print(f"标记部署 {deployment_id} 为非活动状态失败: {_format_request_error(exc)}")
            continue

        # 删除部署
        delete_url = f"https://api.github.com/repos/{owner}/{repo}/deployments/{deployment_id}"
        print(f"尝试删除部署 {deployment_id}")

        try:
            delete_response = requests.delete(delete_url, headers=headers, timeout=REQUEST_TIMEOUT)
            delete_response.raise_for_status()
        except requests.RequestException as exc:
            print(f"删除部署 {deployment_id} 失败: {_format_request_error(exc)}")
            continue
        print(f"部署 {deployment_id} 删除成功")

if __name__ == "__main__":
    main()
