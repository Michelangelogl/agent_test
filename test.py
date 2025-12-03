import os
import requests
from dotenv import load_dotenv
from python_a2a import A2AServer, run_server, AgentCard, AgentSkill, TaskStatus, TaskState

# 加载 .env 文件（确保 .env 在项目根目录）
load_dotenv()

# 从环境变量读取配置（推荐方式）
DIFY_API_URL = os.getenv("DIFY_API_URL", "http://localhost/v1/workflows/run")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

# 验证关键配置
if not DIFY_API_KEY:
    raise ValueError("❌ 环境变量 DIFY_API_KEY 未设置！请在 .env 文件中配置。")

dify_card = AgentCard(
    name="DifyAgentServer",
    description="一个将 A2A 请求转发给 Dify 应用的 Agent。",
    url="http://127.0.0.1:5010",
    version="1.0.0",
    skills=[AgentSkill(name="dify_chat", description="通过 Dify 应用进行对话推理")],
)


class DifyServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=dify_card)

    def _call_dify(self, query: str, user: str = "a2a-user") -> str:
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": {"query": query},  # ⚠️ 确保工作流中的输入变量名为 "query"
            "user": user,
            "response_mode": "blocking"
        }

        try:
            print(f"[调试] 正在调用 Dify API: {DIFY_API_URL}")
            print(f"[调试] 请求头: Authorization: Bearer {'*' * len(DIFY_API_KEY)}")
            print(f"[调试] 请求体: {payload}")

            resp = requests.post(
                DIFY_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            # 打印状态码和响应用于调试
            print(f"[调试] Dify 响应状态码: {resp.status_code}")
            print(f"[调试] Dify 响应体: {resp.text}")

            resp.raise_for_status()  # 触发 HTTPError（如 401, 404, 500）
            data = resp.json()

        except requests.exceptions.HTTPError as e:
            # 特别处理 401 错误
            if resp.status_code == 401:
                return "❌ 调用 Dify 失败: 401 Unauthorized —— 请检查 API Key 是否正确且具有 Workflow 权限。"
            else:
                return f"❌ 调用 Dify 失败: HTTP {resp.status_code} - {resp.text}"
        except Exception as e:
            return f"❌ 调用 Dify 时发生异常: {type(e).__name__}: {e}"

        # 安全解析响应
        outputs = data.get("data", {}).get("outputs", {})
        if not outputs:
            return f"⚠️ Dify 返回成功但无 outputs 字段。完整响应: {data}"

        # 假设你的工作流输出变量名为 "result"
        result = outputs.get("result")
        if result is None:
            # 如果不确定输出名，可以返回整个 outputs
            return f"⚠️ 未找到 'result' 字段，outputs 内容: {outputs}"

        return str(result)

    def handle_task(self, task):
        print("收到 A2A 任务 task =>", task)
        query = (task.message or {}).get("content", {}).get("text", "")
        print(f"[{self.agent_card.name} 日志] 收到 A2A 任务: '{query}'")

        if not query.strip():
            result_text = "❌ 任务中未提供有效文本内容。"
        else:
            result_text = self._call_dify(query=query)

        # 更新任务结果
        task.artifacts = [{"parts": [{"type": "text", "text": result_text}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        print(f"[{self.agent_card.name} 日志] 任务处理完毕")
        return task


if __name__ == "__main__":
    server = DifyServer()
    print(f"[{server.agent_card.name}] 启动成功，服务地址: {server.agent_card.url}")
    run_server(server, host="127.0.0.1", port=5010)