#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ [重构成功] {path}")

# ==========================================
# 1. 统一脑区主网关 (WernickeArea - main.py)
# 架构与 frontal_lobe/main.py 100% 保持一致
# ==========================================
MAIN_PY = """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/brain/wernicke_area/main.py

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

class WernickeArea(NeuronNode):
    def __init__(self):
        super().__init__(
            local_config_path=os.path.join(_CURRENT_DIR, "synapse.yaml"),
            connectome_path=os.path.join(_ROOT_DIR, "dna", "known_nodes.yaml")
        )
        # 激活受体：同时监听外部传入的语音信号 与 脑区内部的接力信号
        self.register_receptor("stimulus.audio")
        self.register_receptor("wernicke.internal")
        
        self.active_cortex_areas = []
        self._neurogenesis()

    def _neurogenesis(self):
        \"\"\"🧬 神经发生：与前额叶完全对齐的双重基因图谱与物理扫描挂载\"\"\"
        config_path = os.path.join(_CURRENT_DIR, "cortex_config.yaml")
        cortex_map = {}
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
                    for area in config_data.get("functional_areas", []) or config_data.get("Functional_areas", []):
                        cortex_map[area.get("name").lower()] = area.get("enabled", False)
                logger.info(f"📄 已成功读取 wernicke_area 基因管控图谱 ({len(cortex_map)} 个配置)。")
            except Exception as e:
                logger.error(f"❌ 解析 config.yaml 失败 ({e})，将回退至纯自动发现模式。")
        else:
            logger.warning("⚠️ 缺失 cortex_config.yaml，系统将默认放行所有物理发现的皮层。")

        cortex_path = os.path.join(_CURRENT_DIR, "cortex")
        os.makedirs(cortex_path, exist_ok=True)
        
        logger.info("🧠 正在组装韦尼克听觉语言皮层...")
        
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
                logger.success(f"  ↳ [听觉皮层挂载成功]: {module_name}")
            except BaseException as e:
                logger.error(f"  ❌ 皮层挂载崩溃 [{module_name}]: {type(e).__name__} -> {e}")

    async def process_signal(self, topic: str, message: dict):
        \"\"\"
        网关调度总线：与前额叶完全一致的“询问-接管-发射”通用范式
        \"\"\"
        payload = message.get("payload", {})
        trace_id = message.get("trace_id", "unknown")
        client_id = payload.get("client_id", "unknown")

        # 构建统一的标准内部请求载荷
        internal_request = {
            "trace_id": trace_id,
            "client_id": client_id,
            "data_type": payload.get("data_type", "audio"),
            "content": payload.get("content", "")
        }

        # 沿着皮层链路寻找对应的功能区 (谁能处理谁接管)
        for area in self.active_cortex_areas:
            if await area.can_process(internal_request):
                plugin_name = getattr(area, "PLUGIN_NAME", area.__name__)
                logger.debug(f"  ↳ 信号已分配至: [{plugin_name}]")
                
                internal_response = await area.process(internal_request)
                
                if internal_response and internal_response.get("status") == "success":
                    outbound_topic = internal_response.get("target_topic")
                    outbound_payload = internal_response.get("payload")
                    
                    logger.info(f"⚡ 韦尼克皮层响应 -> 发射至频道: [{outbound_topic}]")
                    await self.fire_signal(outbound_topic, outbound_payload)
                return

        logger.warning("⚠️ 韦尼克区回路短路：所有听觉皮层均拒绝处理该指令。")

if __name__ == "__main__":
    WernickeArea().run()
"""

# ==========================================
# 2. 听觉皮层 A: Speech to IPA (声学提取)
# ==========================================
SPEECH_TO_IPA_PY = """
# -*- coding: utf-8 -*-
import asyncio
from loguru import logger

PLUGIN_NAME = "Auditory Cortex (Speech -> IPA)"
_model = None

def awaken(root_dir, current_dir):
    \"\"\"启动时将 Allosaurus 声学模型装载入内存\"\"\"
    global _model
    try:
        from allosaurus.app import read_recognizer
        logger.info(f"[{PLUGIN_NAME}] 正在装载 Allosaurus 语音识别内核...")
        _model = read_recognizer()
        logger.success(f"[{PLUGIN_NAME}] Allosaurus 模型装载完毕！")
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 依赖缺失或模型装载失败: {e}")

async def can_process(request: dict) -> bool:
    \"\"\"受体：专门接管音频数据\"\"\"
    return request.get("data_type") == "audio"

async def process(request: dict) -> dict:
    if not _model:
        logger.error(f"[{PLUGIN_NAME}] 模型未初始化，拒绝处理。")
        return {"status": "error"}

    audio_path = request.get("content")
    logger.info(f"[{PLUGIN_NAME}] 正在提取音频 IPA 音标特征: {audio_path}")
    
    try:
        # 🚨 必须放入 asyncio.to_thread 防止 CPU 密集的声学计算阻塞整个 ZMQ 异步主循环
        ipa_result = await asyncio.to_thread(_model.recognize, audio_path, 'eng', True)
        logger.info(f"[{PLUGIN_NAME}] 提取得 IPA 序列: [{ipa_result}]")
    except Exception as e:
        logger.error(f"[{PLUGIN_NAME}] 音频识别异常: {e}")
        return {"status": "error"}

    return {
        "status": "success",
        "target_topic": "wernicke.internal",  # 内部接力频道
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "data_type": "ipa",                # 状态机转为 ipa
            "content": ipa_result
        }
    }
"""

# ==========================================
# 3. 听觉皮层 B: IPA to Text (语义映射)
# ==========================================
IPA_TO_TEXT_PY = """
# -*- coding: utf-8 -*-
from loguru import logger

PLUGIN_NAME = "Semantic Cortex (IPA -> Text)"

def awaken(root_dir, current_dir):
    pass

async def can_process(request: dict) -> bool:
    \"\"\"受体：专门接管上一阶段产出的 IPA 音标序列\"\"\"
    return request.get("data_type") == "ipa"

async def process(request: dict) -> dict:
    ipa_text = request.get("content")
    logger.info(f"[{PLUGIN_NAME}] 正在将 IPA [{ipa_text}] 解码为自然语言文本...")
    
    # Mock 解码逻辑 (后续可接入 G2P/P2G 或小 LLM 矫正模型)
    decoded_text = f"Hello world (decoded from IPA: {ipa_text})"

    return {
        "status": "success",
        "target_topic": "stimulus.raw",  # 💡 跨脑区折跃：直接发射给前额叶!
        "payload": {
            "trace_id": request.get("trace_id"),
            "client_id": request.get("client_id"),
            "content": decoded_text      # 此时内容变回了普通文本
        }
    }
"""

# ==========================================
# 4. 基因配置与硬件突触
# ==========================================
CONFIG_YAML = """
functional_areas:
  - name: speech_to_ipa
    description: 声学音标提取皮层 (Allosaurus)
    enabled: true
  - name: ipa_to_text
    description: 音标语义转换皮层 (IPA -> Text)
    enabled: true
"""

SYNAPSE_YAML = """
identity: wernicke_area
bind_address: tcp://*:22004
"""

def main():
    target_dir = os.path.join(os.getcwd(), "brain", "wernicke_area")
    
    # 1. 物理绞杀旧脑区目录
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        print(f"🧹 已完全抹除旧有脑区: {target_dir}")
        
    # 2. 重新重建干净的微内核脑区
    create_file(os.path.join(target_dir, "main.py"), MAIN_PY)
    create_file(os.path.join(target_dir, "cortex_config.yaml"), CONFIG_YAML)
    create_file(os.path.join(target_dir, "synapse.yaml"), SYNAPSE_YAML)
    create_file(os.path.join(target_dir, "cortex", "__init__.py"), "")
    create_file(os.path.join(target_dir, "cortex", "speech_to_ipa.py"), SPEECH_TO_IPA_PY)
    create_file(os.path.join(target_dir, "cortex", "ipa_to_text.py"), IPA_TO_TEXT_PY)
    
    print("\n🎉 韦尼克脑区（Wernicke Area）已基于统一架构彻底重构完成！")

if __name__ == "__main__":
    main()
