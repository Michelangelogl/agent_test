# 配置说明

## 问题：401 Unauthorized 错误

出现此错误是因为缺少 Dify API Key 配置。

## 解决步骤

### 1. 了解应用配置

项目包含 `QA_test.yml` DSL 配置文件，这是一个**教育AI助手**应用，具有以下特点：
- **应用名称**: QA_test
- **模型**: 通义千问 (qvq-max-latest)
- **功能**: 教学辅助、学习辅导、作业批改
- **模式**: 聊天模式

### 2. 创建 `.env` 文件

在项目根目录创建 `.env` 文件，内容如下：

```env
# Dify API Key（必需）
# 注意：这个 API Key 必须是从 QA_test 应用生成的
DIFY_API_KEY=your_dify_api_key_here

# Dify API URL（可选，默认使用官方 API）
# DIFY_API_URL=https://api.dify.ai/v1/chat-messages

# 是否启用对话上下文（可选，默认 false）
# 启用后，同一用户的对话会保持上下文连贯性
ENABLE_CONVERSATION_CONTEXT=false
```

### 3. 获取 Dify API Key

**重要**：API Key 必须是从 **QA_test** 应用生成的，不是平台通用的 API Key。

1. 访问 https://dify.ai
2. 登录你的账号
3. 进入 **QA_test** 应用（如果还没有，需要先导入 `QA_test.yml` 创建应用）
4. 进入应用的 **API 访问** 或 **设置** 页面
5. 生成并复制该应用的 **API Key**
6. 将 API Key 粘贴到 `.env` 文件中的 `DIFY_API_KEY=` 后面

### 4. 导入应用配置（如果需要）

如果你还没有在 Dify 平台创建 QA_test 应用：

1. 登录 Dify 平台
2. 进入应用管理
3. 选择导入应用
4. 上传 `QA_test.yml` 文件
5. 导入后，在应用设置中生成 API Key

### 5. 启动服务

**第一步：启动 Dify A2A 服务器**
```bash
python dify_a2a_server.py
```

看到以下输出表示启动成功：
```
[DifyAgentServer] 启动成功，服务地址: http://127.0.0.1:5010
```

**第二步：在另一个终端运行客户端**
```bash
python main.py
```

## 功能说明

### 对话上下文（可选）

如果启用 `ENABLE_CONVERSATION_CONTEXT=true`，服务器会为每个用户维护独立的对话上下文，使对话更加连贯。

### 应用特性

根据 `QA_test.yml` 配置，该应用：
- 专注于教育领域（K12）
- 支持教学辅助、学习辅导、作业批改
- 使用通义千问模型
- 启用了检索资源功能

## 注意事项

- 确保 `dify_a2a_server.py` 在运行 `main.py` 之前已经启动
- `.env` 文件应该放在项目根目录（与 `main.py` 同级）
- 不要将 `.env` 文件提交到版本控制系统（已包含在 .gitignore 中）
- **API Key 必须匹配应用**：确保使用的是 QA_test 应用的 API Key，而不是其他应用的

