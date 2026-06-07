# PROGRESS.md · 项目进度 〔本项目活记忆 · AI 维护〕

> **作用**:记录项目当前状态、已完成事项、下一步 TODO、架构决策（ADR）、踩坑记录（GOTCHAS）。
> **更新时机**:每完成一个模块/每遇到一个坑/每次会话结束时更新。
> **格式**:时间倒序，最新在最上面。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **阶段**: 第①步 建仓（进行中）
- **上一步完成**: 用户确认需求，开始建仓
- **下一步 (TODO 第一条)**: 创建 GitHub 仓库，初始化项目结构
- **阻塞项**: 无

---

## TODO（第一批）

### Phase 1: 项目初始化与工程化（对应 US-1）

- [ ] T1.1: 创建 GitHub 仓库 `banksys_szai4`
- [ ] T1.2: 初始化项目目录结构（src/, tests/, data/, models/）
- [ ] T1.3: 配置 `pyproject.toml`（ruff、pytest、项目元数据、依赖）
- [ ] T1.4: 配置 `.gitignore`（models/, __pycache__/, .venv/, .ruff_cache/ 等）
- [ ] T1.5: 编写 GitHub Actions CI workflow（ruff format + ruff check + pytest --cov）
- [ ] T1.6: 创建 Streamlit 最小入口 `src/app.py`（含健康检查页面）
- [ ] T1.7: 本地 uv 环境自检全绿 → 发起 PR → 合并

### Phase 2: 数据模块（对应 US-2）

- [ ] T2.1: 实现 `src/data_loader.py`（加载 train.csv / test.csv，类型推断，缺失值处理）
- [ ] T2.2: 编写 `tests/test_data_loader.py`
- [ ] T2.3: 本地 CI 自检 → 发起 PR

### Phase 3: 数据分析页面（对应 US-3）

- [ ] T3.1: 实现 `src/analysis.py`（统计分析逻辑，纯函数）
- [ ] T3.2: 实现 `src/pages/1_📊_数据分析.py`（Streamlit 页面：概览、分布图、热力图、分组统计）
- [ ] T3.3: 编写 `tests/test_analysis.py`
- [ ] T3.4: 本地 CI 自检 → 发起 PR

### Phase 4: 模型训练（对应 US-4）

- [ ] T4.1: 实现 `src/model.py`（训练、评估、保存、加载、预测）
- [ ] T4.2: 训练模型，验证 AUC >= 0.75
- [ ] T4.3: 编写 `tests/test_model.py`
- [ ] T4.4: 本地 CI 自检 → 发起 PR

### Phase 5: 在线预测页面（对应 US-5）

- [ ] T5.1: 实现 `src/pages/2_🔮_在线预测.py`（点选输入 + 预测结果展示）
- [ ] T5.2: 编写 `tests/test_app.py`（预测函数测试）
- [ ] T5.3: 本地 CI 自检 → 发起 PR

### Phase 6: 本地部署与收尾（对应 US-6，无服务器，仅本地 uv 部署）

- [ ] T6.1: 更新 README.md（项目说明、uv 环境搭建、启动方式）
- [ ] T6.2: 本地 `uv run streamlit run src/app.py --server.port 8004` 验证通过
- [ ] T6.3: CI 全绿最终验证

---

## ADR（架构决策记录）

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 使用 Streamlit 而非 Flask/FastAPI | 课堂要求 + 快速构建数据应用 + 内置交互组件 |
| 2026-06-07 | 使用 uv 管理环境 | 速度快，替代 pip+venv，课堂要求 |
| 2026-06-07 | 模型产物不入 Git | 避免仓库膨胀，本地训练 |
| 2026-06-07 | 数据文件入 Git | 公开教学数据，规模小（~22500行），无敏感信息 |
| 2026-06-07 | 暂不做 CD，仅 CI + 本地 uv 部署 | 无服务器，待后续补充 |

---

## GOTCHAS（踩坑记录）

暂无。开发过程中遇到问题时在此记录。

---

## 里程碑 (DONE)

- [x] 2026-06-07: 读取全部 standards 文件，理解项目规范
- [x] 2026-06-07: 查看 data/train.csv 和 data/test.csv 数据结构
- [x] 2026-06-07: 填写 00-project-context.md（项目上下文）
- [x] 2026-06-07: 填写 01-requirements.md（6 个用户故事 + 验收标准）
- [x] 2026-06-07: 初始化 PROGRESS.md（TODO 列表 + ADR）
