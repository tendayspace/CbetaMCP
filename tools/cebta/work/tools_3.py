from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# CBETA 卷 HTML 內容抓取工具
#
# 🧾 工具功能：
# 通過 CBETA API 抓取指定佛典 work 的指定卷（juan）HTML 內容，
# 可選是否同時返回「佛典資訊 work_info」與「目次 toc」內容。
#
# 📘 CBETA API 說明：
# URL: https://api.cbetaonline.cn/juans
# 參數:
#   - work: 佛典編號，如 T0001
#   - juan: 卷號，從 1 開始
#   - work_info: 是否回傳佛典資訊，0=否，1=是（預設為 0）
#   - toc: 是否回傳目次，0=否，1=是（預設為 0）
#
# ✅ JSON 返回格式範例（節錄）：
# {
#   "num_found": 1,
#   "results": [
#     { "juan": 1, "html": "<div id='body'>...</div>" }
#   ],
#   "work_info": {...},
#   "toc": {
#     "mulu": [...],
#     "juan": [...]
#   }
# }
#
# 🔧 用途：可用於 CBETA 閱讀器前端渲染、段落分析、結構轉換等。

class GetJuanHTMLParams(BaseModel):
    work: str                    # 佛典編號，例如 T0001
    juan: int                   # 卷號（從 1 開始）
    work_info: Optional[int] = 0  # 是否回傳佛典資訊（0=否，1=是）
    toc: Optional[int] = 0        # 是否回傳目次（0=否，1=是）

@__mcp_server__.tool()
async def get_juan_html(params: GetJuanHTMLParams):
    try:
        url = "https://api.cbetaonline.cn/juans"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params.dict())
            resp.raise_for_status()
            data = resp.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"CBETA API 請求失敗: {str(e)}")
