#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/brain/frontal_lobe/main.py

import os
import sys
import json
import asyncio
import aiohttp
from loguru import logger

# 🎯 核心修复：物理环境寻址劫持，确保 Python 能找到 white_matter 基类
_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from dotenv import load_dotenv
from white_matter.neuron_base import NeuronNode

class FrontalLobe(NeuronNode):
    def __init__(self):
        # 1. 物理位置与突触锚定
        super().__init__(
            local_config_path=os.path.join(os.path.dirname(__file__), "synapse.yaml"),
            connectome_path=os.path.join(_ROOT_DIR, "dna", "known_nodes.yaml")
        )
        # 监听来自网关的原始刺激信号
        self.register_receptor("stimulus.raw")
        
        # 👈 2. 向上追溯，精准定位物理根目录的 .env 基因锁
        env_path = os.path.join(_ROOT_DIR, '.env')
        
        # 嗅探并吸收配置
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info("🔐 已成功解析局部 .env 基因保险箱。")
        
        # 3. 认知密钥加载 (现在它可以直接从 .env 吸收了)
        self.api_key = os.environ.get("GROK_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ 缺失 GROK_API_KEY 凭证，认知皮层将被物理切断！")

    async def process_signal(self, topic: str, payload: dict):
        """处理捕获到的神经脉冲"""
        trace_id = payload.get("trace_id", "unknown")
        client_id = payload.get("client_id", "unknown")
        content = payload.get("content", "").strip()

        logger.info(f"🤔 意图解析 (Trace: {trace_id} | Client: {client_id}): {content}")

        # 🛡️ 本地反射弧拦截：对于底层的握手和心跳，直接由小脑本能回应，不经过耗时的大模型思考
        if content == "[[SYSTEM_HANDSHAKE_PING]]":
            logger.info("⚡ 触发本地反射弧：无感处理心跳握手。")
            await self.fire_signal("stimulus.response", {
                "trace_id": trace_id,
                "client_id": client_id,
                "reply": "Noa 中枢前额叶已就绪。神经递质传输畅通。"
            })
            return

        # 🌀 触发大模型深层认知
        logger.info("🌀 激活 Grok 云端皮层进行深度思考...")
        reply = await self._grok_cognitive_process(content)
        
        # ⚡ 认知完成，通过白质网络 (ZMQ) 将决策动作电位回传给网关
        await self.fire_signal("stimulus.response", {
            "trace_id": trace_id,
            "client_id": client_id,
            "reply": reply
        })

    async def _grok_cognitive_process(self, user_input: str) -> str:
        """对接 xAI (Grok) 的云端神经突触"""
        if not self.api_key:
            return "❌ 认知阻断：未发现 GROK_API_KEY，脑区陷入停滞。"

        # xAI 标准 Chat Completions 终端节点
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 🧠 注入系统潜意识 (System Prompt)：定义 Noa 的基础人格与回答范式
        system_prompt = (
            "你是 Noa，一个运行在分布式 ZMQ 神经元网络上的具身智能中枢大脑。"
            "你的语言风格应该极客、冷峻、充满仿生学或赛博朋克色彩。"
            "直接回答问题，避免冗长的解释，你的输出会直接呈现在黑客终端上。"
        )

        data = {
            "model": "grok-beta", # 你也可以切换为 "grok-2-latest"
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.6 # 保持逻辑严谨性
        }

        logger.debug(f"  ↳ 正在通过超空间突触向 Grok 请求规划...")
        
        try:
            # ⚡ 核心异步调用：不阻塞底层的 ZMQ 监听循环
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=20.0) as response:
                    if response.status == 200:
                        result = await response.json()
                        reply = result['choices'][0]['message']['content']
                        logger.success("✅ 云端皮层计算完毕，神经冲动已回流！")
                        return reply
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ 大模型中枢断裂 (HTTP {response.status}): {error_text}")
                        return f"⚠️ 认知皮层遭遇异常电磁干扰 (HTTP {response.status})。"
                        
        except asyncio.TimeoutError:
            logger.error("❌ 大模型中枢断裂: Connection timeout to host api.x.ai")
            return "⏳ 认知超时：Grok 突触连接断开，请检查边缘网络结界。"
        except Exception as e:
            logger.error(f"❌ 突触崩溃: {e}")
            return f"💥 神经突触发生未知物理崩溃: {e}"

if __name__ == "__main__":
    FrontalLobe().run()