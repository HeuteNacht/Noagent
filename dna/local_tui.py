#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 通信基因与静态声明
# ========================================================
import asyncio
import websockets
import json
import uuid
import sys

# ⚠️ 边缘网络寻址：若在 iPhone 端远程运行，改为 Tailscale 分配的主机 IP
GATEWAY_URI = "ws://127.0.0.1:22222/ws"
CLIENT_ID = "local_tui"

# ========================================================
#  2. 并发双线程：听觉皮层与表达中枢
# ========================================================
async def listen_loop(ws):
    """听觉并生线程：全时静默监控来自网关的异步推流"""
    try:
        while True:
            res_data = await ws.recv()
            res = json.loads(res_data)
            
            # 🛡️ 智能过滤器：只放行包含实质性 reply 的反馈或主动通知
            if "reply" in res:
                reply = res.get("reply")
                
                # 🎨 终端视觉防撕裂：
                # 收到后台消息时，先用 \r 回车并清空当前输入行 (\033[K)
                sys.stdout.write("\r\033[K") 
                # 打印中枢回复
                print(f"\033[1;33m🧠 [Grok 中枢]: {reply}\033[0m")
                # 重新画出输入提示符，让用户无缝继续打字
                sys.stdout.write("\033[1;36mnoa@host:~$\033[0m ")
                sys.stdout.flush()
                
    except websockets.exceptions.ConnectionClosed:
        # 这里不打印错误，交由外层统一处理断连，保持终端整洁
        pass
    except Exception as e:
        print(f"\n\033[1;31m❌ 监听流异常: {e}\033[0m")

async def input_loop(ws):
    """表达并生线程：劫持底层阻塞输入"""
    try:
        while True:
            # ⚡ 核心修复：用 to_thread 将同步的 input 扔进后台线程池，彻底解放主事件循环
            cmd = await asyncio.to_thread(input, "\033[1;36mnoa@host:~$\033[0m ")
            
            if not cmd.strip(): 
                continue
            if cmd.strip().lower() in ["exit", "quit", "再见"]:
                await ws.close()
                break

            # 组装输入刺激并打入 UUID
            trace_id = f"tui_{uuid.uuid4().hex[:6]}"
            signal = {
                "trace_id": trace_id,
                "client_id": CLIENT_ID,
                "content": cmd
            }
            
            # 瞬间将信号推入 WebSocket 管道，无需死等回复
            await ws.send(json.dumps(signal))
            
    except Exception as e:
        print(f"\n\033[1;31m❌ 表达突触断裂: {e}\033[0m")

# ========================================================
#  3. 突触建立与全双工生命维持
# ========================================================
async def terminal_loop():
    print("⏳ 正在桥接至丘脑网关...")
    try:
        async with websockets.connect(GATEWAY_URI) as ws:
            print("✅ 内部直连身份验证通过。突触全开。已进入全双工并发模式。\n")
            
            # ⚡ 架构跃迁：将“听”和“说”裂变为两个完全独立的并发任务
            listen_task = asyncio.create_task(listen_loop(ws))
            input_task = asyncio.create_task(input_loop(ws))
            
            # 只要其中任意一个任务（例如用户输入 exit 导致 input_task 结束）完成，就终止探针
            done, pending = await asyncio.wait(
                [listen_task, input_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # 优雅阻断：取消掉另一个还在挂起的任务
            for task in pending:
                task.cancel()
                
    except Exception as e:
        print(f"\033[1;31m❌ 神经链路无法建立或已断开: {str(e)}\033[0m")

if __name__ == "__main__":
    # 兼容性兜底：防止在某些 Windows 环境下 asyncio 抛出 EventLoop 退出异常
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(terminal_loop())
    except KeyboardInterrupt:
        print("\n\033[1;32m💤 探针已拔出。\033[0m")