#!/bin/bash
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")
CMD=$(echo "$1" | sed 's/—/-/g')

purge_existing_neural_processes() {
    pkill -f "sensory_gateway/main.py" 2>/dev/null
    pkill -f "frontal_lobe/main.py" 2>/dev/null
    pkill -f "effector/main.py" 2>/dev/null
    pkill -f "main.py" 2>/dev/null
    if command -v fuser >/dev/null 2>&1; then fuser -k 22222/tcp >/dev/null 2>&1; fi
    sleep 1
}

case "$CMD" in
    start)
        purge_existing_neural_processes
        echo -e "\033[1;34m=============================================================\033[0m"
        echo -e "⚡️ Noa ZMQ 分布式中枢起搏器点火 (后台守护模式)..."
        echo -e "\033[1;34m=============================================================\033[0m"
        nohup python3 "$WORKSPACE/main.py" > "$WORKSPACE/thalamus.log" 2>&1 &
        sleep 1.5
        echo -e "✅ \033[1;32m神经中枢已在后台潜意识运行！终端已释放。\033[0m"
        ;;
    stop)
        echo -e "🔄 正在清剿所有脑区进程..."
        purge_existing_neural_processes
        echo -e "💤 物理链路切断，分布式神经系统已被强制休眠。"
        ;;
    tui)
        python3 "$DNA_DIR/local_tui.py"
        ;;
    approve)
        python3 "$DNA_DIR/device_manager.py"
        ;;
    log)
        tail -f "$WORKSPACE/thalamus.log"
        ;;
    install|evolve)
        bash "$DNA_DIR/install.sh"
        ;;
    *)
        echo -e "\033[1;32m🧠 Noa ZMQ Bionic AI System\033[0m"
        echo "  noa start     - 唤醒集群 (后台静默运行)"
        echo "  noa stop      - 强制休眠全系统"
        echo "  noa tui       - 💻 进入本地交互终端"
        echo "  noa approve   - 🛡️ 审批外部设备接入"
        echo "  noa log       - 📜 追踪系统底层日志"
        echo "  noa install   - 🧬 热重载环境别名"
        ;;
esac
