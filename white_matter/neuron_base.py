#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/white_matter/neuron_base.py
import zmq
import zmq.asyncio
import asyncio
import json
import yaml
import uuid
import os
from loguru import logger

# ========================================================
#  1. 仿生术语初始化与连接组映射
# ========================================================
class NeuronNode:
    def __init__(self, local_config_path: str, connectome_path: str):
        # 1. 读取本脑区的局部基因突触配置（如 synapse.yaml）
        with open(local_config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        # 确定本脑区的身份人格
        self.identity = self.config['identity']
        
        # 2. 读取全局“结构连接组”（known_nodes.yaml），即全网物理黄页
        with open(connectome_path, 'r', encoding='utf-8') as f:
            self.connectome = yaml.safe_load(f).get('nodes', {})

        # 基因缺陷检查：如果当前脑区没有在全局黄页中注册端口，直接熔断报错    
        if self.identity not in self.connectome:
            raise ValueError(f"❌ 基因缺陷: '{self.identity}' 未注册！")
            
        my_node = self.connectome[self.identity]
        # 初始化 ZMQ 的异步 asyncio 上下文（通信引擎的核心）
        self.ctx = zmq.asyncio.Context()
        
        # ========================================================
        #  2. 轴突绑定（PUB）与树突桥接（SUB）
        # ========================================================
        # 📢 轴突（Axon）演化：初始化为 ZMQ 的 PUB（发布）套接字
        self.axon = self.ctx.socket(zmq.PUB)
        bind_addr = f"tcp://*:{my_node['pub_port']}"
        # 绑定自身注册的端口，向外广播信号
        self.axon.bind(bind_addr)
        logger.info(f"🧬 [{self.identity}] 轴突绑定至: {bind_addr}")

        # 🦻 树突（Dendrite）演化：初始化为 ZMQ 的 SUB（订阅）套接字
        self.dendrite = self.ctx.socket(zmq.SUB)
        # 动态激活受体：根据本地配置，订阅感兴趣的神经递质主题（Topic）
        for topic in self.config.get('subscriptions', []):
            self.dendrite.setsockopt_string(zmq.SUBSCRIBE, topic)
            logger.info(f"🪢 [{self.identity}] 激活受体: {topic}")

        # 突触桥接：跨设备/跨进程连接到上游脑区
        for target in self.config.get('listen_to_nodes', []):
            if target in self.connectome:
                # 查黄页获取上游脑区的 IP 和端口
                addr = f"tcp://{self.connectome[target]['host']}:{self.connectome[target]['pub_port']}"
                # 将树突物理连接（Connect）过去
                self.dendrite.connect(addr)
                logger.info(f"🔗 [{self.identity}] 桥接至 {target} ({addr})")

    # ========================================================
    #  3. 动作电位释放与并发倾听
    # ========================================================
    async def fire_signal(self, topic: str, payload: dict):
        """释放神经递质（发布消息）"""
        # 每次释放信号时，默认生成一个 8 位的局部随机追踪 ID，并注入发射源标签
        message = {"trace_id": uuid.uuid4().hex[:8], "source": self.identity, "payload": payload}
        # 使用 ZMQ 的多段发送（Multipart），第一段为 Topic（用于路由过滤），第二段为 JSON 序列化数据
        await self.axon.send_multipart([topic.encode('utf-8'), json.dumps(message, ensure_ascii=False).encode('utf-8')])
        logger.debug(f"⚡️ [{self.identity}] 释放 -> {topic}")

    async def listen(self):
        """潜意识倾听：无限循环的异步接收流"""
        logger.success(f"🟢 [{self.identity}] 脑区激活，潜意识倾听中...")
        while True:
            # 异步挂起，静默等待上游消息段到来
            parts = await self.dendrite.recv_multipart()
            topic, message = parts[0].decode('utf-8'), json.loads(parts[1].decode('utf-8'))
            logger.debug(f"🧠 [{self.identity}] 捕捉 <- {topic}")
            # ⚡ 极高明的设计：收到信号后，立刻用 create_task 异步派生处理任务
            # 确保 listen 的接收循环瞬间回到下一轮 recv_multipart，绝不会因为 process_signal 的耗时而导致 ZMQ 缓冲区堆积
            asyncio.create_task(self.process_signal(topic, message))

    async def process_signal(self, topic: str, message: dict):
        # 留给具体脑区（前额叶/执行器等）去重写的虚函数
        pass

    def shutdown(self):
        """切断神经连接并释放资源"""
        logger.info(f"🛑 [{self.identity}] 正在切断突触连接...")
        # 🩺 核心避坑点：设置 LINGER 为 0
        # 强制 ZMQ 在关闭时丢弃缓冲区内未发出的残留消息，防止进程因等待网络对端而死锁挂起
        self.axon.setsockopt(zmq.LINGER, 0)
        self.dendrite.setsockopt(zmq.LINGER, 0)
        
        self.axon.close()
        self.dendrite.close()
        # 彻底销毁 Context 环境
        self.ctx.term()
        logger.success(f"💤 [{self.identity}] 已完全休眠。")

            
    def run(self):
        """脑区生命维持起搏器"""
        try: loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try: 
            # 阻塞式维持监听流
            loop.run_until_complete(self.listen())
        except KeyboardInterrupt:
            # 捕获外部终止信号（如 main.py 发出的销毁指令），优雅释放资源
            self.shutdown()
