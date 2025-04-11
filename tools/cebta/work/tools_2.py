# tools/cbeta/toc.py
from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# 定义请求参数模型
class CBETATocParams(BaseModel):
    work: str  # 佛典編號，例如 T0001

# 注册 MCP 工具接口，获取 CBETA 佛典內的目次信息
@__mcp_server__.tool()
async def get_cbeta_toc(params: CBETATocParams):
    """
    📘 工具说明：
    通过 CBETA Online API 获取指定佛典的目次结构。

    🔗 外部 API：
    https://api.cbetaonline.cn/toc?work=T0001

    🧾 示例请求参数：
    {
        "work": "T0001"
    }

    ✅ 示例返回结构（部分）：
    {
        "num_found": 1,
        "time": 0.0008,
        "results": [
            {
                "mulu": [
                    {
                        "title": "序",              # 目次節點 標題
                        "file": "T01n0001",       # 所在 XML 檔主檔名
                        "juan": 1,                # 所在卷號
                        "lb": "0001a02",          # 頁、欄、行位置
                        "type": "序"               # 節點類型（如：分、經、序）
                    },
                    {
                        "title": "1 分",
                        "file": "T01n0001",
                        "juan": 1,
                        "lb": "0001b11",
                        "type": "分",
                        "n": 1,                    # 節點序號
                        "isFolder": true,         # 是否有子節點
                        "children": [
                            {
                                "title": "1 大本經",
                                "file": "T01n0001",
                                "juan": 1,
                                "lb": "0001b11",
                                "type": "經",
                                "n": 1
                            }
                            # ... 更多 children
                        ]
                    }
                    # ... 更多目次節點
                ]
            }
        ]
    }

    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.cbetaonline.cn/toc", params={"work": params.work})
            response.raise_for_status()
            data = response.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"取得 CBETA 目次失敗: {str(e)}")
