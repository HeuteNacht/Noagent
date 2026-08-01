#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# probe_grok_models.py

import os
import requests
from dotenv import load_dotenv

# 1. 加载环境变量
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

api_key = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")

if not api_key:
    print("❌ 错误：环境变量中未检测到 GROK_API_KEY 或 XAI_API_KEY！")
    exit(1)

print(f"🔑 正在使用 API Key: {api_key[:6]}...{api_key[-4:]} 探测 x.AI 矩阵...")

# 2. 发起请求
url = "https://api.x.ai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 挂载常见的代理环境变量（如果在服务器直连则自动 fallback）
proxies = None
env_proxy = os.environ.get("NOA_PROXY") or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
if env_proxy:
    proxies = {"http": env_proxy, "https": env_proxy}

try:
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    
    if response.status_code == 200:
        models_data = response.json().get("data", [])
        print("\n✅ API Key 验证成功！当前密钥可使用的完整模型列表：")
        print("-" * 50)
        
        vision_models = []
        for item in models_data:
            model_id = item.get("id")
            print(f"  • {model_id}")
            # 筛选包含 vision 关键字的模型
            if "vision" in model_id.lower():
                vision_models.append(model_id)
                
        print("-" * 50)
        if vision_models:
            print("👁️ [视觉模型推荐] 你的 API Key 支持以下视觉模型：")
            for vm in vision_models:
                print(f"  👉  {vm}")
            print(f"\n💡 建议在 image_to_text.py 中将 model 修改为: '{vision_models[0]}'")
        else:
            print("⚠️ 警告：当前 API Key 下未筛选出显式包含 'vision' 的模型，请确认账号是否拥有视觉模型特权。")

    elif response.status_code in [401, 403]:
        print(f"\n❌ API Key 无效或未授权！HTTP {response.status_code}")
        print(f"响应信息: {response.text}")
    else:
        print(f"\n⚠️ 请求失败，HTTP 状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

except Exception as e:
    print(f"\n💥 网络探测异常: {e}")