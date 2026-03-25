# learnpathlyLangChain

基于 `LangChain + LangGraph` 的学习路径生成服务，按“意图解析 → 路径规划 → 多源检索 → 重排校验 → 结构化生成”执行。

## 功能
- 结构化意图解析（目标、水平、偏好、语言）
- 分阶段学习路径规划（3~8 节点）
- 多源资源检索（YouTube / GitHub / Web）
- 资源重排与基础质量校验
- 输出稳定 JSON，便于前端直接渲染

## 快速开始
1. 安装依赖
   ```bash
   pip install -e .
   ```
2. 配置环境变量
   ```bash
   cp .env.example .env
   ```
   在 `.env` 中至少配置以下 Key 才会走真实 API：
   - `OPENAI_API_KEY`（用于意图解析/路径规划/最终生成）
   - `OPENAI_BASE_URL`（使用非 OpenAI 服务时必填，见下表）
   - `MODEL_INTENT` / `MODEL_PLANNER` / `MODEL_GENERATOR`（模型名）
   - `YOUTUBE_API_KEY`（YouTube Data API v3，可选）
   - `TAVILY_API_KEY`（Web 搜索，可选）
   - `GITHUB_TOKEN`（GitHub 仓库搜索，可选）

   **支持的 LLM 提供商：**

   | 提供商 | OPENAI_BASE_URL | 模型名示例 |
   |--------|-----------------|------------|
   | MiniMax（国内） | `https://api.minimax.chat/v1` | `abab6.5s-chat` |
   | DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
   | OpenAI | （留空） | `gpt-4o-mini` |

   > **MiniMax 注意**：端点必须使用 `api.minimax.chat`，`api.minimax.io` 为国际版，key 不通用。推理模型（MiniMax-M2.5）会输出 `<think>` 标签，建议使用 `abab6.5s-chat`。
3. 启动服务
   ```bash
   uvicorn app:app --reload
   ```
4. 调用接口
   ```bash
   curl -X POST http://127.0.0.1:8000/v1/learning-path \
     -H "Content-Type: application/json" \
     -d '{"query":"我想系统学习 LLM，并做出可上线应用"}'
   ```

## 模拟真实用户输入
- 命令行直调：
  ```bash
  python main.py --query "我是前端工程师，想在 6 周内学会 LangChain + RAG 并上线一个问答助手"
  ```
- 多组真实输入压测：
  ```bash
  curl -X POST http://127.0.0.1:8000/v1/learning-path \
    -H "Content-Type: application/json" \
    -d '{"query":"我零基础，想学 Python 做数据分析，平时每天 1 小时"}'

  curl -X POST http://127.0.0.1:8000/v1/learning-path \
    -H "Content-Type: application/json" \
    -d '{"query":"我会 Java，想转 AI 应用开发，重点学习 Agent 与评估体系"}'
  ```

## 项目结构
- `app.py`: FastAPI 入口
- `learnpathly_langchain/graph.py`: LangGraph 编排
- `learnpathly_langchain/chains/`: Intent/Planner/Generator
- `learnpathly_langchain/tools/`: 资源检索工具
- `learnpathly_langchain/retrieval.py`: 聚合检索与重排
- `learnpathly_langchain/validation.py`: 规则校验

## 说明
- 若未配置外部 API Key，检索会自动降级为 mock 数据，便于本地调试。
- 已支持真实 API 检索（YouTube / GitHub / Tavily），并在请求失败时自动回退 mock。
- 生产建议将检索结果加上 Redis 缓存。
