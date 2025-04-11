from typing import Optional
from pydantic import BaseModel
from main import __mcp_server__, success_response, error_response
import httpx

# 定義請求參數格式
class CBETAAllInOneParams(BaseModel):
    q: str  # 必填，查詢關鍵字，支援 AND / OR / NOT / NEAR 等進階語法
    note: Optional[int] = 1  # 是否包含夾注，0: 不含，1: 含（預設）
    fields: Optional[str] = None  # 指定回傳欄位，如：work,juan,term_hits
    facet: Optional[int] = 0  # 是否回傳 facet，0: 不回傳（預設），1: 回傳
    rows: Optional[int] = 20  # 每頁筆數，預設為 20
    start: Optional[int] = 0  # 起始位置，預設為 0
    around: Optional[int] = 10  # KWIC 前後字數，預設為 10
    order: Optional[str] = None  # 排序條件，如 time_from+ 表升冪，time_from- 表降冪
    cache: Optional[int] = 1  # 是否使用快取，預設為 1

# 註冊 MCP 工具接口
@__mcp_server__.tool()
async def cbeta_all_in_one(params: CBETAAllInOneParams):
    """
    📘 CBETA 全文檢索接口：All in One
    
    查詢關鍵字後，同時回傳 KWIC（關鍵字前後文段）與命中資料。
    可選擇是否同時返回 Facet（藏經、部類、作譯者、朝代、佛典）分類資訊。
    支援 AND / OR / NOT / NEAR 進階語法查詢。
    
    🔧 參數說明：
    - q: 查詢關鍵字，必填。
    - note: 是否含夾注，0: 不含，1: 含（預設）
    - fields: 回傳欄位篩選，例如：work,juan,term_hits
    - facet: 是否回傳分類（facet），0: 否，1: 是
    - rows: 每頁筆數，預設 20
    - start: 起始筆數位置，預設 0
    - around: KWIC 前後字數，預設 10
    - order: 排序條件，如 time_from+, canon-
    - cache: 是否使用快取，1: 使用（預設）

    ✅ 回傳 JSON 示例（不含 facet）：
    {
      "query_string": "法鼓",
      "num_found": 1059,
      "total_term_hits": 1492,
      "results": [
        {
          "juan": 1,
          "canon": "T",
          "work": "T0270",
          "title": "大法鼓經",
          "term_hits": 31,
          "kwics": {
            "num_found": 31,
            "results": [
              {"kwic": "擊於大<mark>法鼓</mark>..."},
              ...
            ]
          }
        }, ...
      ]
    }

    ✅ 回傳 JSON 示例（含 facet）：
    {
      "facet": {
        "category": [
          {"category_id": 17, "category_name": "禪宗部類", "juans": 283},
          ...
        ],
        "dynasty": [
          {"dynasty": "唐", "juans": 164},
          ...
        ]
      }
    }
    """
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                "https://api.cbetaonline.cn/search/all_in_one",
                params=params.dict(exclude_none=True)
            )
            response.raise_for_status()
            return success_response(response.json())
    except Exception as e:
        return error_response(f"CBETA 檢索失敗: {str(e)}")
