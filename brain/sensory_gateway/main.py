#!/usr/bin/env python3
import os, sys, asyncio, json
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from white_matter.neuron_base import NeuronNode
from loguru import logger

# 准入数据库路径
APPROVED_DB = os.path.join(_ROOT, "dna", "approved_devices.json")
PENDING_DB = os.path.join(_ROOT, "dna", "pending_devices.json")

def load_db(path):
    if not os.path.exists(path): return []
    with open(path, 'r') as f: return json.load(f)

def save_db(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=4)

def check_and_log_device(client_id):
    approved = load_db(APPROVED_DB)
    if client_id in approved:
        return True
    
    # 未经批准，写入待审批池
    pending = load_db(PENDING_DB)
    if client_id not in pending:
        pending.append(client_id)
        save_db(PENDING_DB, pending)
    return False

class SensoryGateway(NeuronNode):
    async def process_signal(self, topic: str, message: dict): pass

gateway_node = SensoryGateway(
    os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
    os.path.join(_ROOT, "dna", "known_nodes.yaml")
)
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                signal = json.loads(data)
                client_id = signal.get("client_id", "unknown_device")
                
                # 🛡️ 零信任准入检测
                if not check_and_log_device(client_id):
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
