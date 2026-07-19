# 🧠 Noa: ZMQ Bionic AI System

Noa 是一个基于“神经科学底层原理”构建的分布式、去中心化具身智能网关系统。它抛弃了传统的单体架构，采用 ZeroMQ (ZMQ) 模拟大脑的“白质纤维束”，实现真正的“结构决定功能”。具备极高的抗宕机能力、热重载特性以及零信任准入机制。

## 📂 基因图谱 (Directory Structure)

```text
~/Noagent/
├── README.md                     # 项目文档
├── main.py                       # 脑干起搏器 (一键拉起所有脑区子进程)
├── requirements.txt              # 营养液依赖包
├── dna/                          # 遗传物质与自动化引擎
│   ├── known_nodes.yaml          # 结构连接组 (全局物理黄页)
│   ├── receptors.yaml            # 动态受体配置 (Alias/PATH 声明)
│   ├── sync_receptors.py         # 逆转录引擎 (解析 YAML 生成 bash)
│   ├── install.sh                # 核心有丝分裂流水线 (noa install)
│   ├── noa_cli.sh                # 系统 CLI 路由器 (noa start/stop/...)
│   ├── device_manager.py         # 免疫系统审批终端 (noa approve)
│   ├── local_tui.py              # 本地沉浸式超级终端 (noa tui)
│   └── *.json                    # 动态生成的设备白名单与待审批库
├── white_matter/                 # 核心物理底层
│   └── neuron_base.py            # 神经元基类 (封装 ZMQ PUB/SUB 异步引擎)
└── brain/                        # 灰质脑区模块 (随时热拔插)
    ├── sensory_gateway/          # 丘脑网关 (FastAPI, 拦截外网并转化递质)
    ├── frontal_lobe/             # 前额叶 (意图解析与决策)
    └── effector/                 # 运动皮层 (执行物理脚本/WOL/系统命令)

🧬 核心特性 (Core Features)
 去中心化突触网络 (ZMQ Pub/Sub)：各脑区独立运行，完全解耦。杀死任何一个脑区（如 ⁠effector⁠），系统其余部分依然稳健运行，实现绝对的进程隔离。
 零信任免疫屏障 (Zero-Trust)：丘脑网关默认拒绝一切外来 WebSocket 连接。外部设备（如 iOS）需生成唯一 ⁠CLIENT_ID⁠ 并经历 ⁠noa approve⁠ 白名单授权后方可接入。
 双重动态受体 (Dual Receptors)：基于 ⁠receptors.yaml⁠ 的数据驱动架构，一键（⁠noa install⁠）生成 Bash Alias 与 ⁠~/.local/bin/⁠ 下的物理可执行文件，实现多维命令挂载。
🚀 部署与系统指令 (CLI Usage)
系统内置中枢路由管理器，支持以下核心指令：

noa start
noa stop
noa install
noa tui
noa approve
noa log

📱 游离神经探针 (iOS Integration)
Noa 完美支持通过 iOS 端的 Pythonista 3 应用进行远程异地接入（依赖 Tailscale 组网）。
提供两种典型交互模式：
1. Siri 语音接管模式 (⁠siri_noa.py⁠)：结合 iOS 快捷指令，实现无手眼（Hands-free）交互。Pythonista 在后台携带合法基因锁静默收发数据，Siri 负责朗读中枢反馈。
2. 沉浸式控制台 (⁠tui_noa.py⁠)：在 iPhone 端呈现黑客风命令提示符。支持长连接心跳保活、隐式静默握手检测，以及异常状态的智能捕获。
🔌 开发者热拔插指南 (Hot-plug Guide)
1. 新增终端命令 (CLI Tool)
1. 编辑 ⁠~/Noagent/dna/receptors.yaml⁠ 添加你的快捷指令与执行路径。
2. （可选）编辑 ⁠~/Noagent/dna/noa_cli.sh⁠ 添加子命令路由分支。
3. 终端执行 ⁠noa install⁠，瞬间生效。
2. 培育新脑区 (New Brain Region)
1. 在 ⁠~/Noagent/brain/⁠ 下新建文件夹（如 ⁠amygdala/⁠）。
2. 创建 ⁠synapse.yaml⁠ 声明你需要监听的 ⁠subscriptions⁠ (上游信号) 以及 ⁠listen_to_nodes⁠ (全局黄页注册的节点)。
3. 继承 ⁠NeuronNode⁠ 编写几行 Python 处理逻辑，启动该进程即可自动汇入主神经网络。完全无需修改已有系统的任何代码。
