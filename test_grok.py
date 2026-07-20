#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv

# 加载基因锁
_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_ROOT, '.env'))
API_KEY = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")

print("=============================================================")
print("🧬 Noa Grok 认知构建与路由自检引擎启动...")
print("=============================================================")
print(f"🔑 密钥嗅探结果: {'已加载 (尾号:' + API_KEY[-6:] + ')' if API_KEY else '❌ 未注入 (请检查.env)'}")

async def diagnostic_run():
    # 🎯 1. 严格对照 xAI 官方标准锻造 Grok Build Payload
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "grok-latest", # 确保模型标识符在 2026 链路下无误
        "messages": [
            {"role": "user", "content": "ping"}
        ],
        "temperature": 0.1
    }

    # 编排测试路线
    strategies = [
        ("X-ray Socks5", "socks5://127.0.0.1:10808"),
        ("X-ray HTTP", "http://127.0.0.1:10809"),
        ("Direct Mode", None)
    ]

    for name, proxy_url in strategies:
        print(f"\n🚀 正在测试路由链路: [{name}] (目标: {proxy_url if proxy_url else '直连'})...")
        try:
            if proxy_url and "socks" in proxy_url.lower():
                from aiohttp_socks import ProxyConnector
                connector = ProxyConnector.from_url(proxy_url)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.post(url, headers=headers, json=data, timeout=8.0) as resp:
                        print(f"  ↳ 📥 物理响应状态码: HTTP {resp.status}")
                        res_text = await resp.text()
                        if resp.status == 200:
                            print(f"  🎉 [折跃成功] Grok 回应: {(await resp.json())['choices'][0]['message']['content']}")
                            return
                        else:
                            print(f"  ❌ [认知阻断] 服务器拒绝访问。详情: {res_text}")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data, proxy=proxy_url, timeout=8.0) as resp:
                        print(f"  ↳ 📥 物理响应状态码: HTTP {resp.status}")
                        res_text = await resp.text()
                        if resp.status == 200:
                            print(f"  🎉 [折跃成功] Grok 回应: {(await resp.json())['choices'][0]['message']['content']}")
                            return
                        else:
                            print(f"  ❌ [认知阻断] 服务器拒绝访问。详情: {res_text}")
        except Exception as e:
            print(f"  💥 [物理断裂] 抛出异常: {type(e).__name__} -> {e}")

    print("\n🚨 熔断警报：所有已知路由策略均无法触达大模型皮层。")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ 必须在 .env 中填入有效的 GROK_API_KEY 才能启动测试。")
        sys.exit(1)
    asyncio.run(diagnostic_run())
