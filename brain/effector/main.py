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
                # 示例：异步执行系统 ping 或 wakeonlan 命令
                await self.async_exec("wakeonlan 00:11:22:33:44:55")
                
            elif cmd == "shutdown_host":
                logger.critical("   ↳ 关机序列启动...")
                # 示例：异步执行关机命令
                await self.async_exec("shutdown /s /t 10")

    async def async_exec(self, command: str):
        """底层的异步子进程执行器"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.success(f"✅ 执行成功: {stdout.decode().strip()}")
            else:
                logger.error(f"❌ 执行失败: {stderr.decode().strip()}")
        except Exception as e:
            logger.error(f"⚠️ 子进程异常: {e}")

if __name__ == "__main__":
    Effector(
        os.path.join(os.path.dirname(__file__), "synapse.yaml"), 
        os.path.join(_ROOT, "dna", "known_nodes.yaml")
    ).run()
