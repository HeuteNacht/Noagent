#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/brain/effector/main.py
# ========================================================
#  1. 运动皮层类声明与信号路由拦截
# ========================================================
# 🧬 导入 PyYAML 库，用于解析和序列化大脑的突触配置文件
import yaml

class Effector(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        # 拦截内部白质网络广播的 "action.execute"（执行物理动作）主题信号
        if topic == "action.execute":
            payload = message.get("payload", {})
            # 提取核心执行动词
            cmd = payload.get("command")
            
            # ========================================================
            # 🧬 核心特征：物理神经可塑性改写网络拓扑
            # ========================================================
            if cmd == "rewire_yaml":
                # 目标重连脑区（如 sensory_gateway）
                target_node = payload.get("target_node")
                # 该脑区需要追加订阅的全新 ZMQ 频道
                topic_to_add = payload.get("topic_to_add")
                logger.warning(f"🧬 激活神经可塑性: 正在重连 [{target_node}] 的突触...")
                
                # ========================================================
                #  2. 突触基因文件的定位与安全读取
                # ========================================================
                # 动态定位目标脑区的物理配置文件路径，例如：~/Noagent/brain/sensory_gateway/synapse.yaml
                yaml_path = os.path.join(_ROOT, "brain", target_node, "synapse.yaml")
                
                # 防御性边界检查：如果前额叶大模型幻觉了一个不存在的脑区，及时拦截，防止产生物理文件写入崩溃
                if not os.path.exists(yaml_path):
                    logger.error(f"❌ 找不到节点 {target_node} 的突触配置文件。")
                    return
                
                # 以 UTF-8 编码读取目标突触配置文件的磁盘数据
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    # 反序列化为 Python 字典
                    config = yaml.safe_load(f)
                
                # ========================================================
                #  3. 幂等性改写与有丝分裂落盘
                # ========================================================
                # ⚡ 优雅的幂等性设计：利用 setdefault 确保 "subscriptions" 键必然存在（若无则初始化为空列表）
                # 同时检查新的 topic 是否已经存在于订阅列表中，防止大模型重复发送指令导致突触配置无限叠加
                if topic_to_add not in config.setdefault("subscriptions", []):
                    # 物理追加新触突
                    config["subscriptions"].append(topic_to_add)
                    
                    # 将改写后的全新字典，重新序列化并永久写回物理磁盘
                    with open(yaml_path, 'w', encoding='utf-8') as f:
                        # allow_unicode=True 确保注释或中文字符不被转义，default_flow_style=False 保持漂亮的 YAML 块状层级
                        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
                    
                    logger.success(f"✅ YAML 基因已修改: {target_node} 现已永久包含 {topic_to_add}")
                    
                    # ========================================================
                    #  4. 神经递质触发：热重载广播
                    # ========================================================
                    # ⚠️ 关键一步：在物理文件改写成功后，运动皮层瞬间向内网发射一枚“全域神经递质”
                    # 这个信号将被对应的 target_node 拦截，促使其在不重启进程的前提下，动态重新断开并连接其 ZMQ 核心 Socket
                    await self.fire_signal("system.neuroplasticity", {
                        "target_node": target_node,
                        "new_topic": topic_to_add
                    })