#!/usr/bin/env python3
#Noagent/brain/sensory_gateway/main.py
# ========================================================
#  1. 环境初始化与依赖导入
# ========================================================
import os, sys, asyncio, json
# 计算项目根目录（例如目前是：~/Noagent/），动态将父级的父级目录加入 sys.path，确保能正确导入 white_matter 核心库
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)

# 引入高性能异步 Web 框架及 WebSocket 组件
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# ASGI 服务器，用于启动 FastAPI
import uvicorn
# 引入 Noa 的神经元基类（封装了 ZMQ 核心逻辑）
from white_matter.neuron_base import NeuronNode
# 现代化的日志记录器
from loguru import logger
# ========================================================
#  2. 免疫系统（零信任准入）物理数据库与缓存定义
# ========================================================
# 定义已授权设备和待审批设备的物理 JSON 文件路径（相当于系统的免疫基因库）
APPROVED_DB = os.path.join(_ROOT, "dna", "approved_devices.json")
PENDING_DB = os.path.join(_ROOT, "dna", "pending_devices.json")

# 免疫记忆缓存（内存态）：使用 set 集合实现 O(1) 复杂度的闪电级查杀与校验
_APPROVED_CACHE = set()
_PENDING_CACHE = set()

# ========================================================
#  3.免疫机制核心函数
# ========================================================
def init_immune_system():
    """网关启动时将 DNA (JSON) 加载到内存"""
    global _APPROVED_CACHE, _PENDING_CACHE
    # 如果存在已授权的设备文件，将其反序列化并载入内存缓存
    if os.path.exists(APPROVED_DB):
        with open(APPROVED_DB, 'r') as f:
            _APPROVED_CACHE = set(json.load(f))
    # 如果存在待审批的设备文件，同样载入内存缓存
    if os.path.exists(PENDING_DB):
        with open(PENDING_DB, 'r') as f:
            _PENDING_CACHE = set(json.load(f))
    logger.info(f"🛡️ 免疫系统初始化: {_APPROVED_CACHE}")

def sync_pending_to_disk():
    """将待审批设备写回磁盘（后台执行）"""
    # 将当前的待审批内存集合持久化写入 JSON 文件，供 `noa approve` 指令读取
    with open(PENDING_DB, 'w') as f:
        json.dump(list(_PENDING_CACHE), f, indent=4)

async def check_and_log_device_async(client_id: str) -> bool:
    """
    异步非阻塞的零信任检测
    """
    # 1. 内存级闪电校验：如果设备在白名单中，直接放行，完全不产生文件 IO 阻塞
    if client_id in _APPROVED_CACHE:
        return True
    
    # 2. 如果是新来的陌生设备，且不在待审批队列中，则将其捕获
    if client_id not in _PENDING_CACHE:
        _PENDING_CACHE.add(client_id)
        # ⚡关键优化：将阻塞的磁盘 I/O 操作推入线程池（to_thread），防止阻塞 FastAPI 的异步事件循环
        await asyncio.to_thread(sync_pending_to_disk)
    # 未授权设备一律返回 False    
    return False

# ========================================================
#  4.仿生神经元节点的构建
# ========================================================
class SensoryGateway(NeuronNode):
    # 继承自神经元基类。由于丘脑网关在该设计中属于“纯输入端”，它不需要处理内网发给它的 ZMQ 信号
    # 因此将其收到内部信号的响应函数 `process_signal` 设为 pass 空实现
    async def process_signal(self, topic: str, message: dict): pass

# 实例化丘脑网关节点，传入自身的局部突触配置和全局物理黄页（known_nodes.yaml）
gateway_node = SensoryGateway(
    os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
    os.path.join(_ROOT, "dna", "known_nodes.yaml")
)
# 初始化 FastAPI 实例
app = FastAPI()

# ========================================================
#  5. 生命周期钩子与 WebSocket 核心交互逻辑
# ========================================================
@app.on_event("startup")
async def on_startup():
    """FastAPI 生命周期钩子，启动时激活网关功能"""
    # (1). 优先初始化免疫屏障
    init_immune_system()
    # (2). 将 ZMQ 的底层监听逻辑挂载到 asyncio 后台任务中，使其并发运行而不阻塞 Web 服务
    asyncio.create_task(gateway_node.listen())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 握手建立连接
    await websocket.accept()
    try:
        while True:
            # 持续接收游离探针（如 iOS）发来的指令字符串
            data = await websocket.receive_text()
            try:
                # 解析为字典对象
                signal = json.loads(data)
                # 提取设备唯一识别码
                client_id = signal.get("client_id", "unknown_device")
                
                # 🛡️ 零信任准入检测 (调用异步方法)
                if not await check_and_log_device_async(client_id):
                    logger.warning(f"⛔️ [免疫拦截] 发现陌生设备试图接入: {client_id}")
                    # 向客户端发送未授权警告，并指导其如何在主机端通过 CLI 审批
                    await websocket.send_text(json.dumps({
                        "error": "Unauthorized", 
                        "message": f"设备 {client_id} 未授权，请在终端执行 'noa approve' 批准。"
                    }))
                    # 异常关闭连接，状态码 4003
                    await websocket.close(code=4003)
                    return
                
                # 验证通过，转入内网突触
                logger.success(f"🔓 [准入放行] 合法设备: {client_id}")
                # 🧠 动作电位传导：将外部刺激转化为内部递质，通过 ZMQ 发布到 "stimulus.raw" 频道
                # 此时前额叶（frontal_lobe）等订阅了该频道的脑区将瞬间收到并开始解析意图
                await gateway_node.fire_signal("stimulus.raw", signal)
                # 瞬间向探针返回即时收到的回执，保证交互的丝滑感（心跳与静默握手检测的一部分）
                await websocket.send_text(json.dumps({
                    "status": "received", 
                    "message": "中枢已接管指令，还有什么可以帮您？", 
                    "trace_id": signal.get("trace_id")
                }))
                
            except json.JSONDecodeError:
                # 畸形数据过滤，保障内部网络不被脏数据污染
                await websocket.send_text(json.dumps({"error": "Invalid Format"}))
                
    except WebSocketDisconnect:
        # 捕获客户端断开连接（如 iPhone 走出 Tailscale 局域网或锁屏导致的偶发断连）
        pass

# ========================================================
#  6. 系统入口点
# ========================================================
async def main():
    # 安全起见，再次确保 ZMQ 监听已挂载
    asyncio.create_task(gateway_node.listen())
    # 绑定 0.0.0.0 端口 22222，以便物理局域网或 Tailscale 虚拟网卡内的远程设备能够路由进来
    config = uvicorn.Config(app, host="0.0.0.0", port=22222, log_level="warning")
    await uvicorn.Server(config).serve()

if __name__ == "__main__": 
    # 驱动异步事件循环
    asyncio.run(main())
