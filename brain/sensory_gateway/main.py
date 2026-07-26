#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
# 必须在 Uvicorn 启动前强行将 Windows 策略扭转为 Selector 模式，否则网关的 ZMQ 后台任务必崩
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
        # 记录 client_id -> WebSocket 的物理映射
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

# 实例化突触连接池
manager = ConnectionManager()

# ========================================================
#  3. 免疫机制核心函数
# ========================================================

def init_immune_system():
    global _APPROVED_CACHE, _PENDING_CACHE
    
    # 🧬 [基因表达代偿] 若缺少显性抗原序列，强行从原始 DNA 模板转录出基础免疫库
    if not os.path.exists(APPROVED_DB):
        if os.path.exists(APPROVED_TEMPLATE):
            shutil.copy(APPROVED_TEMPLATE, APPROVED_DB)
            logger.info("🧬 [基因转录] 未检测到物理免疫库，已从原始 DNA 模板逆转录白名单！")
        else:
            logger.warning("⚠️ [免疫缺陷] 未找到模板文件 approved_devices.json.example，白名单初始化可能受阻。")

    # 🛡️ [DNA 序列自愈保护] 防止 JSON 格式损坏导致网关崩溃
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
    # 0. 黑名单物理绞杀：O(1) 复杂度瞬间判定，节省算力
    if client_id in _DENIED_CACHE:
        logger.error(f"☠️ [黑名单绞杀] 恶意设备被底层防御击碎: {client_id}")
        return False
    if client_id in _APPROVED_CACHE: return True
    if client_id not in _PENDING_CACHE:
        _PENDING_CACHE.add(client_id)
        await asyncio.to_thread(sync_pending_to_disk)
    return False

# ========================================================
#  4. 仿生神经元节点的构建 (双向闭环升级)
# ========================================================
class SensoryGateway(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        """
        拦截内网的回传递质 (例如从 FrontalLobe 发出的 stimulus.response)
        """
        # 兼容你的可能性分析设计，这里监听 response 或 reply
        if topic in ["stimulus.response", "brain.reply"]:
            payload = message.get("payload", {})
            client_id = payload.get("client_id")
            reply_text = payload.get("reply")
            trace_id = payload.get("trace_id", "unknown")
            
            if client_id and reply_text:
                logger.info(f"📤 [网关回传] 意图解析完毕 (Trace: {trace_id}) -> 正在推送至: {client_id}")
                # 精准路由：只把消息发给提问的那个终端！
                await manager.send_personal_message({
                    "status": "success",
                    "reply": reply_text,
                    "trace_id": trace_id
                }, client_id)

gateway_node = SensoryGateway(
    os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
    os.path.join(_ROOT, "dna", "known_nodes.yaml")
)
app = FastAPI()

# ========================================================
#  5. 生命周期钩子与 WebSocket 核心交互逻辑
# ========================================================
@app.on_event("startup")
async def on_startup():
    init_immune_system()
    asyncio.create_task(gateway_node.listen())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_client_id = None # 用于记录当前连接的身份，方便断开时清理
    
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
                
                # 登记/刷新 突触连接池 (让网关记住这个设备，为回调做准备)
                await manager.connect(client_id, websocket)
                
                logger.success(f"🔓 [信号注入] 合法设备: {client_id}")
                
                # 将 client_id 强行注入 payload，确保前额叶能把这个 ID 原样传回来
                signal["client_id"] = client_id 
                
                # 发送到内网
                await gateway_node.fire_signal("stimulus.raw", signal)
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid Format"}))
                
    except WebSocketDisconnect:
        # 当设备断开连接时，从突触池中注销
        if current_client_id:
            manager.disconnect(current_client_id)

async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=22222, log_level="warning")
    await uvicorn.Server(config).serve()

if __name__ == "__main__": 
    asyncio.run(main())
