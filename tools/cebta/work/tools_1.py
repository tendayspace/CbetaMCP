# 建議保存為：tools/cbeta/work_info.py

from pydantic import BaseModel
from typing import Optional
import httpx
from main import __mcp_server__, success_response, error_response

# ✅ 請求參數模型：指定佛典編號
class CBETAWorkInfoParams(BaseModel):
    work: str  # 佛典編號，例如 "T1501"

# ✅ MCP 工具：查詢佛典資訊（例如：菩薩戒本 T1501）
@__mcp_server__.tool()
async def get_cbeta_work_info(params: CBETAWorkInfoParams):
    """
    📘 工具名稱：get_cbeta_work_info
    📌 功能：根據 CBETA 佛典編號（work），取得該佛典詳細資訊。

    ✅ 請求參數：
    - work (str)：佛典編號（如 "T1501"）

    🌐 依據 CBETA Online API：https://api.cbetaonline.cn/works?work=T1501

    📥 請求範例：
    {
        "work": "T1501"
    }

    📤 回應成功範例：
    {
      "status": "success",
      "result": {
        "work": "T1501",
        "title": "菩薩戒本",
        "byline": "彌勒菩薩說 唐 玄奘譯",
        "creators": "彌勒菩薩,玄奘",
        "category": "律部類",
        "orig_category": "律部",
        "time_dynasty": "唐",
        "time_from": 649,
        "time_to": 649,
        "cjk_chars": 7748,
        "en_words": 4,
        "file": "T24n1501",
        "juan_start": 1,
        "places": [
          {
            "name": "大慈恩寺",
            "id": "PL000000042410",
            "latitude": 34.219161,
            "longitude": 108.959356
          },
          {
            "name": "翠微寺",
            "id": "PL000000042513",
            "latitude": 33.839563,
            "longitude": 108.928138
          }
        ]
      }
    }

    ❌ 回應錯誤範例（查無資料）：
    {
      "status": "error",
      "message": "查無此佛典資訊"
    }

    🏷️ 字段說明：
    - work：佛典編號（如 T1501）
    - title：佛典題名（經名）
    - byline：作譯者說明（如：彌勒菩薩說 唐 玄奘譯）
    - creators：貢獻者（作者、譯者）
    - category：所屬 CBETA 分類（如 律部類）
    - orig_category：底本原始分類（如 律部）
    - time_dynasty：朝代（如 唐）
    - time_from/to：成立時間範圍（西元年）
    - cjk_chars：中文字數（不含標點）
    - en_words：英文/巴利/數字等單字數量
    - file：對應實體檔案代碼（如 T24n1501）
    - juan_start：起始卷
    - places：地點列表（含地點名稱與座標）

    🧠 本工具適用於：
    - 語義查詢、知識圖譜擴充、數據標註等需要取得佛典背景資訊之任務
    """

    url = "https://api.cbetaonline.cn/works"
    query_params = {"work": params.work}

    try:
        # ⏱️ 非同步請求 CBETA API
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as e:
        return error_response(f"取得佛典資料失敗：{str(e)}")

    if data.get("num_found", 0) == 0:
        return error_response("查無此佛典資訊")

    result = data["results"][0]

    return success_response({
        "work": result.get("work"),
        "title": result.get("title"),
        "byline": result.get("byline"),
        "creators": result.get("creators"),
        "category": result.get("category"),
        "orig_category": result.get("orig_category"),
        "time_dynasty": result.get("time_dynasty"),
        "time_from": result.get("time_from"),
        "time_to": result.get("time_to"),
        "cjk_chars": result.get("cjk_chars"),
        "en_words": result.get("en_words"),
        "file": result.get("file"),
        "juan_start": result.get("juan_start"),
        "places": result.get("places"),
    })
