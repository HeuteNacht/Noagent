#!/usr/bin/env python3
import os, sys, asyncio
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)
from white_matter.neuron_base import NeuronNode
from loguru import logger

class FrontalLobe(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "stimulus.raw":
            payload = message.get("payload", {})
            content = payload.get("content", "")
            # 继承 trace_id，方便全链路追踪
            trace_id = message.get("trace_id", "unknown") 
            
            logger.info(f"🤔 意图解析 (Trace: {trace_id}): [{content}]")
            
            # ==========================================
            # ⚡️ 系统 1：快速反射弧 (正则/关键词匹配)
            # ==========================================
            if "唤醒" in content and "babe" in content.lower():
                await self.fire_signal("action.execute", {"command": "wake_babe_server", "trace_id": trace_id})
                return
                
            if "关机" in content:
                await self.fire_signal("action.execute", {"command": "shutdown_host", "trace_id": trace_id})
                return
                
            # ==========================================
            # 🧠 系统 2：深度认知 (LLM 语义理解)
            # ==========================================
            logger.info(f"🌀 未知指令，激活 LLM 深度思考...")
            # 使用 create_task 扔到后台，防止阻塞主感受循环
            asyncio.create_task(self._llm_cognitive_process(content, trace_id))

    async def _llm_cognitive_process(self, content: str, trace_id: str):
        """
        调用 LLM 进行意图识别与自然语言处理
        """
        try:
            # TODO: 替换为你实际的 LLM 异步 API 调用 (如 OpenAI, Anthropic, Ollama 等)
            # 提示词技巧：要求 LLM 输出 JSON 格式，以便决定是“执行动作”还是“语言回复”
            logger.debug("  ↳ 正在与 LLM 突触交换数据...")
            
            # 模拟 LLM 网络延迟
            await asyncio.sleep(2) 
            
            # 假设 LLM 返回的解析结果
            llm_response = {
                "intent_type": "chat", # 可能是 'command' 或 'chat'
                "reply_text": "我不太明白具体的物理指令，但我们可以聊聊这个话题。"
            }
            
            if llm_response["intent_type"] == "command":
                # LLM 识别出了潜在的系统命令
                await self.fire_signal("action.execute", {
                    "command": llm_response.get("target_command"),
                    "trace_id": trace_id
                })
            else:
                # 只是普通的闲聊，触发语言中枢 (Broca 区) 发声
                await self.fire_signal("speech.synthesize", {
                    "text": llm_response["reply_text"],
                    "trace_id": trace_id
                })
                
        except Exception as e:
            logger.error(f"❌ LLM 认知中枢异常: {e}")
            await self.fire_signal("speech.synthesize", {
                "text": "抱歉，我的深层思维模块刚刚走神了。",
                "trace_id": trace_id
            })

if __name__ == "__main__":
    FrontalLobe(
        os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
        os.path.join(_ROOT, "dna", "known_nodes.yaml")
    ).run()
