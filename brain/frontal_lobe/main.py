#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/brain/frontal_lobe/main.py
# ========================================================
#  1. 环境劫持与神经元挂载
# ========================================================
import os, sys, asyncio, json, re
import aiohttp
from dotenv import load_dotenv

# 动态计算根路径，确保不管在哪里拉起，都能安全将物理根目录 ~/Noagent 注入 Python 寻址空间
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

# 导入白质神经元基类
from white_matter.neuron_base import NeuronNode
from loguru import logger

# 🛡️ 物理环境隔离：精准加载根目录下的 .env 配置文件（内含 XAI_API_KEY）
load_dotenv(os.path.join(_ROOT, '.env'))

# ========================================================
#  2. 前额叶类声明与核心信号拦截
# ========================================================
class FrontalLobe(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        # 拦截丘脑网关（sensory_gateway）通过 ZMQ 广播过来的原始外部刺激
        if topic == "stimulus.raw":
            payload = message.get("payload", {})
            # 用户实际输入的文本指令
            content = payload.get("content", "")
            # 唯一的全链路追踪 ID
            trace_id = message.get("trace_id", "unknown") 
            
            logger.info(f"🤔 意图解析 (Trace: {trace_id}): [{content}]")
            
            # ==========================================
            # ⚡️ 系统 1：快速反射弧 (底层物理硬路由，兜底保护)
            # ==========================================
            # 脊髓级的本能反射！不经过大模型，检测到关键字直接熔断，防御由于云端延迟或断网导致的灾难
            if "紧急关机" in content:
                # 瞬间向运动皮层（effector）发布物理执行冲动
                await self.fire_signal("action.execute", {"command": "shutdown_host", "trace_id": trace_id})
                # 终止传导，不再触发慢思考
                return
                
            # ==========================================
            # 🧠 系统 2：Grok 4.5 深度认知 (Agentic 路由)
            # ==========================================
            logger.info(f"🌀 激活 Grok 云端皮层进行技能规划...")
            # ⚡关键高并发设计：使用 create_task 将慢思考推入 asyncio 后台
            # 这样前额叶的 ZMQ 接收主循环不会被高延迟的云端 API 请求阻塞，能继续接收下一个外部冲动
            asyncio.create_task(self._grok_cognitive_process(content, trace_id))
    # ========================================================
    #  3. Grok 4.5 深度认知网络（Agentic 技能规划）
    # ========================================================
    async def _grok_cognitive_process(self, user_input: str, trace_id: str):
        """
        调用 Grok 进行 OpenClaw 风格的技能规划与 JSON 结构化输出
        """
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            logger.error("❌ 缺失 XAI_API_KEY 环境变量！")
            return

        # 1. 动态注入系统要求与本地 Skills 列表（提示词环境劫持）
        # 强制大模型以纯 JSON 格式输出思考过程（thought）、选定技能（skill）和执行参数（params）
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
        
        # 严格匹配 xAI 官方原生 completion 端点的非流式 Payload 格式
        payload = {
            "model": "grok-4.5",
            "input": injected_prompt
        }
        
        try:
            logger.debug("  ↳ 正在通过突触向 Grok 4.5 请求规划...")
            async with aiohttp.ClientSession() as session:
                # 使用高性能异步 HTTP 库请求云端皮层
                async with session.post("https://api.x.ai/v1/responses", headers=headers, json=payload) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error(f"❌ Grok API 拒绝访问: {resp.status} - {error_text}")
                        return
                        
                    result = await resp.json()
                    
            # 兼容解析逻辑：根据 Grok API 的实际返回层级提取文本
            # 假设返回类似 {"message": "..."} 或 {"response": "..."}
            # 请根据实际 API 文档调整此处的字段提取
            raw_text = result.get("response") or result.get("text") or result.get("output", "")
            
            # 2. 健壮的 JSON 解析器 (防止大模型带 ```json 标记)
            json_match = re.search(r'\{.*\}', raw_text.replace('\n', ' '), re.DOTALL)
            if not json_match:
                raise ValueError("Grok 未返回有效的 JSON 结构。")

            # 反序列化为标准的 Python 字典    
            agent_decision = json.loads(json_match.group())
            skill = agent_decision.get("skill")
            params = agent_decision.get("params", {})
            thought = agent_decision.get("thought", "无思考过程")
            
            logger.success(f"💡 Grok 认知完毕 | 意图: {skill} | 思考: {thought}")
            
            # 3. 神经信号分发 (Hot-plug 热拔插路由核心)
            if skill == "system_control":
                # 分发给运动皮层 (Effector)
                await self.fire_signal("action.execute", {
                    "command": params.get("command"),
                    "trace_id": trace_id
                })
            elif skill == "chat_response":
                # 分发给语言中枢或直接由网关传回 Pythonista
                # 这里我们假设发回 stimulus.response 给网关去回复 WebSocket
                await self.fire_signal("stimulus.response", {
                    "client_id": "host_local_tui", # 生产中建议在 stimulus.raw 中携带并在此处透传真实 client_id
                    "reply": params.get("reply"),
                    "trace_id": trace_id
                })
            elif skill == "synapse_rewire":
                # 【亮点特性】神经可塑性控制！指示执行器去重写特定脑区的 synapse.yaml 突触配置文件
                await self.fire_signal("action.execute", {
                    "command": "rewire_yaml",
                    "target_node": params.get("target_node"),
                    "topic_to_add": params.get("topic_to_add"),
                    "trace_id": trace_id
                })
            else:
                logger.warning(f"⚠️ Grok 幻觉了一个不存在的技能: {skill}")

        except Exception as e:
            # 异常处理：突触断裂时发送兜底提示，防止外部探针无限期挂起挂死
            logger.error(f"❌ 大模型中枢断裂: {e}")
            await self.fire_signal("stimulus.response", {
                "reply": "脑区突触异常，Grok 连接失败。",
                "trace_id": trace_id
            })

if __name__ == "__main__":
    # 初始化前额叶，加载局部突触和全局黄页，并以阻塞模式（.run()）启动进程监听
    FrontalLobe(
        os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
        os.path.join(_ROOT, "dna", "known_nodes.yaml")
    ).run()