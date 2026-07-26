#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境锚定与跨平台依赖
# ========================================================
import os
import sys
import subprocess
import argparse
import yaml
import signal
import time

# 精准锚定物理坐标
DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)

# 🧬 【双轨制核心对齐】：与 noa_cli.sh 共享完全相同的物理锁与日志路径
PID_FILE = os.path.join(DNA_DIR, ".brain.pid")
LOG_FILE = os.path.join(DNA_DIR, "noa.log")

# 动态继承当前的 Python 解释器 (完美兼容 Conda/Miniconda 隔离环境)
CURRENT_PYTHON = sys.executable

# ========================================================
#  2. 靶向阻断引擎 (Targeted PID Eradication)
# ========================================================
def stop_system():
    print("🔄 正在执行手术刀级别的靶向阻断...")
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
                
            # 跨平台进程肢解
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
                
            print(f"💤 物理链路切断，中枢督导树 (PID: {pid}) 已被安全休眠。")
        except (ProcessLookupError, ValueError):
            print("⚠️ 进程已游离，执行空锁回收。")
        except PermissionError:
            print(f"❌ 权限不足，无法终止 PID {pid}。")
        finally:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
    else:
        print("✅ 当前物理宿主机内未发现活跃的 Noa 中枢。")

# ========================================================
#  3. 异构计算集群唤醒 (Distributed SSH Ignition)
# ========================================================
def ignite_remote_nodes():
    """读取全局静态连接组，探测并唤醒远程异地脑区"""
    connectome_path = os.path.join(DNA_DIR, "known_nodes.yaml")
    if not os.path.exists(connectome_path): return
    
    try:
        with open(connectome_path, 'r', encoding='utf-8') as f:
            connectome = yaml.safe_load(f).get('nodes', {})
            
        remote_hosts = set()
        for identity, config in connectome.items():
            host = config.get('host', '127.0.0.1')
            if host not in ['127.0.0.1', 'localhost', '0.0.0.0']:
                remote_hosts.add(host)
                
        for host in remote_hosts:
            print(f"🚀 [分布式唤醒] 正在通过突触链路 (SSH) 点火异地脑区: {host}...")
            subprocess.Popen(
                ["ssh", host, "bash -ic 'noa start'"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception as e:
        print(f"⚠️ 远程集群探测异常: {e}")

# ========================================================
#  4. 中枢主起搏器 (Daemon Launcher)
# ========================================================
def start_system():
    if os.path.exists(PID_FILE):
        print("⚠️ 基因锁 .brain.pid 存在，系统似乎已经在后台运行！")
        print("💡 若属于僵尸锁，请先执行 `noa stop` 进行靶向清理。")
        return

    print("\033[1;34m=============================================================\033[0m")
    print("⚡️ Noa ZMQ 分布式中枢起搏器点火 (Windows 模式)...")
    print("\033[1;34m=============================================================\033[0m")

    # 1. 发射集群唤醒信号
    ignite_remote_nodes()

    # 2. 拉起本地主进程
    main_script = os.path.join(WORKSPACE, "main.py")
    log_fd = open(LOG_FILE, "a", encoding="utf-8")
    
    # 🎯 【核心修复】：强行克隆当前环境，并注入全局 UTF-8 运行时控制变量
    # 这将强制所有后台派生的 Python 子脑区原生输出 UTF-8 字节，彻底杜绝 GBK 乱码
    win_env = os.environ.copy()
    win_env["PYTHONUTF8"] = "1"
    
    # 跨平台的守护进程脱壳技术
    if sys.platform == "win32":
        # Windows API: DETACHED_PROCESS (0x00000008)，使进程彻底脱离当前 VSCodium 控制台后台运行
        p = subprocess.Popen([CURRENT_PYTHON, main_script], stdout=log_fd, stderr=log_fd, creationflags=0x00000008)
    else:
        p = subprocess.Popen([CURRENT_PYTHON, main_script], stdout=log_fd, stderr=log_fd, start_new_session=True)

    # 刻录物理基因锁
    with open(PID_FILE, "w") as f:
        f.write(str(p.pid))

    time.sleep(1.5)
    print(f"✅ \033[1;32m本地神经中枢已在后台潜意识运行 (PID: {p.pid})！终端已释放。\033[0m")

# ========================================================
#  5. 多路意图分发与 CLI 路由
# ========================================================
def main():
    parser = argparse.ArgumentParser(description="🧠 Noa ZMQ Bionic AI System")
    
    # 1. 扩充核心控制指令，加入 "add"
    parser.add_argument(
        "action", 
        choices=["start", "stop", "tui", "approve", "log", "install", "evolve", "add"], 
        help="系统核心控制指令"
    )
    
    # 2. 注入可选目标参数 (使用 nargs="?"，使其在输入如 noa start 时不报错)
    parser.add_argument(
        "target", 
        nargs="?", 
        default=None, 
        help="附加执行目标 (如: cortex)"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # ---------------- 路由分发 ----------------
    if args.action == "start":
        start_system()
        
    elif args.action == "stop":
        stop_system()
        
    elif args.action == "tui":
        subprocess.run([CURRENT_PYTHON, os.path.join(DNA_DIR, "local_tui.py")])
        
    elif args.action == "approve":
        subprocess.run([CURRENT_PYTHON, os.path.join(DNA_DIR, "device_manager.py")])
        
    elif args.action == "log":
        # 跨平台的日志流式挂载
        if sys.platform == "win32":
            # 🎯 核心修复：显式指定用 utf8 解码日志，彻底消除控制台乱码
            subprocess.run(["powershell", "-Command", f"Get-Content '{LOG_FILE}' -Wait -Encoding utf8"])
        else:
            subprocess.run(["tail", "-f", LOG_FILE])
            
    elif args.action in ["install", "evolve"]:
        subprocess.run([CURRENT_PYTHON, os.path.join(DNA_DIR, "sync_receptors.py")])
        
    # 🎯 新增的基因图谱管理路由
    elif args.action == "add":
        if args.target == "cortex":
            subprocess.run([CURRENT_PYTHON, os.path.join(DNA_DIR, "cortex_manager.py")])
        else:
            print("⚠️ 基因指令错误。预期用法: `noa add cortex`")

if __name__ == "__main__":
    main()
