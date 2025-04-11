# 🧠 MCP 聚合工具服务 / MCP Aggregated Tool Service

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-%3E=3.8-blue)
![FastAPI](https://img.shields.io/badge/based%20on-FastAPI-informational)
![Dockerized](https://img.shields.io/badge/docker-ready-success)

一个基于 FastAPI + fastapi_mcp 实现的多工具统一接入平台，支持模块化、自动注册与异步扩展。适用于将多个 AI 工具或微服务聚合为一个统一接口服务，支持标准化输入输出格式，便于前端集成或 LLM 系统调用。

A modular, extensible and FastAPI-based MCP (Multi-Component Platform) tool aggregation service. Easily connect and expose independent tools through standardized APIs. Perfect for frontend integration or large language model (LLM) orchestration.

---

## 🌟 功能特点 / Features

- ✅ 支持多工具自动注册（基于目录扫描）
- ✅ 所有接口统一 POST 方式 + BaseModel 校验
- ✅ 支持异步 httpx 接口调用
- ✅ 标准化 JSON 响应格式（success/error）
- ✅ Docker 一键部署支持
- ✅ 配套开发说明文档，便于扩展工具模块

---

## 📁 项目结构 / Project Structure

```bash
.
├── main.py                    # FastAPI 主程序，含 MCP 注册逻辑
├── tools/                     # 工具目录，每个文件一个功能
├── Dockerfile                 # 构建镜像用
├── docker-compose.yml         # 一键部署支持
├── mcp_tool_开发说明.md       # 开发者使用规范文档（中文）
└── README.md
```

---

## 🚀 快速开始 / Quick Start

### 🧰 依赖要求 / Requirements

- Python 3.8+
- pip
- Docker / Docker Compose（可选）

### 📦 本地运行 / Local Dev

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

默认服务地址：http://localhost:8000/mcp

### 🐳 使用 Docker 部署 / Docker Deployment

```bash
# 构建 & 运行
docker-compose up --build -d

# 访问 MCP 工具服务
http://localhost:8000/mcp
```

---

## 🧱 工具模块开发规范 / Tool Module Guidelines

每个工具应放置于 `tools/` 目录下（可多层嵌套），并包含：

1. 使用 `pydantic.BaseModel` 定义参数；
2. 使用 `@__mcp_server__.tool()` 注册工具函数；
3. 返回 `success_response()` 或 `error_response()`；
4. （可选）异步调用外部接口 + 缓存结果。

示例参考：

```python
from pydantic import BaseModel
from main import __mcp_server__, success_response

class MyParams(BaseModel):
    name: str

@__mcp_server__.tool()
async def hello_tool(params: MyParams):
    return success_response({"message": f"Hello {params.name}!"})
```

---

## 🔗 接口说明 / API Usage

所有工具接口统一通过 `/mcp` 路径访问，自动根据模块注册。

请求方式：`POST`  
请求格式：`application/json`  
响应格式：
```json
{
  "status": "success",
  "result": {
    ...
  }
}
```

---

## 📚 文档参考 / Docs

- [📘 开发说明文档 (中文)](./mcp_tool_开发说明.md)
- 示例模块路径：`tools/xxx/tool_name.py`

---

## 📄 License

MIT License © 2025 [your-name]
