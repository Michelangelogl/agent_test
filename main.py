import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from python_a2a import A2AClient, Message, TextContent, MessageRole, Task


app = FastAPI(
    title="Dify A2A API",
    description="通过 A2A 协议调用 DifyAgentServer 的 HTTP 接口",
)

# 注意：这里的地址需要和你启动 DifyServer 时的 host/port 保持一致
dify_client = A2AClient("http://127.0.0.1:5010")


class DifyQueryRequest(BaseModel):
    query: str


class DifyQueryResponse(BaseModel):
    answer: str


@app.post("/dify_query", response_model=DifyQueryResponse)
async def dify_query(body: DifyQueryRequest):
    """
    调用 DifyAgentServer 的简单 HTTP 接口：
    - 请求体：{"query": "你的问题"}
    - 返回：{"answer": "Dify 的回复文本"}
    """
    query = body.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="查询内容不能为空")

    # 构造 A2A Task
    message = Message(content=TextContent(text=query), role=MessageRole.USER)
    task = Task(id="task-" + str(uuid.uuid4()), message=message.to_dict())

    try:
        # 调用 Dify A2A Server
        result_task = await dify_client.send_task_async(task)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用 DifyAgentServer 失败: {e}")

    # 处理返回结果
    state = str(result_task.status.state)
    if state == "completed":
        try:
            answer = result_task.artifacts[0]["parts"][0]["text"]
        except Exception:
            raise HTTPException(status_code=500, detail="DifyAgentServer 返回格式异常，未找到文本结果")
        return DifyQueryResponse(answer=answer)
    else:
        # 其它状态：input-required / failed 等，统一转为错误信息
        msg = (result_task.status.message or {}).get("content", {}).get("text", "DifyAgentServer 调用失败")
        raise HTTPException(status_code=500, detail=f"状态: {state}, 信息: {msg}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010)


