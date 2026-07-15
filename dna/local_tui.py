#!/usr/bin/env python3
import asyncio
import websockets
import json
import uuid
import sys

GATEWAY_URI = "ws://127.0.0.1:22222/ws"
CLIENT_ID = "host_local_tui"

async def terminal_loop():
    print("\033[1;32m==================================================\033[0m")
    print("\033[1;32m      🧬 NOA LOCAL SUPER TERMINAL (ZMQ)       \033[0m")
    print("\033[1;32m==================================================\033[0m\n")
    print("⏳ 正在桥接至本地丘脑网关...")
    
    try:
        async with websockets.connect(GATEWAY_URI) as ws:
            print("✅ 内部直连身份验证通过。突触全开。\n")
            
            while True:
                cmd = input("\033[1;36mnoa@host:~$\033[0m ")
                
                if cmd.strip().lower() in ["exit", "quit", "再见"]:
                    print("\033[1;31m🔌 正在切断突触连接...\033[0m")
                    break
                    
                if not cmd.strip(): continue
                    
                signal = {
                    "trace_id": f"loc_{uuid.uuid4().hex[:6]}",
                    "client_id": CLIENT_ID,
                    "content": cmd
                }
                
                await ws.send(json.dumps(signal))
                
                try:
                    res_data = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    res = json.loads(res_data)
                    reply = res.get("message", "信号已被本地中枢接收。")
                    print(f"\033[1;33m🧠 [Noa]: {reply}\033[0m\n")
                except asyncio.TimeoutError:
                    print("\033[1;31m⚠️ 响应超时。\033[0m\n")

    except ConnectionRefusedError:
        print("\033[1;31m❌ 连接被拒绝。请确认已执行 'noa start'。\033[0m")
    except Exception as e:
        print(f"\033[1;31m❌ 致命错误: {str(e)}\033[0m")

if __name__ == "__main__":
    try:
        asyncio.run(terminal_loop())
    except KeyboardInterrupt:
        print("\n\033[1;31m🛑 强制退出。\033[0m")
