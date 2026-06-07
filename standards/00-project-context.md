# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里，了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**: `banksys_szai4`
- **一句话目标**: 基于银行营销数据，构建一个包含数据分析看板和在线预测的 Web 应用
- **使用者/受益者**: 银行营销分析师 / 业务决策者 / 课堂演示
- **核心功能**:
  - 数据分析交互页面：对银行营销数据进行可视化探索（分布、相关性、分组统计等）
  - 在线预测系统：基于离线训练的模型，用户通过点选输入特征，实时预测客户是否会认购定期存款
- **输入/数据**:
  - 训练集: `data/train.csv`（含 `subscribe` 目标列，yes/no 二分类）
  - 测试集: `data/test.csv`（无目标列，用于最终预测输出）
  - 特征：age, job, marital, education, default, housing, loan, contact, month, day_of_week, duration, campaign, pdays, previous, poutcome, emp_var_rate, cons_price_index, cons_conf_index, lending_rate3m, nr_employed
  - 数据规模：训练集 ~22500 行，21 列
  - 数据不敏感（公开教学数据），可入 Git

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课堂指定版本 |
| Web 框架 | Streamlit | 快速构建数据应用，交互友好，适合教学 |
| 机器学习 | scikit-learn | 经典 ML 库，分类模型训练与预测 |
| 测试 | pytest | Python 生态标准测试框架 |
| 格式/静态检查 | ruff | 速度快，替代 black + flake8 |
| 打包/运行 | Docker | 容器化部署，环境一致性 |
| 环境管理 | uv | 快速 Python 包管理，替代 pip + venv |
| CI/CD | GitHub Actions | 通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
banksys_szai4/
├── standards/                    # AI 项目记忆与通用规范
├── data/                         # 数据集（可入 Git，公开教学数据）
│   ├── train.csv
│   └── test.csv
├── src/                          # 源码
│   ├── app.py                    # Streamlit 主入口
│   ├── pages/                    # Streamlit 多页面
│   │   ├── 1_📊_数据分析.py       # 数据分析看板
│   │   └── 2_🔮_在线预测.py       # 在线预测页面
│   ├── data_loader.py            # 数据加载与预处理
│   ├── analysis.py               # 数据分析逻辑
│   ├── model.py                  # 模型训练、保存、加载、预测
│   └── config.py                 # 配置常量
├── models/                       # 训练好的模型产物（.pkl，不入 Git，.gitignore 排除）
├── tests/                        # 测试
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   ├── test_model.py
│   └── test_app.py
├── pyproject.toml                # 项目配置（ruff、pytest、依赖）
├── requirements.txt              # 生产运行依赖
├── requirements-dev.txt          # CI/本地检查依赖
├── Dockerfile
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
├── .gitignore
└── README.md
```

> 新增目录前先更新本节，避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `>= 80%` |
| 构建 | `docker build` 成功 |
| 业务/模型指标 | 模型 AUC >= 0.75（训练阶段验证） |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**，只进 GitHub Secrets / 环境变量。
- `data/` 目录为公开教学数据，可入 Git。
- `models/` 目录为模型产物，**不入 Git**（.gitignore 排除），每次 CI/CD 运行时重新训练。
- `main` 分支受保护，日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys_szai4` | 应用名/容器名 |
| `<PORT>` | `8004` | 服务端口（本地 uv 部署） |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 内置健康检查端点 |

> 当前无服务器，仅做 CI + 本地 uv 部署。CD 待后续有服务器时补充。
