import os
import pathlib
import importlib
from fastapi import FastAPI
from fastapi_mcp import add_mcp_server

# 初始化 FastAPI & MCP Server
app = FastAPI(title="MCP工具聚合服务", version="0.1.0")
BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="cebta MCP Tools",
    base_url=BASE_URL,
)

# 提供给其他模块引用的 MCP 装饰器
__mcp_server__ = mcp_server

# 通用响应结构
def success_response(result: dict):
    return {"status": "success", "result": result}

def error_response(message: str):
    return {"status": "error", "message": message}

# 自动递归导入 tools 目录下所有模块
registered_tool_names = set()  # 记录所有注册的 MCP 工具函数名，用于检测重复

def recursive_import_tools(base_dir="tools"):
    base_path = pathlib.Path(base_dir)
    for path in base_path.rglob("*.py"):
        if path.name.startswith("_"):  # 忽略 __init__.py 和 _xxx.py
            continue
        module_parts = path.with_suffix("").parts
        module_path = ".".join(module_parts)
        try:
            mod = importlib.import_module(module_path)
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if callable(attr) and getattr(attr, "_is_mcp_tool", False):
                    if attr.__name__ in registered_tool_names:
                        print(f"⚠️ MCP工具函数重复注册: `{attr.__name__}` 来源模块: {module_path}")
                    else:
                        registered_tool_names.add(attr.__name__)
        except Exception as e:
            print(f"❌ 模块导入失败: {module_path}，错误：{e}")

# 自动导入所有工具模块
recursive_import_tools()

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("APP_PORT", "8000")))