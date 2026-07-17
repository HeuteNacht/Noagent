#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zmq
import zmq.asyncio
import asyncio
import json
import yaml
import uuid
import os
from loguru import logger

class NeuronNode:
    def __init__(self, local_config_path: str, connectome_path: str):
        with open(local_config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.identity = self.config['identity']
        
        with open(connectome_path, 'r', encoding='utf-8') as f:
            self.connectome = yaml.safe_load(f).get('nodes', {})
            
        if self.identity not in self.connectome:
            raise ValueError(f"❌ 基因缺陷: '{self.identity}' 未注册！")
            
        my_node = self.connectome[self.identity]
        self.ctx = zmq.asyncio.Context()
        
        self.axon = self.ctx.socket(zmq.PUB)
        bind_addr = f"tcp://*:{my_node['pub_port']}"
        self.axon.bind(bind_addr)
        logger.info(f"🧬 [{self.identity}] 轴突绑定至: {bind_addr}")

        self.dendrite = self.ctx.socket(zmq.SUB)
        for topic in self.config.get('subscriptions', []):
            self.dendrite.setsockopt_string(zmq.SUBSCRIBE, topic)
            logger.info(f"🪢 [{self.identity}] 激活受体: {topic}")

        for target in self.config.get('listen_to_nodes', []):
            if target in self.connectome:
                addr = f"tcp://{self.connectome[target]['host']}:{self.connectome[target]['pub_port']}"
                self.dendrite.connect(addr)
                logger.info(f"🔗 [{self.identity}] 桥接至 {target} ({addr})")

    async def fire_signal(self, topic: str, payload: dict):
        message = {"trace_id": uuid.uuid4().hex[:8], "source": self.identity, "payload": payload}
        await self.axon.send_multipart([topic.encode('utf-8'), json.dumps(message, ensure_ascii=False).encode('utf-8')])
        logger.debug(f"⚡️ [{self.identity}] 释放 -> {topic}")

    async def listen(self):
        logger.success(f"🟢 [{self.identity}] 脑区激活，潜意识倾听中...")
        while True:
            parts = await self.dendrite.recv_multipart()
            topic, message = parts[0].decode('utf-8'), json.loads(parts[1].decode('utf-8'))
            logger.debug(f"🧠 [{self.identity}] 捕捉 <- {topic}")
            asyncio.create_task(self.process_signal(topic, message))

    async def process_signal(self, topic: str, message: dict):
        pass

    def shutdown(self):
        """切断神经连接并释放资源"""
        logger.info(f"🛑 [{self.identity}] 正在切断突触连接...")
        # 设置 LINGER 为 0，防止 socket 挂起
        self.axon.setsockopt(zmq.LINGER, 0)
        self.dendrite.setsockopt(zmq.LINGER, 0)
        
        self.axon.close()
        self.dendrite.close()
        self.ctx.term()
        logger.success(f"💤 [{self.identity}] 已完全休眠。")

            
    def run(self):
        try: loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try: loop.run_until_complete(self.listen())
        except KeyboardInterrupt:
            self.shutdown()
