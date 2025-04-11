# tools/cbeta/search_notes.py

from typing import Optional
from pydantic import BaseModel
from main import __mcp_server__, success_response, error_response
import httpx

class CBETANotesSearchParams(BaseModel):
    q: str  # 要搜尋的字詞，需加雙引號（且需 URL encode）
    around: Optional[int] = 10  # highlight 關鍵字週圍字數，預設為 10
    rows: Optional[int] = 20  # 每頁回傳筆數，預設為 20
    start: Optional[int] = 0  # 起始位置，預設為 0
    facet: Optional[int] = 0  # 是否回傳 facet，0=不回傳，1=回傳四種 facet

@__mcp_server__.tool()
async def search_cbeta_notes(params: CBETANotesSearchParams):
    """
    📘 CBETA Online 註解／校勘條目搜尋工具

    ✅ 功能：
    以查詢字詞搜尋 CBETA Online 所提供的「註解（夾注、腳註）」內容，支援高亮、分頁與 Facet 統計功能。

    ✅ 參數說明：
    - q（必須）：查詢關鍵詞，需以雙引號括起，例如 `"法鼓"`。
      - AND 查詢：`"法鼓" "印順"`
      - OR 查詢：`"波羅蜜"|"波羅密"`
      - NOT 查詢：`"迦葉" !"迦葉佛"`
      - NEAR 查詢：`"阿含" NEAR/5 "迦葉"`
    - around：highlight 的上下文字數，預設為 10。
    - rows：回傳筆數，預設為 20。
    - start：分頁起始 index，預設為 0。
    - facet：是否回傳 facet 統計資訊，0=不回傳，1=回傳 canon/category/creator/work。

    🧪 API 範例：
    ```
    POST /mcp
    {
        "method": "search_cbeta_notes",
        "params": {
            "q": "%22法鼓%22",
            "around": 10,
            "rows": 5,
            "facet": 1
        }
    }
    ```

    📥 回傳欄位說明：
    - content：註解的實際文字內容
    - note_place：註解位置（"foot" 或 "inline"）
    - highlight：包含關鍵詞的上下文片段
    - facets（若 facet=1）：包含 canon、category、creator、work 的統計

    📤 回傳 JSON 範例：
    ```json
    {
        "status": "success",
        "result": {
            "response": {
                "numFound": 12,
                "start": 0,
                "docs": [
                    {
                        "note_place": "foot",
                        "content": "法鼓山創辦人聖嚴法師...",
                        "highlight": "...<mark>法鼓</mark>山創辦人..."
                    }
                ]
            },
            "facets": {
                "canon": [{"value": "T", "count": 3}],
                "category": [{"value": "論", "count": 2}],
                "creator": [{"value": "聖嚴", "count": 1}],
                "work": [{"value": "T198", "count": 1}]
            }
        }
    }
    ```
    """

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/search/notes", params=params.dict())
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA notes search failed: {str(e)}")
