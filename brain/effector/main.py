import yaml # 确保导入 yaml

class Effector(NeuronNode):
    async def process_signal(self, topic: str, message: dict):
        if topic == "action.execute":
            payload = message.get("payload", {})
            cmd = payload.get("command")
            
            if cmd == "rewire_yaml":
                target_node = payload.get("target_node")
                topic_to_add = payload.get("topic_to_add")
                logger.warning(f"🧬 激活神经可塑性: 正在重连 [{target_node}] 的突触...")
                
                # 定位目标脑区的 YAML 文件
                yaml_path = os.path.join(_ROOT, "brain", target_node, "synapse.yaml")
                
                if not os.path.exists(yaml_path):
                    logger.error(f"❌ 找不到节点 {target_node} 的突触配置文件。")
                    return
                
                # 读写修改 YAML
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # 幂等性检查：如果已经订阅，则跳过
                if topic_to_add not in config.setdefault("subscriptions", []):
                    config["subscriptions"].append(topic_to_add)
                    
                    with open(yaml_path, 'w', encoding='utf-8') as f:
                        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
                    
                    logger.success(f"✅ YAML 基因已修改: {target_node} 现已永久包含 {topic_to_add}")
                    
                    # ⚠️ 关键一步：发送热重载信号，通知目标节点立刻生效
                    await self.fire_signal("system.neuroplasticity", {
                        "target_node": target_node,
                        "new_topic": topic_to_add
                    })