from pydantic import BaseModel
from main import __mcp_server__, success_response, error_response
import httpx

# 定義請求參數模型
class CBETATextSearchParams(BaseModel):
    q: str  # 搜尋關鍵詞或藏經冊號，如 "阿含" 或 "T01"

# 註冊 MCP 工具函數
@__mcp_server__.tool()
async def search_cbeta_texts(params: CBETATextSearchParams):
    """
    📘 工具名稱：search_cbeta_texts

    📌 工具用途：
    搜尋 CBETA 佛典經目，根據關鍵詞或冊號進行查詢。

    🔍 可用搜尋情境：
    1. 搜尋某一關鍵詞（如：阿含）：
       - q="阿含"
       - 對應 API: https://api.cbetaonline.cn/toc?q=阿含

    2. 搜尋某一冊之下的佛典：
       - q="T01"（代表大正藏第1冊）
       - 官方建議改用 catalog_entry: https://api.cbetaonline.cn/catalog_entry?vol=T01
       - 但本接口仍支援舊 toc 查詢

    📥 輸入參數：
    - q (str): 搜尋字串，可為關鍵詞或藏經冊號

    📤 回傳格式範例：
    {
        "num_found": 46,
        "results": [
            {
                "type": "catalog",
                "n": "Cat-T.001",
                "label": "TB01 阿含部 T01~02 (1~151 經)"
            },
            {
                "type": "work",
                "n": "T0001",
                "label": "長阿含經"
            },
            {
                "type": "toc",
                "n": "T0001.001",
                "label": "序品 第一"
            },
            ...
        ]
    }

    📘 type 欄位說明：
    - catalog：表示來自部類目錄
    - work：表示經名層級（佛典標題）
    - toc：表示佛典內目次層級

    ⚠️ 注意：
    若目的是取得某冊之下的佛典列表，建議改用 catalog_entry 的 vol 參數形式。
    但本工具仍支援 toc API，以兼容既有查詢邏輯。

    """
    url = "https://api.cbetaonline.cn/toc"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"q": params.q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP 錯誤: {str(e)}")
    except Exception as e:
        return error_response(f"發生錯誤: {str(e)}")
