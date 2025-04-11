from pydantic import BaseModel
from typing import Optional
from main import __mcp_server__, success_response, error_response
import httpx

class CBETASearchSCParams(BaseModel):
    q: str  # 搜尋關鍵詞（支持簡體/繁體）
    fields: Optional[str] = None  # 限定欄位，如 "juan,text"
    rows: Optional[int] = 10      # 回傳結果數量
    start: Optional[int] = 0      # 起始位置
    order: Optional[str] = None   # 排序方式

@__mcp_server__.tool()
async def cbeta_search_sc(params: CBETASearchSCParams):
    """
    🧩 CBETA 簡體/繁體搜尋工具（無需手動轉換）
    
    📥 請求參數：
    - q (str)：關鍵詞（支持簡體或繁體，如 "四圣谛" 或 "四聖諦"）
    - fields, rows, start, order 等同 CBETA API 參數

    📤 回傳格式：
    {
        "q": "四圣谛",  # 原始查詢詞
        "hits": 41      # 匹配筆數
    }
    """
    try:
        query_params = {
            "q": params.q,  # 直接使用原始輸入，CBETA 會自行處理簡繁轉換
            "fields": params.fields,
            "rows": params.rows,
            "start": params.start,
            "order": params.order
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/search/sc", params=query_params)
            resp.raise_for_status()
            data = resp.json()

        return success_response({
            "q": params.q,
            "hits": data.get("hits", 0)
        })
    
    except Exception as e:
        return error_response(f"查詢 CBETA 失敗：{str(e)}")