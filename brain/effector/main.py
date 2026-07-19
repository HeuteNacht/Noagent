#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境初始化与依赖导入
# ========================================================
import os
import sys
import yaml
import asyncio
import subprocess

# 动态计算根路径，确保物理环境绝对隔离与精准寻址
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: 
    sys.path.insert(0, _ROOT)

from white_matter.neuron_base import NeuronNode
from loguru import logger

# ========================================================
#  2. 并发防御锁 (Race Condition Defense)
# ========================================================
# 全局异步锁：确保在前额叶高频下发多个改写指令时，
# 物理 YAML 文件的读写在同一微秒内是绝对串行的，防止文件写崩。
_synapse_lock = asyncio.Lock()

# ========================================================
#  3. 运动皮层类声明与信号路由拦截
# ========================================================
class Effector(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "action.execute":
            payload = message.get("payload", {})
            cmd = payload.get("command")
            trace_id = payload.get("trace_id", "unknown")
            
            # ----------------------------------------------------
            # ⚡️ 物理反射弧：跨平台执行指令
            # ----------------------------------------------------
            if cmd == "shutdown_host":
                if sys.platform == "win32":
                    logger.critical(f"🦾 [{trace_id}] Windows 11 关机序列启动...")
                    subprocess.Popen("shutdown /s /t 10", shell=True)
                else:
                    logger.critical(f"🦾 [{trace_id}] Debian 13 关机序列启动...")
                    subprocess.Popen("sudo shutdown -h now", shell=True)
                    
            # ----------------------------------------------------
            # 🧬 神经可塑性：突触重连 (Rewire)
            # ----------------------------------------------------
            elif cmd == "rewire_yaml":
                target_node = payload.get("target_node")
                topic_to_add = payload.get("topic_to_add")
                await self._modify_synapse(target_node, topic_to_add, action="add", trace_id=trace_id)

            # ----------------------------------------------------
            # ✂️ 神经可塑性：突触剪枝 (Prune)
            # ----------------------------------------------------
            elif cmd == "prune_yaml":
                target_node = payload.get("target_node")
                topic_to_remove = payload.get("topic_to_remove")
                await self._modify_synapse(target_node, topic_to_remove, action="remove", trace_id=trace_id)

    # ========================================================
    #  4. 基因读写引擎 (受锁保护的异步 I/O)
    # ========================================================
    async def _modify_synapse(self, target_node: str, topic: str, action: str, trace_id: str):
        """
        统一的突触基因修改引擎，包含文件锁和线程池防阻塞机制
        """
        if not target_node or not topic:
            return

        yaml_path = os.path.join(_ROOT, "brain", target_node, "synapse.yaml")

        if not os.path.exists(yaml_path):
            logger.error(f"❌ [{trace_id}] 找不到节点 {target_node} 的突触配置文件。")
            return

        # 🔒 激活互斥锁，进入临界区
        async with _synapse_lock:
            try:
                # ⚡ 关键优化：将阻塞的磁盘 I/O 推入线程池，防止阻塞 ZMQ 主循环
                config = await asyncio.to_thread(self._read_yaml, yaml_path)
                
                subscriptions = config.setdefault("subscriptions", [])
                modified = False

                # 逻辑分支：有丝分裂 vs 突触剪枝
                if action == "add" and topic not in subscriptions:
                    logger.warning(f"🧬 [{trace_id}] 激活神经可塑性: 正在为 [{target_node}] 接入受体 [{topic}]...")
                    subscriptions.append(topic)
                    modified = True
                    
                elif action == "remove" and topic in subscriptions:
                    logger.warning(f"✂️ [{trace_id}] 激活突触剪枝: 正在剥离 [{target_node}] 的受体 [{topic}]...")
                    subscriptions.remove(topic)
                    modified = True

                # 落盘并广播热重载信号
                if modified:
                    await asyncio.to_thread(self._write_yaml, yaml_path, config)
                    logger.success(f"✅ YAML 基因改写完毕: {target_node} 的突触配置已更新。")
                    
                    # ⚠️ 全域广播：通知底层 NeuronBase 瞬间执行 setsockopt 绑定/解绑
                    await self.fire_signal("system.neuroplasticity", {
                        "target_node": target_node,
                        "topic": topic,
                        "action": action # 告知底层是 "add" 还是 "remove"
                    })
                else:
                    logger.debug(f"ℹ️ [{trace_id}] 突触网络无需变动 (幂等过滤)。")

            except Exception as e:
                logger.error(f"❌ 突触改写引发崩溃: {str(e)}")

    def _read_yaml(self, path: str) -> dict:
        """物理文件读取（由 asyncio.to_thread 调度）"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def _write_yaml(self, path: str, config: dict):
        """物理文件写入（由 asyncio.to_thread 调度）"""
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

if __name__ == "__main__":
    # 初始化运动皮层，挂载配置文件并启动 ZMQ 监听
    Effector(
        os.path.join(os.path.dirname(__file__), "synapse.yaml"),
        os.path.join(_ROOT, "dna", "known_nodes.yaml")
    ).run()