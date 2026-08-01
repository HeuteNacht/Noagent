#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 全局皮层智能发现引擎 (Global Genome Auto-Discovery Protocol)
作用：自动扫描 brain 目录下所有脑区，动态分配 ZMQ 端口，并注册新发现的皮层脚本。
"""
import os
import yaml

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)
BRAIN_DIR = os.path.join(WORKSPACE, "brain")
KNOWN_NODES_PATH = os.path.join(DNA_DIR, "known_nodes.yaml")

def intelligent_scan():
    print("🧬 启动全脑智能发现序列 (Global Cortex Auto-Discovery)...")
    
    # ---------------------------------------------------------
    # 1. 扫描物理脑区目录 & 自动更新全局注册表 known_nodes.yaml
    # ---------------------------------------------------------
    # 读取已注册节点
    if os.path.exists(KNOWN_NODES_PATH):
        with open(KNOWN_NODES_PATH, 'r', encoding='utf-8') as f:
            connectome = yaml.safe_load(f) or {}
    else:
        connectome = {}
        
    if 'nodes' not in connectome: connectome['nodes'] = {}
    known_nodes = connectome['nodes']
    
    # 计算当前已分配的最大端口，避免冲突 (基准从 22000 开始)
    existing_ports = [config.get('pub_port', 22000) for config in known_nodes.values()]
    max_port = max(existing_ports) if existing_ports else 22000

    # 扫描物理存在的脑区目录 (排除了 __pycache__ 等无效目录)
    physical_lobes = [d for d in os.listdir(BRAIN_DIR) if os.path.isdir(os.path.join(BRAIN_DIR, d)) and not d.startswith("__")]
    
    global_update_needed = False
    for lobe in physical_lobes:
        if lobe not in known_nodes:
            max_port += 1
            known_nodes[lobe] = {
                'host': '127.0.0.1',
                'pub_port': max_port
            }
            print(f"  🌐 [中枢拓扑] 发现全新脑区器官: {lobe} -> 已分配突触端口 {max_port}")
            global_update_needed = True

    # 刷入全局注册表
    if global_update_needed:
        with open(KNOWN_NODES_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(connectome, f, allow_unicode=True, sort_keys=False)
        print("  ✅ [中枢拓扑] 全局路由表 (known_nodes.yaml) 更新完毕。")

    # ---------------------------------------------------------
    # 2. 深度扫描各个脑区的 cortex 目录，并更新 cortex_config.yaml
    # ---------------------------------------------------------
    for lobe in physical_lobes:
        cortex_dir = os.path.join(BRAIN_DIR, lobe, "cortex")
        config_path = os.path.join(BRAIN_DIR, lobe, "cortex_config.yaml")
        
        # 如果这个脑区没有 cortex 目录（例如 sensory_gateway），则跳过
        if not os.path.exists(cortex_dir):
            continue
            
        # 扫描存在的皮层脚本
        py_files = [f[:-3] for f in os.listdir(cortex_dir) if f.endswith('.py') and not f.startswith("__")]
        
        # 读取该脑区现有的 config
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}
        else:
            config_data = {}
            
        if 'functional_areas' not in config_data:
            config_data['functional_areas'] = []
            
        areas = config_data['functional_areas']
        if areas is None: areas = []
        
        existing_areas_names = {a.get('name', '') for a in areas}
        
        lobe_updated = False
        for py_module in py_files:
            if py_module not in existing_areas_names:
                areas.append({
                    'name': py_module,
                    'description': f"Auto-detected cortex: {py_module}",
                    'enabled': True # 默认开启新发现的皮层
                })
                print(f"  🧠 [{lobe}] 自动接管并注册游离皮层: {py_module}.py")
                lobe_updated = True
                
        if lobe_updated:
            config_data['functional_areas'] = areas
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)
            print(f"  ✅ [{lobe}] 脑区基因锁 (cortex_config.yaml) 更新完毕。")

    print("\n🎉 全脑扫描完成！所有新脑区与皮层已加入生命周期管理。")
    print("💡 请执行 `noa restart` 强力重载使新神经网生效。")

if __name__ == "__main__":
    intelligent_scan()
