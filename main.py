import uuid
import asyncio
from flask import Flask, request, jsonify

from python_a2a import A2AClient, Message, TextContent, MessageRole, Task

app = Flask(__name__)
dify_client = A2AClient("http://127.0.0.1:5010")


@app.route("/")
def index():
    return jsonify({"message": "Dify A2A API", "endpoint": "/dify_query"})


@app.route("/dify_query", methods=["POST"])
def dify_query():
    data = request.json or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "查询内容不能为空"}), 400

    message = Message(content=TextContent(text=query), role=MessageRole.USER)
    task = Task(id=f"task-{uuid.uuid4()}", message=message.to_dict())

    try:
        result_task = asyncio.run(dify_client.send_task_async(task))
    except Exception as e:
        return jsonify({"error": f"调用失败: {e}"}), 502

    if str(result_task.status.state) == "completed":
        try:
            answer = result_task.artifacts[0]["parts"][0]["text"]
            return jsonify({"answer": answer})
        except Exception:
            return jsonify({"error": "返回格式异常"}), 500
    else:
        return jsonify({"error": "调用失败"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)


