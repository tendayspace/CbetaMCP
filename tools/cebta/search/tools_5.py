from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# =====================
# 📘 接口說明：CBETA Facet 多維面向查詢
#
# 此工具用於查詢 CBETA Online 的 Facet 結構，支援以下 5 種分類：
# - canon：藏經編號（例：T、X、J 等）
# - category：部類（例：阿含部、大乘經等）
# - dynasty：朝代（例：唐、宋）
# - creator：作譯者 ID（例：釋道宣）
# - work：佛典編號（例：T01n0001）
#
# 可選擇性指定 `f` 參數，若不指定，將回傳全部 5 類 Facet 資訊。
#
# ✅ 示例請求：
# {
#   "q": "法鼓"
# }
#
# ✅ 示例回傳 JSON 結構：
# {
#   "status": "success",
#   "result": {
#     "canon": [ {"value": "T", "count": 27}, ...],
#     "category": [ {"value": "大乘經", "count": 15}, ...],
#     "dynasty": [ {"value": "唐", "count": 9}, ...],
#     "creator": [ {"value": "釋道宣", "count": 3}, ...],
#     "work": [ {"value": "T01n0001", "count": 2}, ...]
#   }
# }
#
# 📌 欄位說明：
# - q：查詢關鍵字（必填）
# - f：指定 facet 類型（可選：canon、category、dynasty、creator、work）

class CbetaFacetParams(BaseModel):
    q: str                      # 查詢關鍵字
    f: Optional[str] = None    # 指定 facet 類型（若不指定回傳全部）

@__mcp_server__.tool()
async def cbeta_facet_query(params: CbetaFacetParams):
    try:
        # 構建 URL
        base_url = "https://api.cbetaonline.cn/search/facet"
        url = f"{base_url}/{params.f}" if params.f else base_url

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"q": params.q})
            resp.raise_for_status()
            data = resp.json()

            return success_response(data)

    except Exception as e:
        return error_response(f"CBETA facet 查詢失敗: {str(e)}")
