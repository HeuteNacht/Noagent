#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境与路径锚定
# ========================================================
import subprocess
import os
import sys
import time
import threading

_ROOT = os.path.dirname(os.path.abspath(__file__))
# 将统一日志重定向到 DNA 序列文件夹中
LOG_FILE = os.path.join(_ROOT, "dna", "noa.log")

# ⚡ 跨平台动态捕捉当前的 Python 解释器环境 (完美兼容 Conda/Windows/Debian)
CURRENT_PYTHON = sys.executable

# ========================================================
#  2. 细胞器：日志总线与动态扫描
# ========================================================
def stream_logger(region_name: str, pipe):
    """
    独立抽离的脑区日志记录线程，将 stdout 流式写入统一日志文件，避免终端脏乱
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for line in iter(pipe.readline, b''):
            decoded_line = line.decode('utf-8', errors='replace')
            # 附带脑区名称前缀，方便使用 grep 进行快速过滤
            f.write(f"[{region_name}] {decoded_line}")
            f.flush()

def discover_brain_regions() -> list:
    """
    动态无监督有丝分裂：自动扫描 ~/Noagent/brain/ 目录下的可用脑区
    """
    brain_dir = os.path.join(_ROOT, "brain")
    regions = []
    if os.path.exists(brain_dir):
        for item in os.listdir(brain_dir):
            script_path = os.path.join(brain_dir, item, "main.py")
            # 只要该文件夹下存在 main.py，即视为合法可唤醒的脑区
            if os.path.isdir(os.path.join(brain_dir, item)) and os.path.exists(script_path):
                regions.append(item)
    return regions

# ========================================================
#  3. 脑干督导树核心逻辑 (Supervisor Tree)
# ========================================================
def start_brain_regions():
    regions = discover_brain_regions()
    processes = {}       # 存放 {region_name: Popen_object}
    log_threads = {}     # 存放 {region_name: Thread_object}

    print("\033[1;34m=============================================================\033[0m")
    print(f"⚡️ Noa ZMQ 分布式督导起搏器点火 (动态发现 {len(regions)} 个脑区)...")
    print("\033[1;34m=============================================================\033[0m")
    
    # 初始化/覆盖上一轮的陈旧日志
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== Noa 神经中枢启动日志 ===\n")

    def launch_region(region):
        """闭包函数：负责（重新）拉起指定脑区进程及挂载日志监听"""
        script = os.path.join(_ROOT, "brain", region, "main.py")
        
        # 建立隔离进程，并捕获标准输出和错误输出
        p = subprocess.Popen(
            [CURRENT_PYTHON, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        processes[region] = p
        
        # 挂载伴生线程，专职处理该进程的日志排放 (Daemon=True 保证随主进程关闭)
        t = threading.Thread(target=stream_logger, args=(region, p.stdout), daemon=True)
        t.start()
        log_threads[region] = t
        print(f"🫀 [{region}] 脑区已激活 (PID: {p.pid})")

    # 初次唤醒所有动态发现的脑区
    for region in regions:
        launch_region(region)
        time.sleep(0.5) # 防止端口瞬间争抢
        
    print("\033[1;32m✅ 神经网络构建完毕，督导看门狗 (Watchdog) 已挂载。\033[0m")
    print("📜 请打开新终端执行 `noa log` 监控分离后的流式脑电波日志。")
    print("💤 按 Ctrl+C 切断所有突触。")

    try:
        # 🔄 督导轮询循环 (取代原本的阻塞 wait)
        while True:
            time.sleep(2.0) # 心跳频率：2秒检测一次全盘健康状况
            for region in list(processes.keys()):
                p = processes[region]
                # poll() 如果返回 None 说明进程还活着，否则返回了退出状态码
                if p.poll() is not None:
                    exit_code = p.returncode
                    print(f"\033[1;31m⚠️ 警告: [{region}] 脑区因异常脱落 (Exit Code: {exit_code})，正在进行细胞重组...\033[0m")
                    launch_region(region) # 触发自愈机制
                    
    except KeyboardInterrupt:
        # 优雅停机协议
        print("\n💤 阻断各脑区供血...")
        for region, p in processes.items():
            if p.poll() is None: # 只杀死还在运行的进程
                p.terminate()
                print(f"   ↳ {region} 脑区已安全进入休眠。")

if __name__ == "__main__":
    start_brain_regions()