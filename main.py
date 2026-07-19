#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/main.py
# ========================================================
#  1. 环境与路径锚定
# ========================================================
# 导入子进程控制、系统路径及时间阻塞模块
import subprocess, os, time
# 获取当前 main.py 所在的绝对目录，即项目根目录 ~/Noagent/
_ROOT = os.path.dirname(os.path.abspath(__file__))

# ========================================================
#  2. 脑区并发唤醒核心逻辑
# ========================================================
def start_brain_regions():
    # 🧠 硬编码定义需要激活的默认脑区核心集群
    regions = ["sensory_gateway", "frontal_lobe", "effector"]
    # 用于挂载和管理所有存活子进程对象的容器
    processes = []
    # 使用 ANSI 逃逸字符（\033[1;34m 为加粗蓝色）输出炫酷的初始化 UI
    print("\033[1;34m=============================================================\033[0m")
    print("⚡️ Noa ZMQ 分布式中枢起搏器点火...")
    print("\033[1;34m=============================================================\033[0m")
    
    for region in regions:
        # 动态拼接各脑区的物理入口路径，如 ~/Noagent/brain/sensory_gateway/main.py
        script = os.path.join(_ROOT, "brain", region, "main.py")
        # 防御性编程：确保该脑区的核心脚本确实存在，避免抛出底层找不到文件的异常
        if os.path.exists(script):
            # ⚡最核心行：使用 Popen 异步非阻塞地在操作系统中派生（Fork）一个独立子进程运行该脑区
            # 这使得各脑区拥有完全独立的 PID、独立的内存空间和独立的 Python 解释器
            p = subprocess.Popen(["python3", script])
            # 将脑区名称和进程句柄以元组形式存入列表，留待后续生命周期管理
            processes.append((region, p))
            print(f"🫀 [{region}] 脑区已分离唤醒 (PID: {p.pid})")
            # 🕰 建立生理节奏：强制暂停 0.5 秒。
            # 作用是防止瞬间拉起多个网关导致网络端口争抢，或 ZMQ 绑定时发生未定义冲突
            time.sleep(0.5)
        # ========================================================
        #  3. 生命周期监控与阻断（优雅停机）
        # ========================================================     
    print("\033[1;32m✅ 突触建立完毕。按 Ctrl+C 切断。\033[0m")
    try:
        # 守护性阻塞：主进程会在这里循环等待（wait）每一个子进程。
        # 只要子进程不退出，主进程就一直挂起，维持系统的整体存活状态
        for _, p in processes: p.wait()
    except KeyboardInterrupt:
        # 捕获用户在终端按下的 Ctrl+C（信号 SIGINT）
        print("\n💤 阻断各脑区供血...")
        for name, p in processes:
            # 🩺 向每个脑区子进程发送 SIGTERM 终止信号，通知它们释放 ZMQ 端口、保存免疫数据并优雅退出
            p.terminate()
            print(f"   ↳ {name} 脑区已关闭。")

if __name__ == "__main__":
    # 点火运行
    start_brain_regions()
