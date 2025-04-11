# tools/cbeta/extended_search.py

from pydantic import BaseModel
from typing import Optional
import httpx
from urllib.parse import quote
from main import __mcp_server__, success_response, error_response

# 📘 工具用途說明：
# 本工具封裝 CBETA Online 擴充搜尋模式 API（https://api.cbetaonline.cn/search/extended），
# 支援 AND、OR、NOT、NEAR 等語法進行全文檢索，支援繁體佛典查詢。
#
# ✅ 查詢語法說明：
# - AND 搜尋：每個詞語必須加雙引號，再以空格分隔 => `"法鼓" "聖嚴"`
# - OR 搜尋：加上 | 運算符 => `"波羅蜜" | "波羅密"`
# - NOT 搜尋：使用驚嘆號 => `"迦葉" !"迦葉佛"`
# - NEAR 搜尋：使用 NEAR/距離 => `"法鼓" NEAR/7 "迦葉"`
# - 所有查詢語句皆需 URL encode，例如：`"波羅蜜" | "波羅密"` => `%22波羅蜜%22%20%7C%20%22波羅密%22`
#
# 📥 請求參數：
# - q: str        👉 查詢語句（需自行加雙引號及格式語法）
# - start: int    👉 起始位置（預設為 0）
# - rows: int     👉 回傳筆數（預設為 20）

class ExtendedSearchParams(BaseModel):
    q: str
    start: Optional[int] = 0
    rows: Optional[int] = 20

@__mcp_server__.tool()
async def extended_search(params: ExtendedSearchParams):
    """
    🧠 CBETA 擴充模式全文檢索工具

    接收關鍵詞查詢語句，傳送至 CBETA 擴充 API 並回傳匹配經文資訊。

    ✅ 支援 AND、OR、NOT、NEAR 語法，所有查詢語句需為已編碼格式。

    📤 回傳格式（JSON 範例）：
    {
      "status": "success",
      "result": {
        "total": 317,
        "rows": [
          {
            "title": "大方廣佛華嚴經",
            "juan": "卷第十",
            "content": "...善財童子至法鼓山..."
          },
          ...
        ]
      }
    }
    """
    try:
        # 對查詢語句進行 URL encode
        encoded_query = quote(params.q)

        # 發送 GET 請求至 CBETA 擴充搜尋 API
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.cbetaonline.cn/search/extended",
                params={"q": encoded_query, "start": params.start, "rows": params.rows},
                timeout=20
            )
            resp.raise_for_status()
            data = resp.json()

        # 精簡回傳內容
        total = data.get("total", 0)
        rows = [
            {
                "title": r.get("title", ""),
                "juan": r.get("juan", ""),
                "content": r.get("content", "")
            }
            for r in data.get("results", [])
        ]
        return success_response({"total": total, "rows": rows})

    except Exception as e:
        return error_response(f"CBETA 擴充搜尋失敗: {str(e)}")
