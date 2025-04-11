from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# =======================
# ✅ 定義請求參數
# =======================
class TranslatorSearchParams(BaseModel):
    creator_id: Optional[str] = None  # 作譯者 ID，如 A000439
    creator: Optional[str] = None     # 作譯者姓名模糊搜尋，如 "竺"
    creator_name: Optional[str] = None  # 僅搜尋尚未確認 ID 的譯者，如 "竺"

# =======================
# ✅ 註冊 MCP 工具
# =======================
@__mcp_server__.tool()
async def search_works_by_translator(params: TranslatorSearchParams):
    """
    📘 根據 CBETA Online 的作譯者資訊搜尋作品。

    支援三種搜尋方式：
    1. 指定作譯者 ID 搜尋（creator_id）
    2. 作譯者姓名模糊搜尋（creator）
    3. 僅搜尋尚未確認 ID 的姓名（creator_name）

    ✅ 示例請求：
    {
        "creator_id": "A000439"
    }
    或：
    {
        "creator": "竺"
    }
    或：
    {
        "creator_name": "竺"
    }

    ✅ 示例返回：
    {
        "status": "success",
        "result": {
            "num_found": 6,
            "results": [
                {
                    "work": "T0001",
                    "title": "長阿含經",
                    "creators": "佛陀耶舍,竺佛念",
                    "creators_with_id": "佛陀耶舍(A000439);竺佛念(A000435)",
                    "byline": "後秦 佛陀耶舍共竺佛念譯",
                    "canon": "T",
                    "category": "阿含部類",
                    "vol": "T01",
                    "juan": 22,
                    "time_dynasty": "後秦",
                    "time_from": 412,
                    "time_to": 413,
                    "places": [
                        {
                            "name": "長安",
                            "latitude": 34.3288,
                            "longitude": 108.9064
                        }
                    ]
                },
                ... 更多結果
            ]
        }
    }
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {}

    # 根據參數建立對應查詢條件
    if params.creator_id:
        query_params["creator_id"] = params.creator_id
    elif params.creator:
        query_params["creator"] = params.creator
    elif params.creator_name:
        query_params["creator_name"] = params.creator_name
    else:
        return error_response("請至少提供一個搜尋參數：creator_id、creator 或 creator_name")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"查詢失敗: {str(e)}")