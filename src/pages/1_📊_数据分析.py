"""数据分析交互页面。"""

import plotly.express as px
import streamlit as st

from src.analysis import (
    correlation_matrix,
    data_overview,
    group_conversion_rate,
    target_distribution,
    value_counts,
)
from src.data_loader import (
    get_categorical_columns,
    get_numerical_columns,
    load_train_data,
)

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")
st.title("📊 数据分析")

# 加载数据
df = load_train_data()

# 1. 数据概览
st.header("数据概览")
overview = data_overview(df)
col1, col2, col3 = st.columns(3)
col1.metric("行数", f"{overview['rows']:,}")
col2.metric("列数", overview["cols"])
col3.metric("缺失值总数", sum(overview["missing"].values()))

with st.expander("查看各列详情"):
    import pandas as pd

    info_df = pd.DataFrame(
        {
            "列名": list(overview["dtypes"].keys()),
            "类型": list(overview["dtypes"].values()),
            "缺失数": list(overview["missing"].values()),
            "缺失率(%)": list(overview["missing_pct"].values()),
        }
    )
    st.dataframe(info_df, use_container_width=True)

# 2. 目标变量分布
st.header("目标变量分布")
target_dist = target_distribution(df)
fig_target = px.pie(
    values=target_dist.values,
    names=target_dist.index,
    title="subscribe 分布",
    color_discrete_map={"yes": "#2ecc71", "no": "#e74c3c"},
)
st.plotly_chart(fig_target, use_container_width=True)

# 3. 数值特征分布
st.header("数值特征分布")
num_cols = get_numerical_columns(df)
selected_num = st.selectbox("选择数值列", num_cols)
fig_hist = px.histogram(df, x=selected_num, title=f"{selected_num} 分布", marginal="box")
st.plotly_chart(fig_hist, use_container_width=True)

# 4. 分类特征分布
st.header("分类特征分布")
cat_cols = get_categorical_columns(df)
selected_cat = st.selectbox("选择分类列", cat_cols)
cat_counts = value_counts(df, selected_cat)
fig_bar = px.bar(
    x=cat_counts.index,
    y=cat_counts.values,
    title=f"{selected_cat} 分布",
    labels={"x": selected_cat, "y": "数量"},
)
st.plotly_chart(fig_bar, use_container_width=True)

# 5. 相关性热力图
st.header("数值特征相关性")
corr = correlation_matrix(df)
fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="相关性热力图",
    aspect="auto",
)
st.plotly_chart(fig_corr, use_container_width=True)

# 6. 分组转化率
st.header("分组转化率分析")
group_col = st.selectbox("选择分组列", cat_cols, key="group_col")
conv_df = group_conversion_rate(df, group_col)
fig_conv = px.bar(
    x=conv_df.index,
    y=conv_df["conversion_rate"],
    title=f"按 {group_col} 分组的认购转化率",
    labels={"x": group_col, "y": "转化率"},
)
fig_conv.update_layout(yaxis_tickformat=".1%")
st.plotly_chart(fig_conv, use_container_width=True)
