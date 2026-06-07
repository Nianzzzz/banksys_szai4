"""数据加载与预处理模块。"""

from pathlib import Path

import pandas as pd

from src.config import TARGET_COL, TEST_CSV, TRAIN_CSV


def load_train_data(path: Path | str | None = None) -> pd.DataFrame:
    """加载训练数据（含 subscribe 目标列）。"""
    filepath = path or TRAIN_CSV
    df = pd.read_csv(filepath)
    if TARGET_COL not in df.columns:
        raise ValueError(f"训练数据缺少目标列 '{TARGET_COL}'")
    return df


def load_test_data(path: Path | str | None = None) -> pd.DataFrame:
    """加载测试数据（无 subscribe 目标列）。"""
    filepath = path or TEST_CSV
    df = pd.read_csv(filepath)
    if TARGET_COL in df.columns:
        raise ValueError(f"测试数据不应包含目标列 '{TARGET_COL}'")
    return df


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """获取特征列名（排除 id 和目标列）。"""
    exclude = {"id", TARGET_COL}
    return [c for c in df.columns if c not in exclude]


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """获取分类特征列名。"""
    return [c for c in df.select_dtypes(include=["object", "category"]).columns if c != TARGET_COL]


def get_numerical_columns(df: pd.DataFrame) -> list[str]:
    """获取数值特征列名。"""
    return df.select_dtypes(include=["number"]).columns.tolist()
