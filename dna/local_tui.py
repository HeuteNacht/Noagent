import asyncio
import websockets
import json
import uuid

# ⚠️ 在 iPhone 端运行时，将此处改为你主机的 Tailscale IP (例如: 100.x.x.x)
GATEWAY_URI = "ws://127.0.0.1:22222/ws"
CLIENT_ID = "ios_or_local_tui"

async def terminal_loop():
    print("⏳ 正在桥接至丘脑网关...")
    try:
        async with websockets.connect(GATEWAY_URI) as ws:
            print("✅ 内部直连身份验证通过。突触全开。\n")
            
            while True:
                cmd = input("\033[1;36mnoa@host:~$\033[0m ")
                if not cmd.strip(): continue
                if cmd.strip().lower() in ["exit", "quit", "再见"]: break
                    
                # 1. 组装输入刺激
                trace_id = f"tui_{uuid.uuid4().hex[:6]}"
                signal = {
                    "trace_id": trace_id,
                    "client_id": CLIENT_ID,
                    "content": cmd
                }
                
                # 2. 发送信号
                await ws.send(json.dumps(signal))
                
                # 3. 循环等待直到接收到最终的大模型回复
                try:
                    while True:
                        res_data = await asyncio.wait_for(ws.recv(), timeout=15.0) # Grok 思考可能需要时间，延长超时
                        res = json.loads(res_data)
                        
                        # 过滤掉系统内部的 ACK (确认收到) 消息，只截获真正的 reply
                        if "reply" in res:
                            reply = res.get("reply")
                            print(f"\033[1;33m🧠 [Grok 中枢]: {reply}\033[0m\n")
                            break # 获取到最终回复，跳出等待循环，准备下一次 input
                            
                except asyncio.TimeoutError:
                    print("\033[1;31m⚠️ 大模型认知超时，皮层未响应。\033[0m\n")

    except Exception as e:
        print(f"\033[1;31m❌ 神经链路断开: {str(e)}\033[0m")

if __name__ == "__main__":
    asyncio.run(terminal_loop())