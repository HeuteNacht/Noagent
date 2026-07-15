#!/usr/bin/env python3
import os, sys, asyncio
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)
from white_matter.neuron_base import NeuronNode
from loguru import logger

class Effector(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "action.execute":
            cmd = message.get("payload", {}).get("command")
            logger.warning(f"🦾 触发动作: {cmd}")
            if cmd == "wake_babe_server":
                logger.info("   ↳ 发射 WOL 唤醒...")
            elif cmd == "shutdown_host":
                logger.critical("   ↳ 关机序列启动...")

if __name__ == "__main__":
    Effector(os.path.join(os.path.dirname(__file__), "synapse.yaml"), os.path.join(_ROOT, "dna", "known_nodes.yaml")).run()
