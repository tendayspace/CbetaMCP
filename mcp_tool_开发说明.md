
# 🧩 MCP 工具模块开发说明文档

## 📘 项目背景

本项目基于 FastAPI + fastapi_mcp 构建，目标是实现一个**模块化、多工具可扩展的 AI MCP 工具服务平台**。每个工具接口以独立模块存在，遵循统一的注册与响应规范。

---

## 🧰 MCP 工具模块开发规范

### 📂 模块路径规范

每个工具放置在 `tools/` 目录下，**可以是任意多层子目录结构**。

```text
tools/
├── 模块名/
│   ├── 子模块/
│   │   └── 工具名.py 👈 每个文件一个功能接口
```

示例路径：

- `tools/cebta/goto/tools.py`
- `tools/oanda/candles.py`
- `tools/weather/city_forecast.py`

---

## 🧩 接口结构规范

每个工具模块中必须包含以下内容：

### ✅ 1. 请求参数定义

使用 `pydantic.BaseModel` 作为参数校验器：

```python
from pydantic import BaseModel
from typing import Optional

class MyToolParams(BaseModel):
    name: str
    age: Optional[int] = None
```

### ✅ 2. 注册 MCP 工具接口

工具函数必须使用装饰器 `@__mcp_server__.tool()` 装饰，支持 POST 请求方式：

```python
from main import __mcp_server__, success_response, error_response

@__mcp_server__.tool()
async def my_tool(params: MyToolParams):
    # 调用逻辑...
    return success_response({"hello": params.name})
```

### ✅ 3. 响应格式统一：

```python
def success_response(result: dict):
    return {"status": "success", "result": result}

def error_response(message: str):
    return {"status": "error", "message": message}
```

主程序已定义，工具模块直接引用即可。

### ✅ 4. 外部接口调用推荐方式（异步）

```python
import httpx

async with httpx.AsyncClient() as client:
    resp = await client.get("https://xxx/api", params=params.dict())
    resp.raise_for_status()
    return success_response(resp.json())
```

### ✅ 5. 可选：记录缓存

```python
import time, os, json
from collections import defaultdict

LOG_FILE = os.getenv("MCP_LOG_FILE", "mcp_cache_log.json")
search_cache = defaultdict(list)

def add_to_cache(method: str, request: dict, response: dict):
    timestamp = int(time.time())
    entry = {"timestamp": timestamp, "method": method, "request": request, "response": response}
    search_cache[method].append(entry)
    search_cache[method] = search_cache[method][-20:]
    try:
        logs = json.load(open(LOG_FILE, "r", encoding="utf-8")) if os.path.exists(LOG_FILE) else []
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs[-1000:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("写入缓存失败:", e)
```

---

## 🧾 开发提示词模板（Prompt Template）

```text
请帮我创建一个 FastAPI MCP 工具模块，要求如下：

1. 所有逻辑写在一个独立的 Python 文件中，文件路径为：
   tools/<模块目录>/<工具名>.py，例如 tools/weather/city_forecast.py

2. 工具接口使用 POST 请求，使用 BaseModel 定义请求参数；

3. 工具函数使用 @__mcp_server__.tool() 装饰，便于被主程序自动注册；

4. 工具内部可使用 httpx.AsyncClient 请求外部 API，支持异步；

5. 返回统一结构，使用主程序中的：
   from main import __mcp_server__, success_response, error_response

6. 若需记录日志缓存，可使用 add_to_cache(method, request, response)

7. 工具函数必须有中文注释，说明用途与参数含义。

8. 所有依赖必须为标准库或 FastAPI 常见依赖，如 pydantic, httpx, typing。

9. 一个文件建议只注册一个 MCP 工具函数，保持结构清晰。
```

---

## ✅ 工具开发流程

1. 新建模块文件：如 `tools/tools_file/tool_1.py`
2. 写入：
   - `BaseModel` 请求参数
   - MCP 工具函数
   - 响应格式
   - 可选：日志缓存
3. 启动主程序 `main.py`，即可自动加载该模块
4. 通过 `/mcp` 调用或测试该工具功能

---

## 📌 主程序 main.py 要求

- 提供全局 MCP 对象 `__mcp_server__`
- 提供统一响应函数
- 支持自动导入所有 tools 下的模块：

```python
def recursive_import_tools(base_dir="tools"):
    for path in Path(base_dir).rglob("*.py"):
        if not path.name.startswith("_"):
            importlib.import_module(".".join(path.with_suffix("").parts))
```

---
