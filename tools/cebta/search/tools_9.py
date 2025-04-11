from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# 📘 KWIC 檢索工具
# 
# 說明：
# 提供 CBETA Online 的 KWIC（Keyword in Context）單卷前後文檢索功能，可支援關鍵詞 NEAR 查詢、排除詞、夾注開關與關鍵詞標記等參數。
# 
# 📥 請求參數說明：
# - work (str, 必要)：佛典編號，如 T0001、X0600。
# - juan (int, 必要)：卷號，如 1、11。
# - q (str, 必要)：查詢關鍵詞，可含 NEAR、排除詞、雙引號、逗號等高級語法。
# - note (Optional[int])：是否包含夾注，0=不含，1=包含（預設=1）。
# - mark (Optional[int])：是否加 mark 標記，0=不加（預設），1=加。
# - sort (Optional[str])：排序方式，f=關鍵詞後排序，b=前排序，location=依卷內出現位置排序。
# 
# 📤 回傳結果 JSON 示例如下：
# {
#     "num_found": 4,              # 命中結果數
#     "time": 0.021964698,        # 查詢耗時（秒）
#     "results": [
#         {
#             "vol": "T36",       # 卷號代碼
#             "lb": "0002b03",    # 行標位置
#             "kwic": "...<mark>老子</mark>...<mark>道</mark>..."  # 前後文上下文（含關鍵詞）
#         }
#     ]
# }

class KwicSearchParams(BaseModel):
    work: str
    juan: int
    q: str
    note: Optional[int] = 1
    mark: Optional[int] = 0
    sort: Optional[str] = 'f'

@__mcp_server__.tool()
async def cbeta_kwic_search(params: KwicSearchParams):
    """
    🔍 CBETA KWIC 單卷關鍵詞檢索工具

    支援：NEAR/查詢、排除前後詞搭配、夾注開關、排序與標記控制。
    """
    url = "https://api.cbetaonline.cn/search/kwic"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params.dict())
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA KWIC 檢索失敗: {e}")