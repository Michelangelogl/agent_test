import os
import requests
from dotenv import load_dotenv
from python_a2a import A2AServer, run_server, AgentCard, AgentSkill, TaskStatus, TaskState

load_dotenv()

# 预研环境：只考虑「聊天应用 / chat-messages」这一种情况
DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/chat-messages")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")

dify_card = AgentCard(
    name="DifyAgentServer",
    description="简单版：把 A2A 请求转发给 Dify 聊天应用。",
    url="http://127.0.0.1:5010",
    version="1.0.0",
    skills=[AgentSkill(name="dify_chat", description="通过 Dify 聊天应用对话")],
)


class DifyServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=dify_card)

    def _call_dify(self, query: str, user: str = "a2a-user") -> str:
        """最简版：只调用 chat-messages，拿 answer 字段"""
        if not DIFY_API_KEY:
            return "DIFY_API_KEY 未配置"

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

        try:
            resp = requests.post(DIFY_API_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # chat-messages 直接取 answer
            return str(data.get("answer", resp.text))
        except Exception as e:
            return f"调用 Dify 出错: {e}"

    def handle_task(self, task):
        query = (task.message or {}).get("content", {}).get("text", "")
        result_text = self._call_dify(query.strip()) if query.strip() else "内容为空"

        task.artifacts = [{"parts": [{"type": "text", "text": result_text}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task


if __name__ == "__main__":
    server = DifyServer()
    print(f"[{server.agent_card.name}] 启动成功，服务地址: {server.agent_card.url}")
    run_server(server, host="127.0.0.1", port=5010)