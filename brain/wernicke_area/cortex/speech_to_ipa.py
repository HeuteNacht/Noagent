# -*- coding: utf-8 -*-
import asyncio
from loguru import logger

PLUGIN_NAME = "Auditory Cortex (Speech -> IPA)"
_model = None

def awaken(root_dir, current_dir):
    """启动时将 Allosaurus 声学模型装载入内存"""
    global _model
    try:
        from allosaurus.app import read_recognizer
        logger.info(f"[{PLUGIN_NAME}] 正在装载 Allosaurus 语音识别内核...")
        _model = read_recognizer()
        logger.success(f"[{PLUGIN_NAME}] Allosaurus 模型装载完毕！")
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 依赖缺失或模型装载失败: {e}")

async def can_process(request: dict) -> bool:
    """受体：专门接管音频数据"""
    return request.get("data_type") == "audio"

async def process(request: dict) -> dict:
    if not _model:
        logger.error(f"[{PLUGIN_NAME}] 模型未初始化，拒绝处理。")
        return {"status": "error"}

    audio_path = request.get("content")
    logger.info(f"[{PLUGIN_NAME}] 正在提取音频 IPA 音标特征: {audio_path}")
    
    try:
        # 🚨 必须放入 asyncio.to_thread 防止 CPU 密集的声学计算阻塞整个 ZMQ 异步主循环
        ipa_result = await asyncio.to_thread(_model.recognize, audio_path, 'eng', True)
        logger.info(f"[{PLUGIN_NAME}] 提取得 IPA 序列: [{ipa_result}]")
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 音频识别异常: {e}")
        return {"status": "error"}

    return {
        "status": "success",
        "target_topic": "wernicke.internal",  # 内部接力频道
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "data_type": "ipa",                # 状态机转为 ipa
            "content": ipa_result
        }
    }
