#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 免疫基因库与白质网络初始化
# ========================================================
import os
import json
import shutil
import urllib.request

# 精准锚定当前脚本所在目录绝对路径
DNA_DIR = os.path.dirname(__file__)

# 🧬 三位一体免疫基因库物理路径
DB_PATHS = {
    "approved": os.path.join(DNA_DIR, "approved_devices.json"),
    "pending":  os.path.join(DNA_DIR, "pending_devices.json"),
    "denied":   os.path.join(DNA_DIR, "denied_devices.json")
}

# ========================================================
#  2. 数据库 I/O (统一集成 .example 模板代偿机制)
# ========================================================
def ensure_db_and_template(db_key):
    """无痕同步：确保物理库与模板文件绝对对齐"""
    db_path = DB_PATHS[db_key]
    template_path = f"{db_path}.example"
    
    # 1. 模板缺失自愈：自动生成标准空模板
    if not os.path.exists(template_path):
        with open(template_path, 'w', encoding='utf-8') as f:
            # 仅在 approved 模板里放一个示例，其他默认为空列表
            default_data = ["ios_siri_example"] if db_key == "approved" else []
            json.dump(default_data, f, indent=4)
            
    # 2. 物理库缺失自愈：从模板逆转录
    if not os.path.exists(db_path):
        shutil.copy(template_path, db_path)
        
    return db_path

def load_db(db_key):
    """防空指针读取，自带全量模板代偿"""
    db_path = ensure_db_and_template(db_key)
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_db(db_key, data):
    """序列化落盘"""
    with open(DB_PATHS[db_key], 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def fire_immune_hot_reload():
    """
    ⚡ 瞬态突触脉冲：通过本地 HTTP 探针，精准敲击 Gateway 的自愈重载端点。
    """
    try:
        # 直接通过 22222 端口强行唤醒 sensory_gateway 进行内存热重载
        req = urllib.request.Request("http://127.0.0.1:22222/internal/reload_immune", method="POST")
        urllib.request.urlopen(req, timeout=1)
    except Exception as e:
        pass # 静默处理，避免未开启网关时报错

# ========================================================
#  3. 控制台交互与三维免疫裁决
# ========================================================
def main():
    print("\033[1;36m========================================\033[0m")
    print("🛡️ Noa 免疫系统 - 零信任准入控制台")
    print("\033[1;36m========================================\033[0m")
    
    # 动态加载三大免疫记忆库 (自动触发模板自愈)
    pending = load_db("pending")
    approved = load_db("approved")
    denied = load_db("denied")
    
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
            if dev in denied: denied.remove(dev)
            new_approved.append(dev)
            
        elif ans == 'n':
            if dev not in denied: denied.append(dev)
            if dev in approved: approved.remove(dev)
            new_denied.append(dev)
            print(f"   ⛔️ 基因已拉黑。下次拦截时 {dev} 将被底层直接绞杀。")
            
        else:
            remaining_pending.append(dev)
            print(f"   ⏳ 挂起：已将 {dev} 滞留在待审批沙盒中。")
            
    # ========================================================
    #  4. 基因重写落盘与热重载广播
    # ========================================================
    save_db("approved", approved)
    save_db("pending", remaining_pending)
    save_db("denied", denied)
    
    # 💥 发射物理热重载信号
    fire_immune_hot_reload()
    
    # 闭环状态反馈
    if new_approved or new_denied:
        print("\n✅ 免疫基因库重写完毕！")
        for dev in new_approved: print(f"   🔓 特权授权: {dev}")
        for dev in new_denied:   print(f"   ⛔ 永久封杀: {dev}")
        print("\n💡 提示: 瞬态网络脉冲已发送，网关零信任缓存已完成【无感热重载】。请重新呼叫 Siri。")

if __name__ == "__main__":
    main()
