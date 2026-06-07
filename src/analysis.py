"""数据分析逻辑（纯函数，不依赖 Streamlit）。"""

import pandas as pd


def data_overview(df: pd.DataFrame) -> dict:
    """返回数据概览：行数、列数、各列类型、缺失值统计。"""
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
    }


def value_counts(df: pd.DataFrame, col: str) -> pd.Series:
    """返回指定列的值计数。"""
    return df[col].value_counts()


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """返回数值列的相关性矩阵。"""
    numeric_df = df.select_dtypes(include=["number"])
    return numeric_df.corr()


def group_conversion_rate(
    df: pd.DataFrame, group_col: str, target_col: str = "subscribe"
) -> pd.DataFrame:
    """按分组列统计目标列的转化率（yes 比例）。"""
    grouped = df.groupby(group_col)[target_col].value_counts(normalize=True).unstack(fill_value=0)
    if "yes" in grouped.columns:
        result = grouped[["yes"]].rename(columns={"yes": "conversion_rate"})
    else:
        result = grouped.iloc[:, :1].rename(columns={grouped.columns[0]: "conversion_rate"})
    return result.sort_values("conversion_rate", ascending=False)


def target_distribution(df: pd.DataFrame, target_col: str = "subscribe") -> pd.Series:
    """返回目标变量的类别分布。"""
    return df[target_col].value_counts()
