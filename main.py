#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, os, time
_ROOT = os.path.dirname(os.path.abspath(__file__))

def start_brain_regions():
    regions = ["sensory_gateway", "frontal_lobe", "effector"]
    processes = []
    print("\033[1;34m=============================================================\033[0m")
    print("⚡️ Noa ZMQ 分布式中枢起搏器点火...")
    print("\033[1;34m=============================================================\033[0m")
    
    for region in regions:
        script = os.path.join(_ROOT, "brain", region, "main.py")
        if os.path.exists(script):
            p = subprocess.Popen(["python3", script])
            processes.append((region, p))
            print(f"🫀 [{region}] 脑区已分离唤醒 (PID: {p.pid})")
            time.sleep(0.5)
            
    print("\033[1;32m✅ 突触建立完毕。按 Ctrl+C 切断。\033[0m")
    try:
        for _, p in processes: p.wait()
    except KeyboardInterrupt:
        print("\n💤 阻断各脑区供血...")
        for name, p in processes:
            p.terminate()
            print(f"   ↳ {name} 脑区已关闭。")

if __name__ == "__main__":
    start_brain_regions()
