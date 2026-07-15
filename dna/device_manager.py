#!/usr/bin/env python3
import os, json

DNA_DIR = os.path.dirname(__file__)
APPROVED_DB = os.path.join(DNA_DIR, "approved_devices.json")
PENDING_DB = os.path.join(DNA_DIR, "pending_devices.json")

def load_db(path):
    if not os.path.exists(path): return []
    with open(path, 'r') as f: return json.load(f)

def save_db(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=4)

def main():
    print("\033[1;36m========================================\033[0m")
    print("🛡️ Noa 免疫系统 - 设备准入管理控制台")
    print("\033[1;36m========================================\033[0m")
    
    pending = load_db(PENDING_DB)
    approved = load_db(APPROVED_DB)
    
    if not pending:
        print("\n✅ 当前没有待审批的未知设备。")
        print(f"🔒 已授权设备库 ({len(approved)}):")
        for dev in approved:
            print(f"   - {dev}")
        return

    print("\n⚠️ 发现以下未授权设备曾试图接入网关：\n")
    
    new_approved = []
    remaining_pending = []
    
    for idx, dev in enumerate(pending):
        ans = input(f"❓ 是否批准设备 [\033[1;33m{dev}\033[0m] 接入? (y/n/skip): ").strip().lower()
        if ans == 'y':
            if dev not in approved: approved.append(dev)
            new_approved.append(dev)
        elif ans == 'n':
            print(f"   ⛔️ 已将 {dev} 永久拒之门外。")
        else:
            remaining_pending.append(dev)
            
    # 更新免疫库
    save_db(APPROVED_DB, approved)
    save_db(PENDING_DB, remaining_pending)
    
    if new_approved:
        print("\n✅ 批准完成！以下设备现已获得物理白名单特权：")
        for dev in new_approved: print(f"   🔓 {dev}")
        print("\n💡 提示: 无需重启网关，白名单已实时热重载。")

if __name__ == "__main__":
    main()
