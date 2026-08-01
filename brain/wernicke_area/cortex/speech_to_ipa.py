# -*- coding: utf-8 -*-
import asyncio
import base64
import tempfile
import os
from loguru import logger

PLUGIN_NAME = "Auditory Cortex (Speech -> IPA)"
_model = None

def awaken(root_dir, current_dir):
    global _model
    try:
        from allosaurus.app import read_recognizer
        logger.info(f"[{PLUGIN_NAME}] 正在装载 Allosaurus...")
        _model = read_recognizer()
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 模型装载失败: {e}")

async def can_process(request: dict) -> bool:
    # 🎯 多重防御：兼容 data_type、type 以及 payload 嵌套结构
    dtype = request.get("data_type") or request.get("type")
    
    # 只要类型属于 audio_chunk 或 audio，或者含有 base64 content 均放行
    return dtype in ["audio_chunk", "audio"] or bool(request.get("content"))

async def process(request: dict) -> dict:
    if not _model: return {"status": "error"}

    audio_b64 = request.get("content")
    
    # 1. Base64 还原为临时音频文件
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(base64.b64decode(audio_b64))
        temp_path = f.name
    
    try:
        ipa_result = await asyncio.to_thread(_model.recognize, temp_path, 'eng', True)
        logger.info(f"[{PLUGIN_NAME}] IPA 解码成功: [{ipa_result}]")
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 音频识别异常: {e}")
        ipa_result = ""
    finally:
        os.remove(temp_path) # 阅后即焚

    return {
        "status": "success",
        # 💡 核心机制：双路发射！
        # stimulus.response -> 直接原路送回给 Pythonista 显式反馈
        # wernicke.internal -> 丢给 ipa_to_text 继续处理
        "target_topics": ["stimulus.response", "wernicke.internal"],
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "data_type": "ipa", 
            "content": ipa_result
        }
    }