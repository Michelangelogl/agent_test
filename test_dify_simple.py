import requests

# 配置你的 Dify API 信息
API_URL = "https://api.dify.ai/v1/workflows/run"  # 替换为你的 API URL
API_KEY = "your-api-key-here"  # 替换为你的 API Key

# 测试问题
QUERY = "你好，请介绍一下你自己"


def test_dify(api_url, api_key, query):
    """测试 Dify API"""
    resp = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "inputs": {"query": query},
            "user": "test-user",
            "response_mode": "blocking"
        },
        timeout=60
    )
    
    resp.raise_for_status()
    data = resp.json()
    result = data.get("data", {}).get("outputs", {}).get("result", "")
    return result


if __name__ == "__main__":
    print(f"问题: {QUERY}")
    print(f"回复: {test_dify(API_URL, API_KEY, QUERY)}")

