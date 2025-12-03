import os
import requests
from dotenv import load_dotenv
from python_a2a import A2AServer, run_server, AgentCard, AgentSkill, TaskStatus, TaskState

load_dotenv()

DIFY_API_URL = os.getenv("DIFY_API_URL", " ")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

if not DIFY_API_KEY:
    raise ValueError("DIFY_API_KEY 未设置")

dify_card = AgentCard(
    name="DifyAgentServer",
    description="将 A2A 请求转发给 Dify 应用",
    url="http://127.0.0.1:5010",
    version="1.0.0",
    skills=[AgentSkill(name="dify_chat", description="通过 Dify 应用进行对话推理")],
)


class DifyServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=dify_card)

    def _call_dify(self, query: str) -> str:
        try:
            resp = requests.post(
                DIFY_API_URL,
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": {"query": query},
                    "user": "a2a-user",
                    "response_mode": "blocking"
                },
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            return str(data.get("data", {}).get("outputs", {}).get("result", ""))
        except Exception as e:
            return f"错误: {e}"

    def handle_task(self, task):
        query = (task.message or {}).get("content", {}).get("text", "")
        result = self._call_dify(query) if query.strip() else "未提供有效文本内容"

        task.artifacts = [{"parts": [{"type": "text", "text": result}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task

if __name__ == "__main__":
    server = DifyServer()
    print(f"启动成功: {server.agent_card.url}")
    run_server(server, host="127.0.0.1", port=5010)