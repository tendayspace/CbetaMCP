from pydantic import BaseModel
from typing import Optional, List
import httpx
from main import __mcp_server__, success_response, error_response

# ✅ 定义请求参数模型
class CBETADynastySearchParams(BaseModel):
    dynasty: Optional[str] = None  # 可传入单个朝代名称或多个朝代，以英文逗号分隔
    time_start: Optional[int] = None  # 可选：起始年份，如 600
    time_end: Optional[int] = None    # 可选：结束年份，如 700


# ✅ 注册 MCP 工具接口
@__mcp_server__.tool()
async def search_cbeta_by_dynasty(params: CBETADynastySearchParams):
    """
    通过朝代名称或公元时间范围搜索 CBETA 佛典。

    - 可输入 dynasty 参数（支持多个朝代名，用英文逗号隔开）
    - 可输入公元年范围：time_start 和 time_end
    - 若二者皆为空，则返回错误
    """
    if not params.dynasty and not (params.time_start and params.time_end):
        return error_response("请提供 dynasty 或 time_start 与 time_end 参数")

    # 构建请求参数
    query_params = {}
    if params.dynasty:
        query_params["dynasty"] = params.dynasty
    if params.time_start:
        query_params["time_start"] = params.time_start
    if params.time_end:
        query_params["time_end"] = params.time_end

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.cbetaonline.cn/works", params=query_params)
            resp.raise_for_status()
            data = resp.json()

            # ✅ 示例返回结构，便于 LLM 调用演示
            example = {
                "num_found": data.get("num_found", 0),
                "sample_result": data.get("results", [])[:2]  # 仅展示前2条用于示例
            }

            return success_response(example)
    except Exception as e:
        return error_response(f"CBETA 查詢失敗: {str(e)}")
