import os
import requests
from dotenv import load_dotenv
from python_a2a import A2AServer, run_server, AgentCard, AgentSkill, TaskStatus, TaskState

load_dotenv()

# Dify API 配置
# 注意：DIFY_API_KEY 应该是你在 Dify 平台中为 QA_test 应用生成的 API Key
DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/chat-messages")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")

# 对话上下文管理（可选）
# 如果希望保持对话上下文，可以启用此功能
ENABLE_CONVERSATION_CONTEXT = os.getenv("ENABLE_CONVERSATION_CONTEXT", "false").lower() == "true"

dify_card = AgentCard(
    name="DifyAgentServer",
    description="将 A2A 请求转发给 Dify 聊天应用（QA_test - 教育AI助手）",
    url="http://127.0.0.1:5010",
    version="1.0.0",
    skills=[AgentSkill(name="dify_chat", description="通过 Dify QA_test 应用进行教育相关的问答对话")],
)


class DifyServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=dify_card)
        # 对话上下文管理：为每个用户维护独立的对话 ID
        self.conversations = {}  # {user_id: conversation_id}

    def _call_dify(self, query: str, user: str = "a2a-user", conversation_id: str = None) -> str:
        """
        调用 Dify chat-messages API
        支持对话上下文管理（可选）
        """
        if not DIFY_API_KEY:
            return "错误：DIFY_API_KEY 未配置。请在 .env 文件中设置 DIFY_API_KEY，或设置环境变量。"

        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "inputs": {},
            "query": query,
            "user": user,
            "response_mode": "blocking",
        }
        
        # 如果启用了对话上下文，添加 conversation_id
        if ENABLE_CONVERSATION_CONTEXT and conversation_id:
            payload["conversation_id"] = conversation_id

        try:
            resp = requests.post(DIFY_API_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            
            # 保存新的 conversation_id（如果返回了新的）
            if ENABLE_CONVERSATION_CONTEXT and "conversation_id" in data:
                self.conversations[user] = data["conversation_id"]
            
            # chat-messages 直接取 answer
            return str(data.get("answer", resp.text))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return f"调用 Dify 出错: 401 未授权。请检查 DIFY_API_KEY 是否正确，确保它是 QA_test 应用的 API Key。"
            return f"调用 Dify 出错: {e}"
        except Exception as e:
            return f"调用 Dify 出错: {e}"

    def handle_task(self, task):
        query = (task.message or {}).get("content", {}).get("text", "")
        if not query.strip():
            result_text = "内容为空"
        else:
            # 获取用户 ID（如果有），用于对话上下文管理
            user_id = task.message.get("role", {}).get("user", "a2a-user") if isinstance(task.message, dict) else "a2a-user"
            conversation_id = self.conversations.get(user_id) if ENABLE_CONVERSATION_CONTEXT else None
            result_text = self._call_dify(query.strip(), user=user_id, conversation_id=conversation_id)

        task.artifacts = [{"parts": [{"type": "text", "text": result_text}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task


if __name__ == "__main__":
    server = DifyServer()
    print(f"[{server.agent_card.name}] 启动成功，服务地址: {server.agent_card.url}")
    run_server(server, host="127.0.0.1", port=5010)