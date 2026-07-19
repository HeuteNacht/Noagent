#!/bin/bash
# ========================================================
#  1. 环境锚定与参数防御性清洗
# ========================================================
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")
CMD=$(echo "$1" | sed 's/—/-/g')

# 🧬 【双轨制核心对齐】：使用与 noa_cli.py 完全相同的物理锁与日志路径
PID_FILE="$DNA_DIR/.brain.pid"
LOG_FILE="$DNA_DIR/noa.log"

# ========================================================
#  2. 神经清剿反射弧 (升级为精准 PID 靶向阻断)
# ========================================================
purge_existing_neural_processes() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        # 探测进程是否存活 (使用 kill -0 不发信号仅探测)
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "🔄 正在执行手术刀级别的靶向阻断 (PID: $PID)..."
            kill -TERM "$PID" 2>/dev/null
            sleep 1
            echo -e "💤 物理链路切断，中枢督导树已被安全休眠。"
        else
            echo -e "⚠️ 进程已游离，执行空锁回收。"
        fi
        rm -f "$PID_FILE"
    else
        echo -e "✅ 当前物理宿主机内未发现活跃的 Noa 中枢。"
    fi
}

# ========================================================
#  3. 多路意图分发引擎
# ========================================================
case "$CMD" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo -e "⚠️ 基因锁 .brain.pid 存在且进程活跃，请先执行 noa stop！"
            exit 1
        fi
        
        echo -e "\033[1;34m=============================================================\033[0m"
        echo -e "⚡️ Noa ZMQ 分布式中枢起搏器点火 (Bash 极速模式)..."
        echo -e "\033[1;34m=============================================================\033[0m"
        
        # 拉起主进程并记录精确的 PID 到文件
        nohup python3 "$WORKSPACE/main.py" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        
        sleep 1
        echo -e "✅ \033[1;32m神经中枢已在后台潜意识运行 (PID: $(cat $PID_FILE))！终端已释放。\033[0m"
        ;;
    stop)
        purge_existing_neural_processes
        ;;
    tui)
        python3 "$DNA_DIR/local_tui.py"
        ;;
    approve)
        python3 "$DNA_DIR/device_manager.py"
        ;;
    log)
        tail -f "$LOG_FILE"
        ;;
    install|evolve)
        python3 "$DNA_DIR/sync_receptors.py"
        ;;
    *)
        echo -e "\033[1;32m🧠 Noa ZMQ Bionic AI System (Dual-Track Bash)\033[0m"
        echo "  noa start     - 唤醒集群 (极速后台启动)"
        echo "  noa stop      - 精准休眠全系统"
        echo "  noa tui       - 💻 进入本地交互终端"
        echo "  noa approve   - 🛡️ 审批外部设备接入"
        echo "  noa log       - 📜 追踪系统底层日志"
        echo "  noa install   - 🧬 重构受体环境"
        ;;
esac