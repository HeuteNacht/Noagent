#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/dna/local_tui.py
# ========================================================
#  1. 通信基因与静态声明
# ========================================================
# 异步 IO 核心库
import asyncio
# 高性能客户端 WebSocket 通信库
import websockets
import json
import uuid

# ⚠️ 边缘网络寻址：在本地开发时走 127.0.0.1，若在 iPhone 端远程运行，
# 只需将此处改为你在 Tailscale 虚拟组网中分配给主机的 100.x.x.x 物理 IP 即可
GATEWAY_URI = "ws://127.0.0.1:22222/ws"
# 声明本探针的物理身份标识，用于网关免疫系统的白名单比对
CLIENT_ID = "local_tui"

# ========================================================
#  2. 突触建立与长连接循环
# ========================================================
async def terminal_loop():
    print("⏳ 正在桥接至丘脑网关...")
    try:
        # ⚡ 核心步骤：异步建立与 FastAPI 网关的 WebSocket 双向连接上下文
        async with websockets.connect(GATEWAY_URI) as ws:
            print("✅ 内部直连身份验证通过。突触全开。\n")
            
            while True:
                # 🎨 使用 ANSI 逃逸字符渲染出加粗青色的黑客风终端提示符（noa@host:~$）
                cmd = input("\033[1;36mnoa@host:~$\033[0m ")
                # 过滤空内容，防止向白质网络发送无意义垃圾刺激
                if not cmd.strip(): continue
                # 设定休眠与阻断边界，允许用户随时优雅切断探针
                if cmd.strip().lower() in ["exit", "quit", "再见"]: break

                # 1. 组装输入刺激
                # 局部突触发生：利用 UUID 为每一次敲击生成前缀为 tui_ 的 6 位唯一链路追踪码
                trace_id = f"tui_{uuid.uuid4().hex[:6]}"
                signal = {
                    "trace_id": trace_id,
                    "client_id": CLIENT_ID,
                    "content": cmd # 用户实际输入的文本动作
                }
                
                # 2. 发送信号
                # 将 Python 字典序列化为 JSON 字符串，通过物理网络管道推向丘脑网关
                await ws.send(json.dumps(signal))
                
                # ========================================================
                #  3. 认知状态流拦截（等待认知回传）
                # ========================================================
                # 3. 循环等待直到接收到最终的大模型回复
                try:
                    while True:
                        # 🕰 认知挂起防御：由于云端 Grok 4.5 包含深度思考（System 2 慢思考），
                        # 耗时较长，因此设置了 15.0 秒的高容忍度异步等待超时
                        res_data = await asyncio.wait_for(ws.recv(), timeout=15.0) # Grok 思考可能需要时间，延长超时
                        res = json.loads(res_data)
                        
                        # 🛡️ 递质流过滤器：网关收到消息时会瞬间返回一个 ACK（确认收到）消息
                        # 这里通过判断是否包含 "reply" 键，智能化过滤掉过路心跳与中间确认包，直奔主题
                        if "reply" in res:
                            reply = res.get("reply")
                            # 用加粗黄色高亮输出 Grok 中枢的最终认知决策
                            print(f"\033[1;33m🧠 [Grok 中枢]: {reply}\033[0m\n")
                            break # 获取到最终回复，跳出等待循环，准备下一次 input
                            
                except asyncio.TimeoutError:
                    # 云端网络断裂或大模型思考超时的防御提示
                    print("\033[1;31m⚠️ 大模型认知超时，皮层未响应。\033[0m\n")

    except Exception as e:
        # 网络未联通、Tailscale 断连或网关未被 `noa approve` 批准被免疫系统踢出时的异常捕获
        print(f"\033[1;31m❌ 神经链路断开: {str(e)}\033[0m")

if __name__ == "__main__":
    # 驱动探针生命维持
    asyncio.run(terminal_loop())