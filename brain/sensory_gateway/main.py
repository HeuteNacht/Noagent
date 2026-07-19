#!/usr/bin/env python3
import os, sys, asyncio, json
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from white_matter.neuron_base import NeuronNode
from loguru import logger
# ========================================================
# 🧬 补全缺失的免疫数据库物理路径
# ========================================================
APPROVED_DB = os.path.join(_ROOT, "dna", "approved_devices.json")
PENDING_DB = os.path.join(_ROOT, "dna", "pending_devices.json")

# 免疫记忆缓存（内存态）
_APPROVED_CACHE = set()
_PENDING_CACHE = set()

def init_immune_system():
    """网关启动时将 DNA (JSON) 加载到内存"""
    global _APPROVED_CACHE, _PENDING_CACHE
    if os.path.exists(APPROVED_DB):
        with open(APPROVED_DB, 'r') as f:
            _APPROVED_CACHE = set(json.load(f))
    if os.path.exists(PENDING_DB):
        with open(PENDING_DB, 'r') as f:
            _PENDING_CACHE = set(json.load(f))
    logger.info(f"🛡️ 免疫系统初始化: {_APPROVED_CACHE}")

def sync_pending_to_disk():
    """将待审批设备写回磁盘（后台执行）"""
    with open(PENDING_DB, 'w') as f:
        json.dump(list(_PENDING_CACHE), f, indent=4)

async def check_and_log_device_async(client_id: str) -> bool:
    """
    异步非阻塞的零信任检测
    """
    # 1. 内存级闪电校验，完全不阻塞
    if client_id in _APPROVED_CACHE:
        return True
    
    # 2. 如果是新来的陌生设备，加入缓存
    if client_id not in _PENDING_CACHE:
        _PENDING_CACHE.add(client_id)
        # 将磁盘写入操作推入线程池，防止阻塞 FastAPI 异步循环
        await asyncio.to_thread(sync_pending_to_disk)
        
    return False

class SensoryGateway(NeuronNode):
    async def process_signal(self, topic: str, message: dict): pass

gateway_node = SensoryGateway(
    os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
    os.path.join(_ROOT, "dna", "known_nodes.yaml")
)
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    """FastAPI 生命周期钩子，启动时激活网关功能"""
    init_immune_system()
    # 将 ZMQ 监听挂载到后台
    asyncio.create_task(gateway_node.listen())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                signal = json.loads(data)
                client_id = signal.get("client_id", "unknown_device")
                
                # 🛡️ 零信任准入检测 (调用异步方法)
                if not await check_and_log_device_async(client_id):
                    logger.warning(f"⛔️ [免疫拦截] 发现陌生设备试图接入: {client_id}")
                    await websocket.send_text(json.dumps({
                        "error": "Unauthorized", 
                        "message": f"设备 {client_id} 未授权，请在终端执行 'noa approve' 批准。"
                    }))
                    await websocket.close(code=4003)
                    return
                
                # 验证通过，转入内网突触
                logger.success(f"🔓 [准入放行] 合法设备: {client_id}")
                await gateway_node.fire_signal("stimulus.raw", signal)
                await websocket.send_text(json.dumps({
                    "status": "received", 
                    "message": "中枢已接管指令，还有什么可以帮您？", 
                    "trace_id": signal.get("trace_id")
                }))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid Format"}))
                
    except WebSocketDisconnect:
        pass

async def main():
    asyncio.create_task(gateway_node.listen())
    config = uvicorn.Config(app, host="0.0.0.0", port=22222, log_level="warning")
    await uvicorn.Server(config).serve()

if __name__ == "__main__": 
    asyncio.run(main())
