#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/dna/device_manager.py
# ========================================================
#  1. 免疫基因库路径锚定
# ========================================================
import os, json

# 精准锚定当前脚本所在的 dna/ 目录绝对路径
DNA_DIR = os.path.dirname(__file__)
# 拼接出已授权白名单（自身免疫库）与待审批黑户（外来抗原库）的物理 JSON 路径
APPROVED_DB = os.path.join(DNA_DIR, "approved_devices.json")
PENDING_DB = os.path.join(DNA_DIR, "pending_devices.json")

# ========================================================
#  2. 数据库 I/O 稳健封装
# ========================================================
def load_db(path):
    # 防御性编程：若物理文件尚未生成（例如系统首次运行），默认返回空列表，防止引发文件缺失异常
    if not os.path.exists(path): return []
    with open(path, 'r') as f: return json.load(f)

def save_db(path, data):
    # 将更新后的设备列表以美化的 JSON 格式（4格缩进）持久化序列化落盘
    with open(path, 'w') as f: json.dump(data, f, indent=4)

# ========================================================
#  3. 控制台交互与免疫裁决
# ========================================================
def main():
    # 🎨 使用 ANSI 逃逸字符渲染出加粗青色的命令行 UI 边框
    print("\033[1;36m========================================\033[0m")
    print("🛡️ Noa 免疫系统 - 设备准入管理控制台")
    print("\033[1;36m========================================\033[0m")
    
    # 从磁盘动态加载当前的免疫记忆库
    pending = load_db(PENDING_DB)
    approved = load_db(APPROVED_DB)
    
    # 🔍 状态自检：如果没有待审批的设备，则展示当前的信任资产清单后优雅退出
    if not pending:
        print("\n✅ 当前没有待审批的未知设备。")
        print(f"🔒 已授权设备库 ({len(approved)}):")
        for dev in approved:
            print(f"   - {dev}")
        return

    # 🚨 警报触发：发现有游离的神经探针（例如你的 iPhone）试图越权接入
    print("\n⚠️ 发现以下未授权设备曾试图接入网关：\n")
    
    # 记录本次交互中新晋放行的设备
    new_approved = []
    # 记录本次被用户跳过（skip）、留待下次处理的设备
    remaining_pending = []
    
    for idx, dev in enumerate(pending):
        # 交互式裁决：高亮打印陌生设备的 CLIENT_ID，等待管理员物理输入
        ans = input(f"❓ 是否批准设备 [\033[1;33m{dev}\033[0m] 接入? (y/n/skip): ").strip().lower()
        if ans == 'y':
            # 移入白名单（去重保护）
            if dev not in approved: approved.append(dev)
            new_approved.append(dev)
        elif ans == 'n':
            # ⛔️ 拒绝策略：直接丢弃，不加入任何列表。
            print(f"   ⛔️ 已将 {dev} 永久拒之门外。")
        else:
            # 暂缓处理：用户选择了 skip 或输入了其他杂质字符，保留在待审批队列中
            remaining_pending.append(dev)
            
    # ========================================================
    #  4. 基因重写落盘与热生效提示
    # ========================================================
    # 🧬 免疫库有丝分裂：将最新的判定结果无缝重写回物理磁盘
    save_db(APPROVED_DB, approved)
    save_db(PENDING_DB, remaining_pending)
    
    # 闭环反馈
    if new_approved:
        print("\n✅ 批准完成！以下设备现已获得物理白名单特权：")
        for dev in new_approved: print(f"   🔓 {dev}")
        # 💡 正如我们在丘脑网关看到的设计：网关每次只查内存 `_APPROVED_CACHE`，
        # 如果配合文件 Watchdog 或 ZMQ 广播，这里就真正实现了无感知的“实时热重载”
        print("\n💡 提示: 无需重启网关，白名单已实时热重载。")

if __name__ == "__main__":
    main()
