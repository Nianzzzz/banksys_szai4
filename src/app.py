"""Streamlit 主入口。"""

import sys
from pathlib import Path

# 将项目根目录加入 sys.path，确保 src 包可被导入
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st

st.set_page_config(
    page_title="银行营销分析与预测",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 银行营销数据分析与预测系统")
st.markdown("""
欢迎使用银行营销数据分析与预测系统！

### 功能模块
- **📊 数据分析**：探索银行营销数据的分布、相关性和转化率
- **🔮 在线预测**：输入客户特征，预测是否会认购定期存款

请使用左侧导航栏选择功能。
""")
