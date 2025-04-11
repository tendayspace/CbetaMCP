import httpx
from typing import Optional
from pydantic import BaseModel
from main import __mcp_server__, success_response, error_response

# 📘 CBETA 一般全文檢索工具
# 說明：
# 本工具透過 CBETA API 執行佛典全文檢索功能。
# 可輸入關鍵字與查詢選項（欄位、筆數、排序等），回傳包含卷號、藏經 ID、佛典編號等資訊。
# 
# ✅ 支援參數：
# - q (str): 【必填】關鍵字或組字式（需事先 escape）
# - fields (str): 【選填】指定回傳欄位，例如 "work,juan,term_hits"
# - rows (int): 【選填】每頁回傳筆數，預設為 20
# - start (int): 【選填】回傳的起始筆數，預設為 0
# - order (str): 【選填】排序欄位，例如 "time_from-" 表示依成立年代降序
# 
# 📥 範例請求：
# {
#     "q": "法鼓",
#     "fields": "work,juan,term_hits",
#     "rows": 3,
#     "order": "time_from-"
# }
#
# 📤 回傳欄位說明：
# - query_string: 搜尋字串標準化後的版本
# - num_found: 符合條件的卷數
# - total_term_hits: 關鍵詞總出現次數
# - results: 詳細結果，每筆含以下欄位：
#   - id: 條目 ID
#   - juan: 卷號
#   - category: 部類
#   - canon: 藏經 ID
#   - vol: 冊號
#   - work: 佛典編號
#   - title: 佛典標題
#   - creators: 譯者等資訊
#   - file: 檔案代碼
#   - time_from / time_to: 佛典成立時間
#
# ✅ 回傳 JSON 範例：
# {
#   "num_found": 2628,
#   "total_term_hits": 3860,
#   "results": [
#     {
#       "id": 12298,
#       "juan": 1,
#       "category": "法華部",
#       "canon": "T",
#       "vol": "T09",
#       "work": "T0270",
#       "term_hits": 31,
#       "title": "大法鼓經",
#       "creators": "求那跋陀羅",
#       "file": "T09n0270",
#       "time_from": 420,
#       "time_to": 479
#     }
#   ]
# }

class CBETASearchParams(BaseModel):
    q: str  # 搜尋關鍵字（必填）
    fields: Optional[str] = None  # 指定欄位（可選）
    rows: Optional[int] = 20  # 每頁筆數
    start: Optional[int] = 0  # 起始位置
    order: Optional[str] = None  # 排序規則

@__mcp_server__.tool()
async def cbeta_fulltext_search(params: CBETASearchParams):
    """
    CBETA 一般全文檢索工具，使用 CBETA Open API 搜尋佛典。
    文件：https://api.cbetaonline.cn/search
    """
    try:
        query_params = {k: v for k, v in params.dict().items() if v is not None}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search", params=query_params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA 搜尋失敗: {str(e)}")
