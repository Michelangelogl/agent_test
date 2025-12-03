import requests
import json


def test_dify_api(api_url: str, api_key: str, query: str, user: str = "test-user"):
    """
    测试 Dify 智能体 API
    
    参数:
        api_url: Dify API 地址 (例如: https://api.dify.ai/v1/workflows/run)
        api_key: Dify API Key
        query: 要发送的问题
        user: 用户标识 (可选)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "inputs": {"query": query},
        "user": user,
        "response_mode": "blocking"
    }
    
    print(f"📤 发送请求到: {api_url}")
    print(f"📝 问题: {query}")
    print("-" * 50)
    
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        
        data = resp.json()
        print(f"✅ 状态码: {resp.status_code}")
        print(f"📋 完整响应:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
        print("-" * 50)
        
        # 尝试提取结果
        result = data.get("data", {}).get("outputs", {}).get("result", "")
        if result:
            print(f"💬 回复: {result}")
        else:
            print("⚠️  未找到 result 字段，请检查 outputs 结构")
            
        return data
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        print(f"响应内容: {resp.text}")
        return None
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    # 在这里填入你的 Dify API 信息
    API_URL = input("请输入 Dify API URL: ").strip()
    API_KEY = input("请输入 Dify API Key: ").strip()
    QUERY = input("请输入测试问题: ").strip()
    
    if not all([API_URL, API_KEY, QUERY]):
        print("❌ 信息不完整，请重新运行")
    else:
        test_dify_api(API_URL, API_KEY, QUERY)


