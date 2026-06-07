# 🏦 银行营销数据分析与预测系统

基于银行营销数据，使用 Streamlit 构建的交互式数据分析看板与在线预测应用。

## 功能

- **📊 数据分析**：数据概览、特征分布、相关性热力图、分组转化率分析
- **🔮 在线预测**：点选输入客户特征，实时预测是否会认购定期存款

## 技术栈

| 层 | 选型 |
|---|---|
| 语言 | Python 3.11+ |
| Web 框架 | Streamlit |
| 机器学习 | scikit-learn (GradientBoosting) |
| 数据处理 | pandas |
| 可视化 | plotly |
| 环境管理 | uv |
| 代码检查 | ruff |
| 测试 | pytest + pytest-cov |
| CI | GitHub Actions |

## 快速开始

### 1. 安装 uv

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆项目

```bash
git clone https://github.com/Nianzzzz/banksys_szai4.git
cd banksys_szai4
```

### 3. 安装依赖

```bash
uv sync --all-extras
```

### 4. 训练模型

```bash
uv run python -c "from src.model import train_model; from src.data_loader import load_train_data; df = load_train_data(); model, metrics = train_model(df); print(metrics)"
```

### 5. 启动应用

```bash
uv run streamlit run src/app.py --server.port 8004
```

访问 http://localhost:8004

## 项目结构

```
banksys_szai4/
├── data/                      # 数据集
│   ├── train.csv              # 训练集（含 subscribe 目标列）
│   └── test.csv               # 测试集
├── src/                       # 源码
│   ├── app.py                 # Streamlit 主入口
│   ├── config.py              # 配置常量
│   ├── data_loader.py         # 数据加载与预处理
│   ├── analysis.py            # 数据分析逻辑
│   ├── model.py               # 模型训练/预测
│   └── pages/                 # Streamlit 多页面
│       ├── 1_📊_数据分析.py
│       └── 2_🔮_在线预测.py
├── tests/                     # 测试
├── models/                    # 模型产物（不入 Git）
├── pyproject.toml             # 项目配置
├── .github/workflows/ci.yml   # CI 流水线
└── README.md
```

## 开发

```bash
# 代码格式检查
uv run ruff format --check .

# 自动格式化
uv run ruff format .

# 静态检查
uv run ruff check .

# 运行测试
uv run pytest --cov=src --cov-fail-under=80
```

## 数据说明

数据来源于银行营销活动，包含客户基本信息、联系方式、社会经济指标等特征。

- **目标变量**：`subscribe`（yes/no）—— 客户是否认购定期存款
- **训练集**：~22500 条记录
- **特征**：20 个（包括 age, job, marital, education, duration 等）
