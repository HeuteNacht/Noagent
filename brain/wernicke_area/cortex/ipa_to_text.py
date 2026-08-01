# -*- coding: utf-8 -*-
from loguru import logger

PLUGIN_NAME = "Semantic Cortex (IPA -> Text)"

def awaken(root_dir, current_dir):
    pass

async def can_process(request: dict) -> bool:
    """受体：专门接管上一阶段产出的 IPA 音标序列"""
    return request.get("data_type") == "ipa"

async def process(request: dict) -> dict:
    ipa_text = request.get("content")
    logger.info(f"[{PLUGIN_NAME}] 正在将 IPA [{ipa_text}] 解码为自然语言文本...")
    
    # Mock 解码逻辑 (后续可接入 G2P/P2G 或小 LLM 矫正模型)
    decoded_text = f"Hello world (decoded from IPA: {ipa_text})"

    return {
        "status": "success",
        "target_topic": "stimulus.raw",  # 💡 跨脑区折跃：直接发射给前额叶!
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "content": decoded_text      # 此时内容变回了普通文本
        }
    }
