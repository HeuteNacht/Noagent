#!/bin/bash
#Noagent/dna/noa_cli.sh
# ========================================================
#  1. 环境锚定与参数防御性清洗
# ========================================================
# 🧬 稳健的路径自锚定：利用 BASH_SOURCE 精准计算当前脚本所在的绝对物理目录 ~/Noagent/dna
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# 向上跳一级，捕获到系统的真实主目录 ~/Noagent
WORKSPACE=$(dirname "$DNA_DIR")

# 🛡️ 符号防御性清洗：利用 sed 把可能因为手机输入法或复制粘贴误输入的“长破折号（—）”
# 强行清洗替换为标准的“短横线（-）”，提高对外部混乱输入的免疫力和解析鲁棒性
CMD=$(echo "$1" | sed 's/—/-/g')

# ========================================================
#  2. 神经清剿反射弧（强力进程清理机制）
# ========================================================
purge_existing_neural_processes() {
    # 🪓 斩断旧脑区：使用 pkill -f 模糊匹配全路径，强行杀死可能残留在后台运行的各子脑区进程
    pkill -f "sensory_gateway/main.py" 2>/dev/null
    pkill -f "frontal_lobe/main.py" 2>/dev/null
    pkill -f "effector/main.py" 2>/dev/null
    pkill -f "main.py" 2>/dev/null

    # ⚡ 端口强行熔断：如果系统安有 fuser 工具，直接定向爆破占用 22222 端口（丘脑网关 WebSocket）的 TCP 连接
    # 确保重启时绝不会因为“Address already in use”导致端口争抢而启动失败
    if command -v fuser >/dev/null 2>&1; then fuser -k 22222/tcp >/dev/null 2>&1; fi
    sleep 1
}

# ========================================================
#  3. 多路意图分发引擎（Case 路由开关）
# ========================================================
case "$CMD" in
    start)
        # 【唤醒集群模式】
        # 1. 启动前先执行清剿，防止多实例重叠导致的脑区功能紊乱
        purge_existing_neural_processes
        echo -e "\033[1;34m=============================================================\033[0m"
        echo -e "⚡️ Noa ZMQ 分布式中枢起搏器点火 (后台守护模式)..."
        echo -e "\033[1;34m=============================================================\033[0m"
        
        # 🧠 守护进程化挂起：利用 nohup 在后台异步拉起起搏器主脚本，并将标准输出与错误全部重定向到物理日志流中
        # 这样即使你关闭当前终端，Noa 依然在操作系统的潜意识（后台）中稳健存活
        nohup python3 "$WORKSPACE/main.py" > "$WORKSPACE/thalamus.log" 2>&1 &
        sleep 1.5
        echo -e "✅ \033[1;32m神经中枢已在后台潜意识运行！终端已释放。\033[0m"
        ;;
    stop)
        # 【全强迫休眠模式】
        echo -e "🔄 正在清剿所有脑区进程..."
        purge_existing_neural_processes
        echo -e "💤 物理链路切断，分布式神经系统已被强制休眠。"
        ;;
    tui)
        # 【本地沉浸式交互】直连接口，直接拉起我们在前面解析的长连接黑客控制台
        python3 "$DNA_DIR/local_tui.py"
        ;;
    approve)
        # 【免疫系统介入】一键拉起审批控制台，用于管理员物理授权外部游离探针（如 iPhone）
        python3 "$DNA_DIR/device_manager.py"
        ;;
    log)
        # 【全链路日志追踪】利用 tail -f 挂起实时流，追踪全系统的异常动作电位与拦截流水
        tail -f "$WORKSPACE/thalamus.log"
        ;;
    install|evolve)
        # 【基因进化/热重载】路由执行 install.sh，触发逆转录引擎更新系统别名或 PATH 包装程序
        bash "$DNA_DIR/install.sh"
        ;;
    *)
        # 🎨 兜底帮助菜单：输出充满仿生科技色彩的 CLI 引导手册
        echo -e "\033[1;32m🧠 Noa ZMQ Bionic AI System\033[0m"
        echo "  noa start     - 唤醒集群 (后台静默运行)"
        echo "  noa stop      - 强制休眠全系统"
        echo "  noa tui       - 💻 进入本地交互终端"
        echo "  noa approve   - 🛡️ 审批外部设备接入"
        echo "  noa log       - 📜 追踪系统底层日志"
        echo "  noa install   - 🧬 热重载环境默认"
        echo "  noa evolve    - 🧬 热重载环境别名"
        ;;
esac
