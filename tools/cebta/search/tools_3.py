from pydantic import BaseModel
from typing import Optional
import httpx

from main import __mcp_server__, success_response, error_response

# ------------------------------
# 📘 工具名称：CBETA Online 近义词搜索
# 🔍 接口用途：
#   输入关键词（如“文殊師利”），返回与该关键词相关的近义词列表。
#   可用于文本理解、智能问答、佛典对照等场景。
# 📮 外部请求地址：https://api.cbetaonline.cn/search/synonym?q=文殊師利
#
# ✅ 请求参数说明：
#   - q (str): 必填，查询关键词，例如“文殊師利”
#
# ✅ 返回字段说明：
#   - time (float): 查询耗时（单位：秒）
#   - num_found (int): 找到的近义词数量
#   - results (List[str]): 所有近义词词条列表
#
# ✅ 示例返回 JSON：
# {
#     "time": 0.001340973,
#     "num_found": 9,
#     "results": [
#         "滿殊尸利",
#         "曼殊室利",
#         "妙德",
#         "妙首",
#         "妙吉祥",
#         "文殊",
#         "妙吉祥菩薩",
#         "妙音",
#         "曼殊"
#     ]
# }
# ------------------------------

class SynonymSearchParams(BaseModel):
    q: str  # 查詢詞，如：文殊師利

@__mcp_server__.tool()
async def synonym_search(params: SynonymSearchParams):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/search/synonym", params={"q": params.q})
            resp.raise_for_status()
            data = resp.json()
            return success_response(data)
    except Exception as e:
        return error_response(f"近义词搜索失败: {str(e)}")