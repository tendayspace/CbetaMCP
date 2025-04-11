from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# ==========================
# CBETA 相似搜尋工具模組
# ==========================

class CBETASimilarSearchParams(BaseModel):
    q: str  # 必要參數：要搜尋的字串，不含標點，建議長度 6~50 字
    k: Optional[int] = 500  # 模糊搜尋取 top k 筆，預設為 500
    gain: Optional[int] = 2  # Smith-Waterman 比對加分，預設為 2
    penalty: Optional[int] = -1  # Smith-Waterman 扣分，預設為 -1
    score_min: Optional[int] = 16  # Score 最小值，預設為 16
    facet: Optional[int] = 0  # 是否回傳 facet：0 不回傳，1 回傳五種 facet 資訊
    cache: Optional[int] = 1  # 是否使用快取：1 使用，0 不使用

@__mcp_server__.tool()
async def cbeta_similar_search(params: CBETASimilarSearchParams):
    """
    🔍 CBETA 相似搜尋工具

    說明：
    本工具使用 CBETA Online 的 /search/similar API，透過 Manticore + Smith-Waterman 演算法實現字句相似搜尋。

    ✅ 參數說明：
    - q (str): 【必要】要搜尋的句子內容（不含標點）
    - k (int): 取回前 k 筆初始結果，預設 500
    - gain (int): 比對演算法中 match 的加分，預設 2
    - penalty (int): 比對演算法中 miss/插入/刪除的扣分，預設 -1
    - score_min (int): 最低匹配分數，預設 16
    - facet (int): 是否回傳分類 facet，1 為是，0 為否（預設）
    - cache (int): 是否啟用快取（預設為 1）

    📥 示例請求：
    {
        "q": "已得善提捨不證"
    }

    📤 回傳 JSON 結構示例：
    {
        "query_string": "已得善提捨不證",
        "SQL": "SELECT ...",
        "time": 1.101,
        "num_found": 0,
        "cache_key": "...",
        "results": []
    }

    回傳欄位說明：
    - query_string: 查詢內容
    - SQL: 後端實際查詢語句
    - time: 執行時間 (秒)
    - num_found: 命中筆數
    - cache_key: 快取索引鍵
    - results: 命中資料陣列（含經文標題、段落、句子與比對標記）

    🔗 API 來源：https://api.cbetaonline.cn/search/similar
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/search/similar", params=params.dict())
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA 相似搜尋失敗: {str(e)}")
