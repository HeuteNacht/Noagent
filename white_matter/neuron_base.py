#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境与依赖初始化
# ========================================================
import sys
import zmq
import zmq.asyncio
import asyncio
import json
import yaml
import uuid
import os
from loguru import logger

# ========================================================
#  2. 仿生神经元基类定义
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
        #  3. 轴突绑定（PUB）与树突桥接（SUB）
        # ========================================================
        # 📢 轴突（Axon）演化：初始化为 ZMQ 的 PUB（发布）套接字
        self.axon = self.ctx.socket(zmq.PUB)
        bind_addr = f"tcp://*:{my_node['pub_port']}"
        self.axon.bind(bind_addr)
        logger.info(f"🧬 [{self.identity}] 轴突绑定至: {bind_addr}")

        # 🦻 树突（Dendrite）演化：初始化为 ZMQ 的 SUB（订阅）套接字
        self.dendrite = self.ctx.socket(zmq.SUB)
        # 动态激活受体：根据本地配置，订阅感兴趣的神经递质主题
        for topic in self.config.get('subscriptions', []):
            self.dendrite.setsockopt_string(zmq.SUBSCRIBE, topic)
            logger.info(f"🪢 [{self.identity}] 激活受体: {topic}")

        # 突触桥接：跨设备/跨进程连接到上游脑区
        for target in self.config.get('listen_to_nodes', []):
            if target in self.connectome:
                addr = f"tcp://{self.connectome[target]['host']}:{self.connectome[target]['pub_port']}"
                self.dendrite.connect(addr)
                logger.info(f"🔗 [{self.identity}] 桥接至 {target} ({addr})")

    # ========================================================
    #  4. 动作电位释放 (支持全链路追踪)
    # ========================================================
    async def fire_signal(self, topic: str, payload: dict, trace_id: str = None):
        """释放神经递质（发布消息）"""
        # 🎯 修复断链隐患：优先继承上游透传的 trace_id，确保一镜到底
        chosen_trace = trace_id or payload.get("trace_id") or uuid.uuid4().hex[:8]
        
        message = {
            "trace_id": chosen_trace, 
            "source": self.identity, 
            "payload": payload
        }
        
        await self.axon.send_multipart([
            topic.encode('utf-8'), 
            json.dumps(message, ensure_ascii=False).encode('utf-8')
        ])
        logger.debug(f"⚡️ [{self.identity}] 释放 -> {topic} (Trace: {chosen_trace})")

    # ========================================================
    #  5. 并发倾听与基因级热重载
    # ========================================================
    async def listen(self):
        """潜意识倾听：无限循环的异步接收流"""
        logger.success(f"🟢 [{self.identity}] 脑区激活，潜意识倾听中...")
        
        # 📡 基类特权：强制所有脑区订阅全网的系统级广播（神经可塑性信号）
        self.dendrite.setsockopt_string(zmq.SUBSCRIBE, "system.neuroplasticity")
        
        while True:
            parts = await self.dendrite.recv_multipart()
            topic = parts[0].decode('utf-8')
            message = json.loads(parts[1].decode('utf-8'))
            
            # ----------------------------------------------------
            # 🧬 基类层面的自愈与演化干预 (不干扰业务层)
            # ----------------------------------------------------
            if topic == "system.neuroplasticity":
                payload = message.get("payload", {})
                if payload.get("target_node") == self.identity:
                    action = payload.get("action", "add")
                    target_topic = payload.get("topic")
                    
                    if action == "add" and target_topic:
                        # 瞬间开辟新的受体通道 (有丝分裂)
                        self.dendrite.setsockopt_string(zmq.SUBSCRIBE, target_topic)
                        logger.success(f"🔥 [{self.identity}] 物理热重载成功！新受体 [{target_topic}] 已无缝接管。")
                    
                    elif action == "remove" and target_topic:
                        # 瞬间闭合指定的受体通道 (突触剪枝)
                        self.dendrite.setsockopt_string(zmq.UNSUBSCRIBE, target_topic)
                        logger.warning(f"✂️ [{self.identity}] 突触剪枝成功！旧受体 [{target_topic}] 已被剥离。")
                        
                # 拦截系统指令，直接进入下一次循环，不向下游业务层分发
                continue 

            # ----------------------------------------------------
            # 业务层信号分发
            # ----------------------------------------------------
            logger.debug(f"🧠 [{self.identity}] 捕捉 <- {topic} (Trace: {message.get('trace_id', 'unknown')})")
            asyncio.create_task(self.process_signal(topic, message))

    async def process_signal(self, topic: str, message: dict):
        # 留给具体脑区（前额叶/执行器等）去重写的虚函数
        pass

    # ========================================================
    #  6. 优雅停机与生命维持
    # ========================================================
    def shutdown(self):
        """切断神经连接并释放资源"""
        logger.info(f"🛑 [{self.identity}] 正在切断突触连接...")
        self.axon.setsockopt(zmq.LINGER, 0)
        self.dendrite.setsockopt(zmq.LINGER, 0)
        
        self.axon.close()
        self.dendrite.close()
        self.ctx.term()
        logger.success(f"💤 [{self.identity}] 已完全休眠。")
            
    def run(self):
        """脑区生命维持起搏器"""
        
        # 👇 ADD THIS BLOCK 👇
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # 👆 ADD THIS BLOCK 👆
            
        try: 
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        try: 
            loop.run_until_complete(self.listen())
        except KeyboardInterrupt:
            self.shutdown()