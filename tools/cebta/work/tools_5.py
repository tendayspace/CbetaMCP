from pydantic import BaseModel
from typing import Optional
import httpx

from main import __mcp_server__, success_response, error_response

# 📘 工具名稱：CBETA 指定行段文字取得工具
# 📌 工具功能說明：
# 透過 CBETA Online API，依據「行首資訊 linehead」或「起迄範圍 linehead_start / linehead_end」取得大正藏對應行文字（含註解）。
# 支援取得單行、上下文擴展、以及行段範圍文字。

# ✅ 支援參數：
# - linehead: 指定單行行號，如 "T01n0001_p0001a04"
# - linehead_start: 行段起始行號
# - linehead_end: 行段結束行號
# - before: 額外取得前幾行（搭配 linehead 使用）
# - after: 額外取得後幾行（搭配 linehead 使用）

# 🧾 回傳範例 JSON：
# {
#   "num_found": 1,
#   "results": [
#     {
#       "linehead": "T01n0001_p0001a04",
#       "html": "<a class=\"noteAnchor\" href=\"#n0001002\"></a>長安釋僧肇<a class=\"noteAnchor\" href=\"#n0001003\"></a>述",
#       "notes": {
#         "0001002": "〔長安〕－【宋】",
#         "0001003": "〔述〕－【宋】"
#       }
#     }
#   ]
# }

# 🔗 API 來源：https://api.cbetaonline.cn/lines


class CBETALineParams(BaseModel):
    linehead: Optional[str] = None  # 指定單一行首資訊
    linehead_start: Optional[str] = None  # 起始行首
    linehead_end: Optional[str] = None  # 結束行首
    before: Optional[int] = None  # 額外前幾行（搭配 linehead）
    after: Optional[int] = None  # 額外後幾行（搭配 linehead）


@__mcp_server__.tool()
async def get_cbeta_lines(params: CBETALineParams):
    """
    📘 CBETA 行文擷取工具
    依據 CBETA 大正藏 API，抓取指定行或行段的 HTML 內容與註解。
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/lines", params=params.dict(exclude_none=True))
            resp.raise_for_status()
            data = resp.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"CBETA 行文擷取失敗: {str(e)}")
