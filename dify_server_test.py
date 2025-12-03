import requests
import json

# 配置你的 Dify API 信息
# 方式1: 如果使用 Workflow API，URL 格式为: https://api.dify.ai/v1/workflows/{workflow_id}/run
# 方式2: 如果使用 Chat API，URL 格式为: https://api.dify.ai/v1/chat-messages
API_URL = "https://api.dify.ai/v1/workflows/run"  # 替换为你的完整 API URL
API_KEY = "app-Ufqq2RgfPrPxVrcMeVGWb6IJ"  # 替换为你的 API Key

# 测试问题
QUERY = "你好，请介绍一下你自己"


def test_dify(api_url, api_key, query):
    """测试 Dify API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 尝试 Workflow API 格式
    payload = {
        "inputs": {"query": query},
        "user": "test-user",
        "response_mode": "blocking"
    }
    
    print(f"📤 请求 URL: {api_url}")
    print(f"📝 问题: {query}")
    print(f"🔑 API Key: {api_key[:10]}...")
    print("-" * 50)
    
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        print(f"📊 状态码: {resp.status_code}")
        print(f"📋 响应头: {dict(resp.headers)}")
        
        if resp.status_code == 401:
            print("❌ 401 未授权错误")
            print("可能的原因:")
            print("1. API Key 不正确或已过期")
            print("2. API URL 不正确（可能需要包含 workflow_id）")
            print("3. 使用了错误的 API 端点")
            print(f"\n响应内容: {resp.text}")
            
            # 尝试 Chat API 格式
            print("\n尝试使用 Chat API 格式...")
            chat_url = "https://api.dify.ai/v1/chat-messages"
            chat_payload = {
                "inputs": {},
                "query": query,
                "user": "test-user",
                "response_mode": "blocking"
            }
            chat_resp = requests.post(chat_url, headers=headers, json=chat_payload, timeout=60)
            print(f"Chat API 状态码: {chat_resp.status_code}")
            if chat_resp.status_code == 200:
                chat_data = chat_resp.json()
                print(f"Chat API 响应: {json.dumps(chat_data, ensure_ascii=False, indent=2)}")
                return chat_data.get("answer", "")
            else:
                print(f"Chat API 响应: {chat_resp.text}")
            
            return None
        
        resp.raise_for_status()
        data = resp.json()
        print(f"✅ 成功响应:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
        
        result = data.get("data", {}).get("outputs", {}).get("result", "")
        if not result:
            result = data.get("answer", "")  # Chat API 格式
        
        return result
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        print(f"响应内容: {resp.text}")
        return None
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    print(f"问题: {QUERY}\n")
    result = test_dify(API_URL, API_KEY, QUERY)
    if result:
        print(f"\n💬 回复: {result}")
    else:
        print("\n❌ 测试失败，请检查 API URL 和 API Key")

