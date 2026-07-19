#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境劫持与神经元挂载
# ========================================================
import os, sys, asyncio, json, re
import aiohttp
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

from white_matter.neuron_base import NeuronNode
from loguru import logger

# 🛡️ 物理环境隔离：精准加载根目录下的 .env 配置文件
load_dotenv(os.path.join(_ROOT, '.env'))

# ========================================================
#  2. 前额叶类声明与核心信号拦截
# ========================================================
class FrontalLobe(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "stimulus.raw":
            payload = message.get("payload", {})
            content = payload.get("content", "")
            trace_id = message.get("trace_id", "unknown") 
            
            # 🎯 溯源透传改造：动态提取外部游离探针的物理身份标识
            client_id = payload.get("client_id") or message.get("client_id", "unknown_device")
            
            logger.info(f"🤔 意图解析 (Trace: {trace_id} | Client: {client_id}): [{content}]")
            
            # ==========================================
            # ⚡️ 系统 1：快速反射弧 (兜底保护)
            # ==========================================
            if "紧急关机" in content:
                await self.fire_signal("action.execute", {"command": "shutdown_host", "trace_id": trace_id})
                return
                
            # ==========================================
            # 🧠 系统 2：Grok 4.5 深度认知 (Agentic 路由)
            # ==========================================
            logger.info(f"🌀 激活 Grok 云端皮层进行技能规划...")
            # 携带着溯源 client_id 进入慢思考后台任务
            asyncio.create_task(self._grok_cognitive_process(content, trace_id, client_id))

    # ========================================================
    #  3. Grok 4.5 深度认知网络
    # ========================================================
    async def _grok_cognitive_process(self, user_input: str, trace_id: str, client_id: str):
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            logger.error("❌ 缺失 XAI_API_KEY 环境变量！")
            return

        injected_prompt = f"""[SYSTEM]
You are Noa, an autonomous neural gateway. You act as an intelligent router.
Based on the [USER INPUT], select the appropriate skill and extract parameters.

[AVAILABLE SKILLS]
1. "system_control": For physical or network actions (e.g., wake_babe_server).
   - Params: {{"command": "<target_command>"}}
2. "chat_response": For answering questions.
   - Params: {{"reply": "<response>"}}
3. "synapse_rewire": 动态神经可塑性。When the user asks a specific node to listen to or subscribe to a new topic, use this.
   - Params: {{"target_node": "<e.g., sensory_gateway>", "topic_to_add": "<e.g., stimulus.response>"}}

[OUTPUT FORMAT]
Must be valid JSON.
{{
    "thought": "brief reasoning",
    "skill": "chosen_skill",
    "params": {{ ... }}
}}

[USER INPUT]
{user_input}
"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 🛡️ 空行与贪婪匹配防御：强制大模型在 API 级别返回结构化 JSON
        payload = {
            "model": "grok-4.5",
            "input": injected_prompt,
            "response_format": {"type": "json_object"}
        }
        
        try:
            logger.debug("  ↳ 正在通过突触向 Grok 4.5 请求规划...")
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.x.ai/v1/responses", headers=headers, json=payload) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error(f"❌ Grok API 拒绝访问: {resp.status} - {error_text}")
                        return
                        
                    result = await resp.json()
                    
            raw_text = result.get("response") or result.get("text") or result.get("output", "")
            
            # 🎯 JSON 解析优化：由于开启了 response_format，优先尝试直接反序列化
            try:
                agent_decision = json.loads(raw_text.strip())
            except json.JSONDecodeError:
                # 兜底：如果模型依然抽风返回了 Markdown 标记，进行非贪婪的正则剥离
                json_match = re.search(r'\{.*?\}', raw_text.replace('\n', ' '), re.DOTALL)
                if not json_match:
                    raise ValueError("Grok 未返回有效的 JSON 结构。")
                agent_decision = json.loads(json_match.group())

            skill = agent_decision.get("skill")
            params = agent_decision.get("params", {})
            thought = agent_decision.get("thought", "无思考过程")
            
            logger.success(f"💡 Grok 认知完毕 | 意图: {skill} | 思考: {thought}")
            
            # 3. 神经信号分发 (Hot-plug 路由核心)
            if skill == "system_control":
                await self.fire_signal("action.execute", {
                    "command": params.get("command"),
                    "trace_id": trace_id
                })
            elif skill == "chat_response":
                # 🎯 溯源回传：将动态提取的 client_id 精准打回给丘脑网关
                await self.fire_signal("stimulus.response", {
                    "client_id": client_id, 
                    "reply": params.get("reply"),
                    "trace_id": trace_id
                })
            elif skill == "synapse_rewire":
                await self.fire_signal("action.execute", {
                    "command": "rewire_yaml",
                    "target_node": params.get("target_node"),
                    "topic_to_add": params.get("topic_to_add"),
                    "trace_id": trace_id
                })
            else:
                logger.warning(f"⚠️ Grok 幻觉了一个不存在的技能: {skill}")

        except Exception as e:
            logger.error(f"❌ 大模型中枢断裂: {e}")
            # 发生异常时，同样将报警信息精准投递给提问的终端
            await self.fire_signal("stimulus.response", {
                "client_id": client_id,
                "reply": "脑区突触异常，Grok 连接或解析失败。",
                "trace_id": trace_id
            })

if __name__ == "__main__":
    FrontalLobe(
        os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
        os.path.join(_ROOT, "dna", "known_nodes.yaml")
    ).run()