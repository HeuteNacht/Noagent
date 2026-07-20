#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/brain/frontal_lobe/main.py

import os
import sys
import json
import asyncio
import aiohttp
from loguru import logger

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from dotenv import load_dotenv
from white_matter.neuron_base import NeuronNode

class FrontalLobe(NeuronNode):
    def __init__(self):
        super().__init__(
            local_config_path=os.path.join(os.path.dirname(__file__), "synapse.yaml"),
            connectome_path=os.path.join(_ROOT_DIR, "dna", "known_nodes.yaml")
        )
        
        self.register_receptor("stimulus.raw")
        
        env_path = os.path.join(_ROOT_DIR, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info("🔐 已成功解析局部 .env 基因保险箱。")
        
        self.api_key = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ 缺失 GROK_API_KEY / XAI_API_KEY 凭证，认知皮层将被物理切断！")

    async def process_signal(self, topic: str, message: dict):
        payload = message.get("payload", {})
        
        trace_id = message.get("trace_id", "unknown")
        client_id = payload.get("client_id", "unknown")
        content = payload.get("content", "").strip()

        logger.info(f"🤔 意图解析 (Trace: {trace_id} | Client: {client_id}): {content}")
        
        if not content:
            return

        if content == "[[SYSTEM_HANDSHAKE_PING]]":
            logger.info("⚡ 触发本地反射弧：无感处理心跳握手。")
            await self.fire_signal("stimulus.response", {
                "trace_id": trace_id,
                "client_id": client_id,
                "reply": "Noa 中枢前额叶已就绪。神经递质传输畅通。"
            })
            return

        logger.info("🌀 激活 Grok 云端皮层进行深度思考...")
        reply = await self._grok_cognitive_process(content)
        
        await self.fire_signal("stimulus.response", {
            "trace_id": trace_id,
            "client_id": client_id,
            "reply": reply
        })

    async def _adaptive_routing_request(self, url: str, headers: dict, data: dict) -> dict:
        env_proxy = os.environ.get("NOA_PROXY") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        
        strategies = []
        if env_proxy:
            strategies.append(("Env Proxy", env_proxy))
            
        strategies.extend([
            ("X-ray Socks5", "socks5://127.0.0.1:10808"),
            ("X-ray HTTP", "http://127.0.0.1:10809"),
            ("Direct Mode", None)
        ])

        seen = set()
        unique_strategies = []
        for name, proxy in strategies:
            if proxy not in seen:
                seen.add(proxy)
                unique_strategies.append((name, proxy))

        for name, proxy_url in unique_strategies:
            logger.debug(f"  ↳ 尝试激活路由策略 [{name}] ...")
            try:
                if proxy_url and "socks" in proxy_url.lower():
                    from aiohttp_socks import ProxyConnector
                    connector = ProxyConnector.from_url(proxy_url)
                    async with aiohttp.ClientSession(connector=connector) as session:
                        async with session.post(url, headers=headers, json=data, timeout=6.0) as response:
                            if response.status == 200:
                                return await response.json()
                else:
                    async with aiohttp.ClientSession(trust_env=True) as session:
                        async with session.post(url, headers=headers, json=data, proxy=proxy_url, timeout=6.0) as response:
                            if response.status == 200:
                                return await response.json()
            except Exception as e:
                logger.debug(f"  ↳ 策略 [{name}] 折跃失败: {type(e).__name__}")
                continue
                
        raise ConnectionError("所有网络突触路由均宣告折跃失败。")

    async def _grok_cognitive_process(self, user_input: str) -> str:
        if not self.api_key:
            return "❌ 认知阻断：未发现 API 密钥，脑区陷入停滞。请检查 .env 文件。"

        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        system_prompt = (
            "你是 Noa，一个运行在分布式 ZMQ 神经元网络上的具身智能中枢大脑。"
            "你的语言风格应该极客、冷峻、充满仿生学或赛博朋克色彩。"
            "直接回答问题，避免冗长的解释，你的输出会直接呈现在黑客终端上。"
        )

        data = {
            "model": "grok-beta", 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.6 
        }

        logger.debug(f"  ↳ 正在通过超空间突触向 Grok 请求规划...")
        
        try:
            result = await self._adaptive_routing_request(url, headers, data)
            reply = result['choices'][0]['message']['content']
            logger.success("✅ 云端皮层计算完毕，神经冲动已顺畅回流！")
            return reply
            
        except ConnectionError:
            logger.error("❌ 大模型中枢断裂: 所有代理与直连通道均超时。")
            return "⏳ 认知超时：Grok 突触在超空间折跃失败，请检查边缘网络结界。"
        except Exception as e:
            logger.error(f"❌ 突触崩溃: {e}")
            return f"💥 神经突触发生未知物理崩溃: {e}"

if __name__ == "__main__":
    FrontalLobe().run()
