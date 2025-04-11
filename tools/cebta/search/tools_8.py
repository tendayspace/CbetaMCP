# 文件路径：tools/cbeta/search_title.py

from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# 📘 工具說明：
# 本工具接口功能為【搜尋佛典標題（經名）】。
# 接口將向 CBETA Online API 發送請求，對經名進行模糊搜尋（至少三字以上），
# 並返回相關書目條目信息，包含經名、卷數、作者朝代等資料。
#
# 🔸 外部API地址：https://api.cbetaonline.cn/search/title
#
# ✅ 支持參數說明：
# - q（str）：必填，搜尋關鍵字，至少三個字。
# - rows（int）：選填，每頁回傳筆數，預設為 20。
# - start（int）：選填，起始位置，預設為 0（用於分頁）。
#
# ✅ 示例 JSON 返回：
# {
#   "query_string": "觀無量壽經",
#   "time": 0.01657838,
#   "num_found": 49,
#   "results": [
#     {
#       "work": "X0411",                          # 書號
#       "content": "觀無量壽經義疏正觀記",         # 書名
#       "highlight": "<mark>觀無量壽經</mark>義疏正<mark>觀</mark>記",  # 高亮顯示結果
#       "byline": "宋 戒度述",                     # 作者資訊
#       "juan": 3,                                # 卷數
#       "creators_with_id": "戒度(A000511)",      # 作者及其 ID
#       "time_dynasty": "宋",                      # 朝代
#       "time_from": 960,                         # 起始年份
#       "time_to": 1279                           # 結束年份
#     },
#     ...
#   ]
# }

class SearchTitleParams(BaseModel):
    q: str  # 搜尋經名（至少三個字）
    rows: Optional[int] = 20  # 每頁回傳筆數，預設為 20
    start: Optional[int] = 0  # 起始位置，預設為 0（分頁使用）

@__mcp_server__.tool()
async def search_title(params: SearchTitleParams):
    """搜尋佛典標題（經名）"""
    if len(params.q.strip()) < 3:
        return error_response("搜尋關鍵字至少需三個字以上")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/search/title", params=params.dict())
            resp.raise_for_status()
            data = resp.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"外部 API 請求失敗: {str(e)}")
