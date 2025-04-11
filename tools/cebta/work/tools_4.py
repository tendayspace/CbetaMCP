from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# 📘 工具名稱：CBETA 經文跳轉接口
# 🧾 接口說明：
# 該工具封裝 CBETA Online 的 `/juans/goto` 接口，支持通過藏經編號、經號、冊數、頁數、欄、行等跳轉方式，獲取對應經文位置 URL。
# 支持三種跳轉方式：
# 1. 經卷結構（canon, work, juan, page, col, line）
# 2. 書本結構（canon, vol, page, col, line）
# 3. 行首格式引用（linehead）

# 📥 請求參數：
class CBETAGotoParams(BaseModel):
    canon: Optional[str] = None  # 藏經編號，如 T、X、N
    work: Optional[str] = None   # 經號，如 1、2、150A
    juan: Optional[int] = None   # 卷數
    vol: Optional[int] = None    # 冊數
    page: Optional[int] = None   # 頁碼
    col: Optional[str] = None    # 欄位，a, b, c
    line: Optional[int] = None   # 行數
    linehead: Optional[str] = None  # 行首引用，如 T01n0001_p0066c25 或 CBETA 格式

# 📤 返回示例：
# {
#     "status": "success",
#     "result": {
#         "url": "https://api.cbetaonline.cn/juans/goto?canon=T&work=1&page=11&col=b&line=10"
#     }
# }

@__mcp_server__.tool()
async def cbeta_goto(params: CBETAGotoParams):
    """
    📌 功能：跳轉到 CBETA 對應的經文位置 URL。

    ✅ 三種跳轉模式：
    - canon + work + (juan/page/col/line)
    - canon + vol + (page/col/line)
    - linehead (優先)

    ⚠️ 注意：若 linehead 存在，則其他參數將被忽略。
    """
    base_url = "https://api.cbetaonline.cn/juans/goto"
    query_params = {}

    # 優先處理 linehead
    if params.linehead:
        query_params['linehead'] = params.linehead
    else:
        for field in ['canon', 'work', 'juan', 'vol', 'page', 'col', 'line']:
            value = getattr(params, field)
            if value is not None:
                query_params[field] = value

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=query_params)
            response.raise_for_status()
            final_url = str(response.url)
            return success_response({"url": final_url})
    except Exception as e:
        return error_response(f"CBETA 跳轉失敗：{str(e)}")