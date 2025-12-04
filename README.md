# agent_test

用于测试各种 agent 开发工具

## 项目说明

这是一个基于 Dify A2A (Agent-to-Agent) 协议的智能体测试项目，集成了 Dify 平台的 QA_test 教育AI助手应用。

## 文件说明

- `main.py` - 客户端程序，提供控制台交互界面
- `dify_a2a_server.py` - A2A 服务器，将请求转发到 Dify API
- `QA_test.yml` - Dify 应用 DSL 配置文件（教育AI助手）
- `SETUP.md` - 详细的配置和启动说明

## 快速开始

1. 查看 `SETUP.md` 了解详细配置步骤
2. 创建 `.env` 文件并配置 `DIFY_API_KEY`
3. 启动服务器：`python dify_a2a_server.py`
4. 运行客户端：`python main.py`

## QA_test 应用特性

根据 `QA_test.yml` 配置，该应用是一个**教育AI助手**，支持：
- 📚 教学辅助（面向教师）
- 🎓 学习辅导（面向学生）
- ✅ 作业批改

使用通义千问模型，专注于 K12 教育场景。
