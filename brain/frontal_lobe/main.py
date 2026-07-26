#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/brain/frontal_lobe/main.py

import os
import sys
import yaml
import pkgutil
import importlib
from loguru import logger

# ========================================================
#  1. 环境初始化与路径挂载 (同时包含根目录与当前脑区目录)
# ========================================================
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(os.path.dirname(_CURRENT_DIR))

# 🎯 必须同时挂载当前脑区路径，否则 importlib 无法识别 cortex 包
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)


from white_matter.neuron_base import NeuronNode

class FrontalLobe(NeuronNode):
    def __init__(self):
        super().__init__(
            local_config_path=os.path.join(os.path.dirname(__file__), "synapse.yaml"),
            connectome_path=os.path.join(_ROOT_DIR, "dna", "known_nodes.yaml")
        )
        
        self.register_receptor("stimulus.raw")
        self.active_cortex_areas = []
        self._neurogenesis()  # 触发皮层发育与挂载

    def _neurogenesis(self):
        """🧬 双重保险神经发生：基于 YAML 基因图谱与动态物理目录扫描"""
        config_path = os.path.join(os.path.dirname(__file__), "cortex_config.yaml")
        cortex_map = {}
        
        # ==========================================
        #  防线 1：解析 YAML 基因图谱 (强制小写容错)
        # ==========================================
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
                    for area in config_data.get("functional_areas", []) or config_data.get("Functional_areas", []):
                        # 强转小写，防止 YAML 填写不规范
                        cortex_map[area.get("name").lower()] = area.get("enabled", False)
                logger.info(f"📄 已成功读取 cortex_config.yaml (读取到 {len(cortex_map)} 个基因锁配置)。")
            except Exception as e:
                logger.error(f"❌ 解析 config.yaml 失败 ({e})，将回退至纯自动发现模式。")
        else:
            logger.warning("⚠️ 缺失 cortex_config.yaml，系统将默认放行所有物理发现的脑区。")

        # ==========================================
        #  防线 2：物理扫描与双重校验挂载
        # ==========================================
        cortex_path = os.path.join(os.path.dirname(__file__), "cortex")
        if not os.path.exists(cortex_path):
            os.makedirs(cortex_path, exist_ok=True)
            
        logger.info(f"🧠 正在扫描并重组前额叶皮层拓扑 (扫描路径: {cortex_path}) ...")
        
        found_any = False
        # 遍历 cortex 目录下的所有 .py 模块
        for _, module_name, _ in pkgutil.iter_modules([cortex_path]):
            found_any = True
            mod_name_lower = module_name.lower()
            
            # ⭐️ 双重保险阻断：图谱中明确标记为 false 的脑区，直接物理绞杀！
            if mod_name_lower in cortex_map and cortex_map[mod_name_lower] is False:
                logger.warning(f"  ⛔ [基因锁阻断] 脑区已被配置禁用，跳过挂载: {module_name}")
                continue
                
            try:
                # 动态导入模块
                mod = importlib.import_module(f"cortex.{module_name}")
                
                # 触发子程序的唤醒钩子
                if hasattr(mod, 'awaken'):
                    mod.awaken(_ROOT_DIR, os.path.dirname(__file__))
                
                self.active_cortex_areas.append(mod)
                
                if mod_name_lower in cortex_map:
                    logger.success(f"  ↳ [图谱授权] 成功挂载脑区: {module_name}")
                else:
                    logger.success(f"  ↳ [野生突变] 自动发现并激活未注册脑区: {module_name}")
                    
            except BaseException as e:  # 🚨 升级为 BaseException 拦截一切语法/导入级崩溃！
                logger.error(f"  ❌ 脑区挂载崩溃 [{module_name}]: {type(e).__name__} -> {e}")

        if not found_any:
            logger.warning("⚠️ cortex 目录下没有扫描到任何有效的 .py 文件！请确保该目录下包含 '__init__.py' 且有代码文件。")

    async def process_signal(self, topic: str, message: dict):
        """
        网关调度总线：遍历所有激活的脑区，由脑区自行决定是否处理。
        接收到脑区返回的标准 API 字典后，向外发射 ZMQ 信号。
        """
        payload = message.get("payload", {})
        trace_id = message.get("trace_id", "unknown")
        client_id = payload.get("client_id", "unknown")
        content = payload.get("content", "").strip()

        if not content: return
        
        # 🚨 终极探针加入：这行代码会原形毕露地打印出 Siri 到底传了什么怪东西！
        logger.info(f"⚡ 刺激截获 (Trace: {trace_id} | Client: {client_id}) 载荷分析: [{content}]")

        # 构建给子程序分析的标准输入载荷
        internal_request = {
            "trace_id": trace_id,
            "client_id": client_id,
            "content": content
        }

        # 沿着皮层链路寻找对应的功能区 (先入为主，找到即中止)
        for area in self.active_cortex_areas:
            # 1. 询问该皮层是否接管此信号
            if await area.can_process(internal_request):
                # 获取子程序自定义的插件名称，如果没定义则用模块名
                plugin_name = getattr(area, "PLUGIN_NAME", area.__name__)
                logger.debug(f"  ↳ 信号已分配至: [{plugin_name}]")
                
                # 2. 执行逻辑并获取标准内部 API 响应
                internal_response = await area.process(internal_request)
                
                # 3. 额叶网关执行 ZMQ 跨节点通信交互
                if internal_response and internal_response.get("status") == "success":
                    outbound_topic = internal_response.get("target_topic", "stimulus.response")
                    await self.fire_signal(outbound_topic, internal_response.get("payload"))
                return

        # 若无任何脑区接管
        logger.warning("⚠️ 神经回路短路：所有脑区均拒绝处理该指令。")
        await self.fire_signal("stimulus.response", {
            "trace_id": trace_id,
            "client_id": client_id,
            "reply": "⚠️ 额叶皮层受损或功能缺失：无法处理该指令。"
        })

if __name__ == "__main__":
    FrontalLobe().run()
