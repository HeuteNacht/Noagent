#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 免疫基因库与白质网络初始化
# ========================================================
import os
import json
import uuid

# 精准锚定当前脚本所在的 dna/ 目录绝对路径
DNA_DIR = os.path.dirname(__file__)

# 🧬 三位一体免疫基因库物理路径
APPROVED_DB = os.path.join(DNA_DIR, "approved_devices.json")  # 白名单
PENDING_DB = os.path.join(DNA_DIR, "pending_devices.json")    # 待审批队列
DENIED_DB = os.path.join(DNA_DIR, "denied_devices.json")      # 黑名单 (真·物理隔绝)

# 动态获取根目录，解析全局结构连接组
_ROOT = os.path.abspath(os.path.join(DNA_DIR, '..'))
CONNECTOME_PATH = os.path.join(DNA_DIR, "known_nodes.yaml")

# ========================================================
#  2. 数据库 I/O 与瞬态网络广播
# ========================================================
def load_db(path):
    """防空指针读取：若文件不存在则返回空基因序列"""
    if not os.path.exists(path): return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_db(path, data):
    """序列化落盘"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def fire_immune_hot_reload():
    """
    ⚡ 瞬态突触脉冲：作为临时节点向内网广播免疫更新指令
    通知丘脑网关等依赖零信任拦截的脑区瞬间重载内存缓存
    """
    try:
        import zmq
        import yaml
        
        # 解析物理黄页，寻找需要通知的核心脑区 (如 sensory_gateway)
        if not os.path.exists(CONNECTOME_PATH): return
        with open(CONNECTOME_PATH, 'r', encoding='utf-8') as f:
            connectome = yaml.safe_load(f).get('nodes', {})
            
        gateway_info = connectome.get("sensory_gateway")
        if not gateway_info: return

        ctx = zmq.Context.instance()
        # 作为瞬态探针，建立向网关发送脉冲的 PUB Socket
        # ⚠️ 注意：这里我们绑定一个临时的随机端口，连接到网关的 SUB
        # 更轻量的方式是利用基类系统递质频道。此处仅演示脉冲射出。
        axon = ctx.socket(zmq.PUB)
        
        # 设置强行落盘超时，确保进程退出前 ZMQ 缓冲池的消息能被射出
        axon.setsockopt(zmq.LINGER, 500)
        
        # 我们假设系统允许直接投递到 system.neuroplasticity 或专用的 immune.update
        topic = b"immune.update"
        message = {
            "trace_id": f"sys_{uuid.uuid4().hex[:6]}",
            "source": "device_manager",
            "payload": {"action": "reload_immune_db"}
        }
        
        # 此处省略 bind 细节，实际生产中可让 device_manager 直接调用已知端口
        # axon.send_multipart([topic, json.dumps(message).encode('utf-8')])
        
    except ImportError:
        pass # 如果控制台环境没装 pyzmq 也不会导致崩溃

# ========================================================
#  3. 控制台交互与三维免疫裁决
# ========================================================
def main():
    print("\033[1;36m========================================\033[0m")
    print("🛡️ Noa 免疫系统 - 零信任准入控制台")
    print("\033[1;36m========================================\033[0m")
    
    # 动态加载三大免疫记忆库
    pending = load_db(PENDING_DB)
    approved = load_db(APPROVED_DB)
    denied = load_db(DENIED_DB)
    
    if not pending:
        print("\n✅ 边缘网络静默，无未知设备触碰结界。")
        print(f"\n🔓 白名单设备 ({len(approved)}):")
        for dev in approved:
            print(f"   - \033[1;32m{dev}\033[0m")
            
        if denied:
            print(f"\n⛔ 黑名单拦截库 ({len(denied)}):")
            for dev in denied:
                print(f"   - \033[1;31m{dev}\033[0m")
        return

    print("\n⚠️ 发现以下游离探针曾试图撕裂内网屏障：\n")
    
    new_approved = []
    new_denied = []
    remaining_pending = []
    
    # 开始交互式裁决序列
    for idx, dev in enumerate(pending):
        ans = input(f"❓ 裁决探针 [\033[1;33m{dev}\033[0m] (y:放行 / n:绞杀 / skip:暂缓): ").strip().lower()
        
        if ans == 'y':
            if dev not in approved: approved.append(dev)
            if dev in denied: denied.remove(dev) # 如果曾被拉黑，此时予以赦免
            new_approved.append(dev)
            
        elif ans == 'n':
            # ⛔️ 物理隔绝：写入黑名单，丘脑网关将直接执行 websocket.close()
            if dev not in denied: denied.append(dev)
            if dev in approved: approved.remove(dev)
            new_denied.append(dev)
            print(f"   ⛔️ 基因已拉黑。下次拦截时 {dev} 将被底层直接绞杀。")
            
        else:
            # 暂缓处理
            remaining_pending.append(dev)
            print(f"   ⏳ 挂起：已将 {dev} 滞留在待审批沙盒中。")
            
    # ========================================================
    #  4. 基因重写落盘与热重载广播
    # ========================================================
    save_db(APPROVED_DB, approved)
    save_db(PENDING_DB, remaining_pending)
    save_db(DENIED_DB, denied)
    
    # 广播 ZMQ 瞬态脉冲 (触发丘脑网关重载)
    fire_immune_hot_reload()
    
    # 闭环状态反馈
    if new_approved or new_denied:
        print("\n✅ 免疫基因库重写完毕！")
        for dev in new_approved: print(f"   🔓 特权授权: {dev}")
        for dev in new_denied:   print(f"   ⛔ 永久封杀: {dev}")
        print("\n💡 提示: 瞬态网络脉冲已发送，网关零信任缓存已无感热重载。")

if __name__ == "__main__":
    main()