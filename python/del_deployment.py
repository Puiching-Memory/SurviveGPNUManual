"""
该脚本用于删除 GitHub 仓库中的所有部署
使用前请确保设置了环境变量 GITHUB_TOKEN
powershell $env:GITHUB_TOKEN = "your_token_here"
cmd set GITHUB_TOKEN=your_token_here
"""

import os
import requests

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
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    deployments = response.json()

    for index,deployment in enumerate(deployments):
        print(deployment)
        print("="*80)
        deployment_id = deployment['id']

        # 将部署标记为非活动以允许删除
        status_url = f"https://api.github.com/repos/{owner}/{repo}/deployments/{deployment_id}/statuses"
        status_response = requests.post(status_url, headers=headers, json={"state": "inactive"})
        try:
            status_response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(f"标记部署 {deployment_id} 为 inactive 失败") from exc

        # 删除部署
        delete_url = f"https://api.github.com/repos/{owner}/{repo}/deployments/{deployment_id}"
        print(f"尝试删除 Deployment {deployment_id}")

        delete_response = requests.delete(delete_url, headers=headers)
        delete_response.raise_for_status()

if __name__ == "__main__":
    main()
