#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/dna/cortex_manager.py

import os
import yaml
import pkgutil

# 精准锚定物理路径
DNA_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(DNA_DIR, '..'))
FRONTAL_LOBE_DIR = os.path.join(ROOT_DIR, "brain", "frontal_lobe")
CORTEX_DIR = os.path.join(FRONTAL_LOBE_DIR, "cortex")
CONFIG_PATH = os.path.join(FRONTAL_LOBE_DIR, "cortex_config.yaml")

def main():
    print("\033[1;35m========================================\033[0m")
    print("🧠 Noa 皮层基因图谱重组终端 (Cortex Manager)")
    print("\033[1;35m========================================\033[0m")

    # 1. 读取现有的 YAML 配置 (若无则初始化空图谱)
    config_data = {"functional_areas": []}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {"functional_areas": []}
        except Exception as e:
            print(f"❌ 解析现有 cortex_config.yaml 失败: {e}")
            return

    existing_areas = {area["name"]: area for area in config_data.get("functional_areas", [])}
    
    # 2. 扫描物理目录，发现所有皮层模块
    if not os.path.exists(CORTEX_DIR):
        print("⚠️ 未发现 cortex 物理目录，皮层完全缺失。")
        return

    found_modules = []
    for _, module_name, _ in pkgutil.iter_modules([CORTEX_DIR]):
        found_modules.append(module_name)

    if not found_modules:
        print("✅ 当前 cortex 目录下没有发现任何子程序。")
        return

    print(f"\n🧬 物理扫描完毕，共发现 \033[1;36m{len(found_modules)}\033[0m 个脑区模块。\n")

    # 3. 开始交互式注入
    updated_areas = []
    for mod_name in found_modules:
        is_known = mod_name in existing_areas
        current_status = existing_areas[mod_name]["enabled"] if is_known else None
        
        status_text = ""
        if current_status is True:
            status_text = "[\033[1;32m已激活\033[0m]"
        elif current_status is False:
            status_text = "[\033[1;31m已封印\033[0m]"
        else:
            status_text = "[\033[1;33m野生突变\033[0m]"

        desc = existing_areas[mod_name].get("description", "自定义拓展脑区") if is_known else "自定义拓展脑区"

        print(f"🧩 脑区: \033[1;37m{mod_name}\033[0m {status_text}")
        ans = input(f"   ❓ 是否激活该脑区？(y:激活 / n:封印 / skip:跳过保持原样): ").strip().lower()
        
        if ans == 'y':
            updated_areas.append({"name": mod_name, "description": desc, "enabled": True})
            print("   ✅ 基因已固化: 允许放行。")
        elif ans == 'n':
            updated_areas.append({"name": mod_name, "description": desc, "enabled": False})
            print("   ⛔ 基因已固化: 物理绞杀。")
        else:
            # 保持原样，如果之前有配置就沿用
            if is_known:
                updated_areas.append(existing_areas[mod_name])
            print("   ⏳ 维持现状。")
        print("-" * 40)

    # 4. 覆盖写入 YAML
    config_data["functional_areas"] = updated_areas
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print("\n🎉 基因图谱重组完成！请执行 `noa restart` 或 `noa start` 使新皮层生效。")
    except Exception as e:
        print(f"\n❌ 落盘失败: {e}")

if __name__ == "__main__":
    main()
