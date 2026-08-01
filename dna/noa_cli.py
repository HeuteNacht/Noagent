#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import argparse
import yaml
import signal
import time

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)
PID_FILE = os.path.join(DNA_DIR, ".brain.pid")
LOG_FILE = os.path.join(DNA_DIR, "noa.log")
CURRENT_PYTHON = sys.executable

def stop_system():
    print("🔄 正在执行手术刀级别的全脑靶向阻断...")
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGKILL)
            print(f"💤 中枢督导树 (PID: {pid}) 已休眠。")
        except:
            print("⚠️ 主进程已游离，执行空锁回收。")
        finally:
            if os.path.exists(PID_FILE): os.remove(PID_FILE)
    
    if sys.platform == "win32":
        subprocess.run('wmic process where "name=\'python.exe\' and CommandLine like \'%Noagent/brain/%\'" call terminate', shell=True, capture_output=True)
    else:
        subprocess.run(["pkill", "-9", "-f", "Noagent/brain/"], capture_output=True)
    print("✅ 当前物理宿主机内存已纯净，游离皮层已被回收。")

def start_system():
    if os.path.exists(PID_FILE):
        print("⚠️ 基因锁存在，请先执行 `noa stop`。")
        return
    print("\033[1;34m=============================================================\033[0m")
    print("⚡️ Noa ZMQ 分布式全脑起搏器点火 (跨平台模式)...")
    print("\033[1;34m=============================================================\033[0m")
    
    main_script = os.path.join(WORKSPACE, "main.py")
    log_fd = open(LOG_FILE, "a", encoding="utf-8")
    win_env = os.environ.copy()
    win_env["PYTHONUTF8"] = "1"
    
    if sys.platform == "win32":
        p = subprocess.Popen([CURRENT_PYTHON, main_script], stdout=log_fd, stderr=log_fd, env=win_env, creationflags=0x00000008)
    else:
        p = subprocess.Popen([CURRENT_PYTHON, main_script], stdout=log_fd, stderr=log_fd, env=win_env, start_new_session=True)

    with open(PID_FILE, "w") as f:
        f.write(str(p.pid))
    time.sleep(1.5)
    print(f"✅ \033[1;32m神经中枢已在后台潜意识运行 (PID: {p.pid})！\033[0m")

def main():
    parser = argparse.ArgumentParser(description="🧠 Noa ZMQ Bionic AI System")
    parser.add_argument("action", choices=["start", "stop", "restart", "tui", "approve", "log", "install", "evolve", "add"])
    parser.add_argument("target", nargs="?", default=None)
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.action == "start": start_system()
    elif args.action == "stop": stop_system()
    elif args.action == "restart":
        print("🔄 正在执行全脑强制重启序列...")
        stop_system()
        time.sleep(1)
        start_system()
    elif args.action == "log":
        if sys.platform == "win32":
            subprocess.run(["powershell", "-Command", f"Get-Content '{LOG_FILE}' -Wait -Encoding utf8"])
        else:
            subprocess.run(["tail", "-f", LOG_FILE])
    # 🎯 新增 tui 分支：调用 local_tui.py
    elif args.action == "tui":
        tui_script = os.path.join(DNA_DIR, "local_tui.py")
        if os.path.exists(tui_script):
            subprocess.run([CURRENT_PYTHON, tui_script])
        else:
            print(f"⚠️ 未找到 TUI 脚本: {tui_script}")
    elif args.action == "add" and args.target == "cortex":
        subprocess.run([CURRENT_PYTHON, os.path.join(DNA_DIR, "cortex_manager.py")])

if __name__ == "__main__":
    main()
