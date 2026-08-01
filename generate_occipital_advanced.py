#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

TARGET_DIR = os.path.join(os.getcwd(), "brain", "occipital_lobe")
CORTEX_DIR = os.path.join(TARGET_DIR, "cortex")

# ==========================================
# 1. 主节点 (main.py) - 对齐韦尼克区的神经发生机制
# ==========================================
MAIN_PY_CONTENT = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/brain/occipital_lobe/main.py

import os
import sys
import yaml
import pkgutil
import importlib
from loguru import logger

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(os.path.dirname(_CURRENT_DIR))

if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from white_matter.neuron_base import NeuronNode

class OccipitalLobe(NeuronNode):
    def __init__(self):
        super().__init__(
            local_config_path=os.path.join(_CURRENT_DIR, "synapse.yaml"),
            connectome_path=os.path.join(_ROOT_DIR, "dna", "known_nodes.yaml")
        )
        # 激活受体：监听外部传入的视觉信号 与 脑区内部的接力信号
        self.register_receptor("stimulus.visual")
        self.register_receptor("occipital.internal")
        
        self.active_cortex_areas = []
        self._neurogenesis()

    def _neurogenesis(self):
        \"\"\"🧬 神经发生：动态扫描并挂载视觉皮层功能区\"\"\"
        config_path = os.path.join(_CURRENT_DIR, "cortex_config.yaml")
        cortex_map = {}
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
                    for area in config_data.get("functional_areas", []):
                        cortex_map[area.get("name").lower()] = area.get("enabled", False)
                logger.info(f"📄 已成功读取 occipital_lobe 基因管控图谱 ({len(cortex_map)} 个配置)。")
            except Exception as e:
                logger.error(f"❌ 解析 config.yaml 失败 ({e})，将回退至纯自动发现模式。")
        else:
            logger.warning("⚠️ 缺失 cortex_config.yaml，系统将默认放行所有物理发现的皮层。")

        cortex_path = os.path.join(_CURRENT_DIR, "cortex")
        os.makedirs(cortex_path, exist_ok=True)
        
        logger.info("👁️ 正在组装枕叶视觉皮层...")
        
        for _, module_name, _ in pkgutil.iter_modules([cortex_path]):
            mod_name_lower = module_name.lower()
            
            if mod_name_lower in cortex_map and cortex_map[mod_name_lower] is False:
                logger.warning(f"  ⛔ [基因锁阻断] 皮层已被配置禁用: {module_name}")
                continue
                
            try:
                mod = importlib.import_module(f"cortex.{module_name}")
                if hasattr(mod, 'awaken'):
                    mod.awaken(_ROOT_DIR, _CURRENT_DIR)
                
                self.active_cortex_areas.append(mod)
                logger.success(f"  ↳ [视觉皮层挂载成功]: {module_name}")
            except BaseException as e:
                logger.error(f"  ❌ 皮层挂载崩溃 [{module_name}]: {type(e).__name__} -> {e}")

    async def process_signal(self, topic: str, message: dict):
        \"\"\"
        网关调度总线：支持多突触广播机制
        \"\"\"
        payload = message.get("payload", {})
        trace_id = message.get("trace_id", "unknown")
        client_id = payload.get("client_id", "unknown")

        internal_request = {
            "trace_id": trace_id,
            "client_id": client_id,
            "data_type": payload.get("data_type", "image"),
            "content": payload.get("content", payload.get("data", ""))
        }

        for area in self.active_cortex_areas:
            if await area.can_process(internal_request):
                plugin_name = getattr(area, "PLUGIN_NAME", area.__name__)
                
                internal_response = await area.process(internal_request)
                
                if internal_response and internal_response.get("status") == "success":
                    outbound_topics = internal_response.get("target_topics", [])
                    outbound_payload = internal_response.get("payload")
                    
                    for out_topic in outbound_topics:
                        logger.info(f"⚡ [{plugin_name}] 响应 -> 发射至频道: [{out_topic}]")
                        await self.fire_signal(out_topic, outbound_payload)
                return

        logger.warning("⚠️ 枕叶区回路短路：所有视觉皮层均拒绝处理该指令。")

if __name__ == "__main__":
    OccipitalLobe().run()
"""

# ==========================================
# 2. 突触与基因配置 (synapse.yaml & cortex_config.yaml)
# ==========================================
SYNAPSE_YAML_CONTENT = """identity: occipital_lobe
listen_to_nodes:
  - sensory_gateway
subscriptions:
  - "stimulus.visual"
  - "occipital.internal"
"""

CORTEX_CONFIG_YAML_CONTENT = """functional_areas:
  - name: image_to_text
    description: 视觉大模型理解皮层 (VLM)
    enabled: true
  - name: face_recognition
    description: 专有面部特征识别皮层 (预留拓展)
    enabled: false
"""

# ==========================================
# 3. 动态皮层功能区 (cortex/image_to_text.py)
# ==========================================
CORTEX_PLUGIN_CONTENT = """# -*- coding: utf-8 -*-
from loguru import logger

PLUGIN_NAME = "Visual Cortex (Image -> Text / VLM)"

def awaken(root_dir, current_dir):
    # 这里未来可以初始化你的 VLM (如 LLaVA, GPT-4o-vision)
    logger.info(f"[{PLUGIN_NAME}] 正在初始化视觉大模型权重...")
    pass

async def can_process(request: dict) -> bool:
    # 🎯 兼容 data_type、type
    dtype = request.get("data_type") or request.get("type")
    
    # 放行图像类型，或者含有内容载荷的请求
    return dtype in ["image", "image_chunk"] or bool(request.get("content"))

async def process(request: dict) -> dict:
    image_data = request.get("content")
    
    # ==========================================
    # 🧠 TODO: 接入真实模型进行图像分析
    # ==========================================
    logger.info(f"[{PLUGIN_NAME}] 正在通过大模型解析图像特征...")
    decoded_text = f"【枕叶视觉皮层解析完毕】: 成功提取图像内容并转化为文本理解。"

    return {
        "status": "success",
        # 💡 核心机制：双路发射预留
        # stimulus.response -> 发给 Sensory Gateway
        "target_topics": ["stimulus.response"],
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "data_type": "text", 
            "content": decoded_text
        }
    }
"""

def generate_brain_area():
    print(f"🧠 开始构建高阶脑区架构: {TARGET_DIR}")
    
    os.makedirs(CORTEX_DIR, exist_ok=True)
    
    files_to_create = {
        "main.py": MAIN_PY_CONTENT,
        "synapse.yaml": SYNAPSE_YAML_CONTENT,
        "cortex_config.yaml": CORTEX_CONFIG_YAML_CONTENT,
        "cortex/__init__.py": "",  # 设为包目录
        "cortex/image_to_text.py": CORTEX_PLUGIN_CONTENT
    }

    for filename, content in files_to_create.items():
        path = os.path.join(TARGET_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ [组件挂载] {filename} 生成完毕")

    print("\n🎉 枕叶视觉区 (Occipital Lobe) 高阶模块一键生成完毕！")
    print("✨ 已完美对齐韦尼克区的 Cortex 动态皮层加载机制与多总线发射功能。")

if __name__ == "__main__":
    generate_brain_area()