#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/brain/sensory_gateway/main.py
# ========================================================
#  1. 环境初始化与依赖导入
# ========================================================
import os, sys, asyncio, json, shutil
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from white_matter.neuron_base import NeuronNode
from loguru import logger

# 🎯 【FastAPI/Uvicorn 事件循环劫持】
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ========================================================
#  2. 免疫系统与突触池定义
# ========================================================
APPROVED_DB = os.path.join(_ROOT, "dna", "approved_devices.json")
APPROVED_TEMPLATE = os.path.join(_ROOT, "dna", "approved_devices.json.example")
PENDING_DB = os.path.join(_ROOT, "dna", "pending_devices.json")

_APPROVED_CACHE = set()
_PENDING_CACHE = set()
_DENIED_CACHE = set()

class ConnectionManager:
    """突触连接池：用于管理并发的游离神经探针"""
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"🔌 [突触断开] 设备离线: {client_id}")

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(json.dumps(message))
        else:
            logger.warning(f"⚠️ [投递失败] 目标设备 {client_id} 已游离或断开连接。")

manager = ConnectionManager()

# ========================================================
#  3. 免疫机制核心函数
# ========================================================
def init_immune_system():
    global _APPROVED_CACHE, _PENDING_CACHE
    
    if not os.path.exists(APPROVED_DB):
        if os.path.exists(APPROVED_TEMPLATE):
            shutil.copy(APPROVED_TEMPLATE, APPROVED_DB)
            logger.info("🧬 [基因转录] 未检测到物理免疫库，已从原始 DNA 模板逆转录白名单！")
        else:
            logger.warning("⚠️ [免疫缺陷] 未找到模板文件 approved_devices.json.example，白名单初始化可能受阻。")

    if os.path.exists(APPROVED_DB):
        try:
            with open(APPROVED_DB, 'r') as f:
                _APPROVED_CACHE = set(json.load(f))
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"🚨 [DNA 序列变异] approved_devices.json 语法损坏 ({e})！正在自动从模板自愈重置...")
            if os.path.exists(APPROVED_TEMPLATE):
                shutil.copy(APPROVED_TEMPLATE, APPROVED_DB)
                with open(APPROVED_DB, 'r') as f:
                    _APPROVED_CACHE = set(json.load(f))

    if os.path.exists(PENDING_DB):
        try:
            with open(PENDING_DB, 'r') as f:
                _PENDING_CACHE = set(json.load(f))
        except (json.JSONDecodeError, ValueError):
            _PENDING_CACHE = set()

    logger.info(f"🛡️ 免疫系统初始化: {_APPROVED_CACHE}")

def sync_pending_to_disk():
    with open(PENDING_DB, 'w') as f:
        json.dump(list(_PENDING_CACHE), f, indent=4)

async def check_and_log_device_async(client_id: str) -> bool:
    if client_id in _DENIED_CACHE:
        logger.error(f"☠️ [黑名单绞杀] 恶意设备被底层防御击碎: {client_id}")
        return False
    if client_id in _APPROVED_CACHE: return True
    if client_id not in _PENDING_CACHE:
        _PENDING_CACHE.add(client_id)
        await asyncio.to_thread(sync_pending_to_disk)
    return False

# ========================================================
#  4. 仿生神经元节点的构建 (双向闭环与多模态升级)
# ========================================================
class SensoryGateway(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        """
        拦截内网的回传递质 (兼容文本 reply 与 语音解码的 content)
        """
        if topic in ["stimulus.response", "brain.reply"]:
            payload = message.get("payload", {})
            client_id = payload.get("client_id")
            
            # 💡 无损兼容升级：优先取 reply，如果没有则取 content (韦尼克区发来的格式)
            reply_text = payload.get("reply") or payload.get("content")
            trace_id = payload.get("trace_id", "unknown")
            data_type = payload.get("data_type", "text") 
            
            if client_id and reply_text:
                logger.info(f"📤 [网关回传] 意图解析完毕 (Trace: {trace_id}, Type: {data_type}) -> 正在推送至: {client_id}")
                
                await manager.send_personal_message({
                    "status": "success",
                    "reply": reply_text,       
                    "content": reply_text,     
                    "data_type": data_type,    
                    "trace_id": trace_id
                }, client_id)

gateway_node = SensoryGateway(
    os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
    os.path.join(_ROOT, "dna", "known_nodes.yaml")
)

# 🚨 极其关键的一行：必须在这里初始化 app！
app = FastAPI()

# ========================================================
#  5. 生命周期钩子与 WebSocket 核心交互逻辑
# ========================================================
@app.post("/internal/reload_immune")
async def reload_immune():
    init_immune_system()
    logger.success("⚡ [瞬态脉冲] 收到控制台热重载指令，免疫基因库已无感刷新！")
    return {"status": "reloaded"}

@app.on_event("startup")
async def on_startup():
    init_immune_system()
    asyncio.create_task(gateway_node.listen())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_client_id = None 
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                signal = json.loads(data)
                client_id = signal.get("client_id", "unknown_device")
                current_client_id = client_id
                
                # 🛡️ 零信任准入检测
                if not await check_and_log_device_async(client_id):
                    logger.warning(f"⛔️ [免疫拦截] 发现陌生设备试图接入: {client_id}")
                    await websocket.send_text(json.dumps({
                        "error": "Unauthorized", 
                        "message": f"设备 {client_id} 未授权，请在终端执行 'noa approve' 批准。"
                    }))
                    await websocket.close(code=4003)
                    return
                
                await manager.connect(client_id, websocket)
                signal["client_id"] = client_id 
                
                # 💡 核心升级：动态路由分流引擎
                data_type = signal.get("type", "text")
                if data_type == "audio_chunk":
                    target_bus = "stimulus.audio" # 🎧 语音流 -> 投射给韦尼克听觉区
                    logger.success(f"🔓 [音频注入] 合法设备: {client_id} -> 路由至: {target_bus}")
                elif data_type in ["image", "image_chunk"]:
                    target_bus = "stimulus.visual" # 👁️ 图像流 -> 投射给枕叶视觉区
                    logger.success(f"🔓 [图像注入] 合法设备: {client_id} -> 路由至: {target_bus}")
                else:
                    target_bus = "stimulus.raw"   # 📝 文本流 -> 投射给前额叶
                    logger.success(f"🔓 [文本注入] 合法设备: {client_id} -> 路由至: {target_bus}")
                
                await gateway_node.fire_signal(target_bus, signal)
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid Format"}))
                
    except WebSocketDisconnect:
        if current_client_id:
            manager.disconnect(current_client_id)

async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=22222, log_level="warning")
    await uvicorn.Server(config).serve()

if __name__ == "__main__": 
    asyncio.run(main())