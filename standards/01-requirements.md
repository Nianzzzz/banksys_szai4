# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里，不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 课堂项目要求 | 写成用户故事 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR，等待 CI 和 Review |
| 合并 | Done | PR 合并 main，自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号，PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI/CD · 状态: Backlog

作为 **项目开发者**，
我想要 项目具备基础工程结构、测试、CI 与 CD，
以便 后续每次开发都能自动检查并自动部署。

验收标准:
- AC1: 从 `main` 开 feature 分支完成初始化，不直接 push main。
- AC2: 项目结构符合 `00-project-context.md` 目录地图（src/, tests/, data/, models/ 等）。
- AC3: `pyproject.toml` 配置好 ruff、pytest、项目依赖。
- AC4: `requirements.txt` 和 `requirements-dev.txt` 分离生产与开发依赖。
- AC5: `.gitignore` 排除 models/、__pycache__/、.venv/ 等。
- AC6: PR 触发 CI，至少包含格式检查（ruff format）、静态检查（ruff check）、单元测试（pytest）、覆盖率检查（>= 80%）。
- AC7: CI 全绿后合并 main。
- AC8: 合并 main 自动触发 CD，部署后健康检查通过（Streamlit `/_stcore/health`）。
- AC9: 完成后更新 `standards/PROGRESS.md`。

技术备注:
- 使用 uv 管理本地环境。
- Docker 端口映射 8004:8501（Streamlit 默认 8501）。
- 本地不强制 docker build，交给 CI。

---

### US-2 数据加载与预处理模块 · 状态: Backlog

作为 **数据分析师**，
我想要 系统能自动加载并预处理银行营销数据，
以便 后续分析和建模有干净可靠的数据基础。

验收标准:
- AC1: Given `data/train.csv` 存在，When 调用加载函数，Then 返回包含全部 21 列的 DataFrame，数据类型正确。
- AC2: Given `data/test.csv` 存在，When 调用加载函数，Then 返回包含 20 列的 DataFrame（无 subscribe 列）。
- AC3: 缺失值被正确处理（unknown 视为缺失或保留，需明确策略）。
- AC4: 分类特征编码策略可配置（如 one-hot / label encoding）。
- AC5: 单元测试覆盖正常加载、文件缺失、列名异常等场景。
- AC6: ruff format + ruff check + pytest 全绿。

---

### US-3 数据分析交互页面 · 状态: Backlog

作为 **银行营销分析师**，
我想要 一个交互式数据看板来探索银行营销数据的分布和规律，
以便 我能快速理解客户画像和营销效果，为决策提供依据。

验收标准:
- AC1: Given 用户访问 Streamlit 应用，When 点击"数据分析"页面，Then 展示数据概览（行数、列数、数据类型、缺失值统计）。
- AC2: 用户可选择任意数值列查看分布直方图。
- AC3: 用户可选择任意分类列查看各分类的计数柱状图。
- AC4: 展示数值特征之间的相关性热力图。
- AC5: 展示目标变量 `subscribe` 的类别分布（yes/no 比例）。
- AC6: 支持按分类特征分组统计 subscribe 的转化率（如不同 job 的认购率）。
- AC7: 所有图表可交互（hover 显示数值、可筛选）。
- AC8: 页面加载无报错，数据正确展示。

技术备注:
- 使用 Streamlit 原生组件 + plotly/altair 交互图表。
- 大数据量时注意缓存（`@st.cache_data`）。

---

### US-4 离线模型训练 · 状态: Backlog

作为 **数据科学家**，
我想要 基于训练数据离线训练一个分类模型来预测客户是否会认购，
以便 该模型能被在线预测系统调用。

验收标准:
- AC1: Given 训练数据 `data/train.csv`，When 运行训练脚本，Then 输出训练好的模型文件到 `models/` 目录。
- AC2: 模型使用 scikit-learn 分类器（如 RandomForest / LogisticRegression / GradientBoosting，需选择最优）。
- AC3: 训练过程中进行 train/validation split 或 cross-validation。
- AC4: 模型在验证集上 AUC >= 0.75。
- AC5: 训练完成后打印模型评估指标（accuracy, precision, recall, f1, AUC）。
- AC6: 模型文件可通过 `joblib.load()` 正确加载。
- AC7: 单元测试覆盖模型训练流程、模型加载、预测输出格式。
- AC8: ruff format + ruff check + pytest 全绿。

技术备注:
- 训练脚本可在 CI 中运行（CD 部署时重新训练）。
- 模型产物不入 Git，.gitignore 排除 models/。
- 需处理分类特征编码（与 US-2 保持一致）。

---

### US-5 在线预测系统 · 状态: Backlog

作为 **银行营销人员**，
我想要 通过点选输入客户特征，系统实时告诉我该客户是否会认购定期存款，
以便 我能精准筛选高潜力客户，提高营销效率。

验收标准:
- AC1: Given 用户访问"在线预测"页面，When 页面加载完成，Then 展示所有可输入特征的点选控件（下拉框、滑块等）。
- AC2: 分类特征（job, marital, education 等）使用 selectbox/下拉框输入。
- AC3: 数值特征（age, duration, campaign 等）使用 slider/数字输入框输入。
- AC4: Given 用户填写完所有特征，When 点击"预测"按钮，Then 显示预测结果（认购/不认购）及置信概率。
- AC5: 预测结果页面展示清晰，使用颜色或图标区分结果。
- AC6: 模型未加载时显示友好提示，不崩溃。
- AC7: 单元测试覆盖预测函数的输入输出格式。
- AC8: ruff format + ruff check + pytest 全绿。

技术备注:
- 模型在应用启动时加载（`@st.cache_resource`）。
- 输入控件的选项值应从训练数据中提取，保证一致性。
- 预测函数应接受 DataFrame 输入，返回预测类别和概率。

---

### US-6 Docker 容器化部署 · 状态: Backlog

作为 **运维人员**，
我想要 应用能通过 Docker 容器一键部署，
以便 环境一致、部署可重复、便于 CI/CD 自动化。

验收标准:
- AC1: Given Dockerfile 存在，When 运行 `docker build`，Then 构建成功无报错。
- AC2: Given 容器启动，When 等待 3 秒后访问 `http://localhost:8004/_stcore/health`，Then 返回 200 OK。
- AC3: 容器内训练模型并启动 Streamlit 服务。
- AC4: Dockerfile 包含国内镜像源配置参数（`PIP_INDEX_URL` build arg）。
- AC5: 容器端口 8501 映射到主机 8004。

技术备注:
- 使用多阶段构建或精简基础镜像。
- Streamlit 默认端口 8501，主机映射 8004。

---

## 5. 非功能需求

- **安全**: 密钥只进 Secrets，不进 Git。
- **可维护**: 一需求一小 PR，避免大爆炸式提交。
- **可测试**: 核心逻辑必须有单元测试，覆盖率 >= 80%。
- **可部署**: 部署后必须有健康检查（`/_stcore/health`）。
- **性能**: Streamlit 页面加载 < 3 秒（使用缓存优化）。
