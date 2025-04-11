from pydantic import BaseModel
from typing import Optional
from main import __mcp_server__, success_response, error_response
import httpx

# 定義請求參數模型，用於驗證輸入參數
class CBETACatalogParams(BaseModel):
    q: str  # 查詢節點編號，例如 'root'、'CBETA'、'orig-T'、'CBETA.001' 等

# 註冊 MCP 工具函數，支援 POST 調用
@__mcp_server__.tool()
async def get_cbeta_catalog(params: CBETACatalogParams):
    """
    📘 工具名稱：get_cbeta_catalog

    📌 工具用途：
    查詢 CBETA Online 提供的佛典目錄結構資料，可用於取得特定藏經分類、原書結構、或進一步展開經文節點。

    🔧 支援的查詢類型（q 參數）：
    - "root"：取得所有頂層目錄節點
    - "CBETA"：取得 CBETA 的部類目錄（如 阿含部、般若部等）
    - "orig"：取得所有原始藏經分類
    - "orig-T"：取得《大正藏》的原書結構目錄
    - "CBETA.001"：取得某一部類下的細節目錄
    - "Vol-J.001"：特殊節點查詢（可能出現 node_type=alt 替代）

    📥 輸入參數：
    - q (str): 查詢字串，對應 CBETA API 的查詢參數

    📤 回傳格式（示例）：
    {
        "num_found": 21,
        "results": [
            {
                "n": "CBETA.001",
                "label": "01 阿含部類 T01-02,25,33 etc."
            },
            ...
        ]
    }

    🔁 子節點查詢方式：
    可根據任一回傳項目的 `n` 字段進一步查詢下層，如：
    - 查詢 CBETA.001 的下層：q="CBETA.001"
    - 查詢 T0220 大般若經內容：q="CBETA.003.001"

    ⚠️ 注意事項：
    - 若 node_type 為 'alt'，代表該節點未直接收錄全文，可透過對應藏經節點查詢。

    """
    url = "https://api.cbetaonline.cn/catalog_entry"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"q": params.q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP 錯誤: {str(e)}")
    except Exception as e:
        return error_response(f"發生錯誤: {str(e)}")
