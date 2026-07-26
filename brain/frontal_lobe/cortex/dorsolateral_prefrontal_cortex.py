# -*- coding: utf-8 -*-
# Noagent/brain/frontal_lobe/cortex/dorsolateral_prefrontal_cortex.py
import os
import aiohttp
from loguru import logger
from dotenv import load_dotenv

PLUGIN_NAME = "Dorsolateral Prefrontal Cortex (LLM Reasoning)"

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
        logger.warning(f"⚠️ [{PLUGIN_NAME}] 缺失凭证，认知皮层将被物理切断！")

async def can_process(request: dict) -> bool:
    """逻辑兜底：处理除握手以外的所有复杂指令"""
    content = request.get("content", "")
    return bool(content and content != "[[SYSTEM_HANDSHAKE_PING]]")

async def process(request: dict) -> dict:
    """核心推理逻辑"""
    if not _API_KEY:
        return _build_response(request, "❌ 认知阻断：未发现 API 密钥，请检查环境变量。")

    content = request.get("content")
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {_API_KEY}"}
    data = {
        "model": "grok-latest",
        "messages": [
            {"role": "system", "content": "你是 Noa，分布式具身智能中枢。风格冷峻、极客。"}, 
            {"role": "user", "content": content}
        ],
        "temperature": 0.6
    }

    try:
        logger.debug(f"[{PLUGIN_NAME}] 正在折跃...")
        result = await _adaptive_request(url, headers, data)
        reply = result['choices'][0]['message']['content']
        return _build_response(request, reply)
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 崩溃: {e}")
        return _build_response(request, f"💥 认知皮层异常: {e}")

def _build_response(request: dict, reply_text: str) -> dict:
    return {
        "status": "success",
        "target_topic": "stimulus.response",
        "payload": {"trace_id": request.get("trace_id"), "client_id": request.get("client_id"), "reply": reply_text}
    }

# 👇 完美复刻你的多路自适应路由与记忆烙印
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
                    async with session.post(url, headers=headers, json=data, timeout=30.0) as response:
                        if response.status == 200:
                            with open(_ROUTE_MEMORY_PATH, 'w') as f: f.write(name)
                            return await response.json()
                        else:
                            raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
            else:
                async with aiohttp.ClientSession(trust_env=True) as session:
                    async with session.post(url, headers=headers, json=data, proxy=proxy_url, timeout=30.0) as response:
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
