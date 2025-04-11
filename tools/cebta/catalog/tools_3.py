import httpx
from pydantic import BaseModel
from typing import Optional
from main import __mcp_server__, success_response, error_response

# 定义请求参数格式
class BuddhistCanonSearchParams(BaseModel):
    canon: str              # 藏經 ID，如 T 或 X
    vol_start: int          # 開始冊數，如 1
    vol_end: int            # 結束冊數，如 2

# 注册为 MCP 工具接口
@__mcp_server__.tool()
async def search_buddhist_canons_by_vol(params: BuddhistCanonSearchParams):
    """
    佛典範圍搜尋工具

    根據指定藏經 (canon) ID 與冊數起迄範圍 (vol_start ~ vol_end)，
    查詢對應範圍內的佛典資料。

    參數：
    - canon: 藏經 ID，例如 T、X
    - vol_start: 開始冊數 (int)
    - vol_end: 結束冊數 (int)

    外部 API 來源：https://api.cbetaonline.cn/works?canon=T&vol_start=1&vol_end=2
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {
        "canon": params.canon,
        "vol_start": params.vol_start,
        "vol_end": params.vol_end
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response({
                "num_found": data.get("num_found"),
                "results": data.get("results", [])
            })
    except Exception as e:
        return error_response(f"API 請求失敗: {str(e)}")


# ========================
# 🌟 示例：呼叫此工具方式如下：
# POST /mcp/search_buddhist_canons_by_vol
# Body JSON:
# {
#     "canon": "T",
#     "vol_start": 1,
#     "vol_end": 2
# }
#
# 💡 返回範例：
# {
#     "status": "success",
#     "result": {
#         "num_found": 155,
#         "results": [
#             {
#                 "work": "T0001",
#                 "title": "長阿含經",
#                 "vol": "T01",
#                 "juan": 22,
#                 "byline": "後秦 佛陀耶舍共竺佛念譯",
#                 ...
#             },
#             ...
#         ]
#     }
# }
# ========================