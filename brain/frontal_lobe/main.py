#!/usr/bin/env python3
import os, sys
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _ROOT not in sys.path: sys.path.insert(0, _ROOT)
from white_matter.neuron_base import NeuronNode
from loguru import logger

class FrontalLobe(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "stimulus.raw":
            content = message.get("payload", {}).get("content", "")
            logger.info(f"🤔 意图解析: [{content}]")
            if "唤醒" in content and "babe" in content.lower():
                await self.fire_signal("action.execute", {"command": "wake_babe_server"})
            elif "关机" in content:
                await self.fire_signal("action.execute", {"command": "shutdown_host"})
            else:
                logger.info(f"🤷 无需物理行动: {content}")

if __name__ == "__main__":
    FrontalLobe(os.path.join(os.path.dirname(__file__), "synapse.yaml"), os.path.join(_ROOT, "dna", "known_nodes.yaml")).run()
