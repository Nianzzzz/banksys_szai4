"""在线预测页面。"""

import pandas as pd
import streamlit as st

from src.data_loader import get_feature_columns, load_train_data
from src.model import load_model, predict

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")
st.title("🔮 在线预测")


# 加载数据（用于获取特征选项）
@st.cache_data
def get_train_df():
    return load_train_data()


# 加载模型
@st.cache_resource
def get_model():
    try:
        return load_model()
    except FileNotFoundError:
        return None


train_df = get_train_df()
model_result = get_model()

if model_result is None:
    st.warning("⚠️ 模型尚未训练。请先运行 `python -m src.model` 训练模型。")
    st.stop()

model, encoders = model_result
feature_cols = get_feature_columns(train_df)

st.markdown("请填写客户特征信息，然后点击预测按钮。")

# 构建输入表单
with st.form("prediction_form"):
    cols = st.columns(3)
    input_values = {}

    for i, col_name in enumerate(feature_cols):
        with cols[i % 3]:
            if col_name in train_df.select_dtypes(include=["object", "category"]).columns:
                # 分类特征：下拉框
                options = sorted(train_df[col_name].dropna().unique().tolist())
                input_values[col_name] = st.selectbox(col_name, options, key=f"input_{col_name}")
            else:
                # 数值特征：数字输入
                col_min = float(train_df[col_name].min())
                col_max = float(train_df[col_name].max())
                col_mean = float(train_df[col_name].median())
                input_values[col_name] = st.number_input(
                    col_name,
                    min_value=col_min,
                    max_value=col_max,
                    value=col_mean,
                    step=1.0 if col_max - col_min > 100 else 0.1,
                    key=f"input_{col_name}",
                )

    submitted = st.form_submit_button("🔮 预测", use_container_width=True)

if submitted:
    input_df = pd.DataFrame([input_values])
    result = predict(model, encoders, input_df)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if result["prediction"] == "yes":
            st.success("### 预测结果：✅ 认购")
        else:
            st.error("### 预测结果：❌ 不认购")

    with col2:
        st.metric("置信概率", f"{result['probability']:.1%}")
