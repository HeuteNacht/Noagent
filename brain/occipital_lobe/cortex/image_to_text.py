# -*- coding: utf-8 -*-
# Noagent/brain/occipital_lobe/cortex/image_to_text.py
import os
import aiohttp
from loguru import logger
from dotenv import load_dotenv

PLUGIN_NAME = "Visual Cortex (Grok Vision)"

_API_KEY = None
_ROUTE_MEMORY_PATH = None

def awaken(root_dir, current_dir):
    """装载密钥与网络记忆"""
    global _API_KEY, _ROUTE_MEMORY_PATH
    _ROUTE_MEMORY_PATH = os.path.join(current_dir, ".synapse_route.cache")
    env_path = os.path.join(root_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    _API_KEY = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")
    if not _API_KEY:
        logger.warning(f"⚠️ [{PLUGIN_NAME}] 缺失凭证，视觉皮层将被物理切断！")

async def can_process(request: dict) -> bool:
    """拦截图像脉冲"""
    dtype = request.get("data_type") or request.get("type")
    content = request.get("content")
    return dtype in ["image", "image_chunk"] and bool(content)

async def process(request: dict) -> dict:
    """视觉核心推理逻辑"""
    if not _API_KEY:
        return _build_response(request, "❌ 视觉阻断：未发现 API 密钥，请检查环境变量。")

    base64_image = request.get("content")
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {_API_KEY}"}
    
    # 构建兼容 OpenAI Vision 规范的载荷格式
    data = {
        "model": "grok-vision-beta", # 或根据 X.AI 最新的 vision 模型名替换为 grok-latest
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "你是 Noa，分布式具身智能中枢。分析这张图像，提取其核心内容与细节，以冷峻、极客的风格进行描述。"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "temperature": 0.6
    }

    try:
        logger.debug(f"[{PLUGIN_NAME}] 正在向高维视觉模型折跃特征矩阵...")
        result = await _adaptive_request(url, headers, data)
        reply = result['choices'][0]['message']['content']
        return _build_response(request, reply)
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 崩溃: {e}")
        return _build_response(request, f"💥 视觉皮层异常: {e}")

def _build_response(request: dict, reply_text: str) -> dict:
    return {
        "status": "success",
        "target_topics": ["stimulus.response"], # 适配枕叶的多路发射数组
        "payload": {
            "trace_id": request.get("trace_id"), 
            "client_id": request.get("client_id"), 
            "data_type": "text", 
            "reply": reply_text,
            "content": reply_text
        }
    }

# 👇 完美复刻的多路自适应路由与记忆烙印
async def _adaptive_request(url, headers, data):
    env_proxy = os.environ.get("NOA_PROXY") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    
    strategies = []
    if env_proxy:
        strategies.append(("Env Proxy", env_proxy))
        
    strategies.extend([
        ("X-ray Socks5", "socks5://127.0.0.1:10808"),
        ("X-ray HTTP", "http://127.0.0.1:10809"),
        ("Direct Mode", None)
    ])

    seen, unique_strategies = set(), []
    for name, proxy in strategies:
        if name not in seen:
            seen.add(name)
            unique_strategies.append((name, proxy))

    preferred_route = None
    if os.path.exists(_ROUTE_MEMORY_PATH):
        try:
            with open(_ROUTE_MEMORY_PATH, 'r') as f:
                preferred_route = f.read().strip()
        except Exception: pass
            
    if preferred_route:
        for i, (name, proxy) in enumerate(unique_strategies):
            if name == preferred_route:
                unique_strategies.insert(0, unique_strategies.pop(i))
                break

    for name, proxy_url in unique_strategies:
        try:
            if proxy_url and "socks" in proxy_url.lower():
                from aiohttp_socks import ProxyConnector
                connector = ProxyConnector.from_url(proxy_url)
                async with aiohttp.ClientSession(connector=connector) as session:
                    # 考虑到图像上传较慢，超时时间从 30 增加到 60 秒
                    async with session.post(url, headers=headers, json=data, timeout=60.0) as response:
                        if response.status == 200:
                            with open(_ROUTE_MEMORY_PATH, 'w') as f: f.write(name)
                            return await response.json()
                        else:
                            raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
            else:
                async with aiohttp.ClientSession(trust_env=True) as session:
                    async with session.post(url, headers=headers, json=data, proxy=proxy_url, timeout=60.0) as response:
                        if response.status == 200:
                            with open(_ROUTE_MEMORY_PATH, 'w') as f: f.write(name)
                            return await response.json()
                        else:
                            raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
        except RuntimeError as re:
            raise re
        except Exception as e:
            logger.debug(f"  💥 策略 [{name}] 折跃失败: {type(e).__name__}")
            continue
            
    raise ConnectionError("所有网络突触路由均宣告折跃失败。")