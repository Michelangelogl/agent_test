import uuid
import asyncio
import sys
import time
from python_a2a import A2AClient, Message, TextContent, MessageRole, Task, TaskState

# 注意：这里的地址需要和你启动 DifyServer 时的 host/port 保持一致
dify_client = A2AClient("http://127.0.0.1:5010")


def get_answer(query: str) -> str:
    """获取 Dify Agent 的回答（同步方式）"""
    if not query.strip():
        return "错误：查询内容不能为空"

    # 构造 A2A Task
    message = Message(content=TextContent(text=query), role=MessageRole.USER)
    task = Task(id="task-" + str(uuid.uuid4()), message=message.to_dict())

    try:
        # 异步调用转为同步执行
        result_task = asyncio.run(dify_client.send_task_async(task))
    except Exception as e:
        return f"调用失败: {str(e)}"

    # 处理返回结果
    state_enum = result_task.status.state
    state = str(state_enum)
    if state_enum == TaskState.COMPLETED:
        try:
            # 这里直接返回文本结果，由外层统一负责打印，避免重复输出
            return result_task.artifacts[0]["parts"][0]["text"]
        except Exception:
            return "错误：DifyAgentServer 返回格式异常，未找到文本结果"
    else:
        msg = (result_task.status.message or {}).get("content", {}).get("text", "未指定错误信息")
        return f"状态: {state}, 信息: {msg}"


def main():
    print("=" * 50)
    print("Dify Agent 控制台交互程序 (输入 'exit' 退出)")
    print("=" * 50)

    while True:
        try:
            query = input("\n用户: ").strip()
            if query.lower() == "exit":
                print("已退出程序")
                break
            if not query:
                print("请输入有效问题")
                continue

            print("Dify: ", end="", flush=True)
            answer = get_answer(query)

            # 模拟打字效果（可选）
            for char in answer:
                print(char, end="", flush=True)
                sys.stdout.flush()
                time.sleep(0.02)  # 减慢输出速度，模拟打字
            print("\n")

        except KeyboardInterrupt:
            print("\n程序已中断")
            break
        except Exception as e:
            print(f"程序错误: {str(e)}")


if __name__ == "__main__":
    main()
