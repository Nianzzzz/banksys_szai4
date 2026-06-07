"""数据加载模块测试。"""

import pandas as pd
import pytest

from src.config import TARGET_COL
from src.data_loader import (
    get_categorical_columns,
    get_feature_columns,
    get_numerical_columns,
    load_test_data,
    load_train_data,
)


class TestLoadTrainData:
    def test_loads_successfully(self):
        df = load_train_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert TARGET_COL in df.columns

    def test_has_expected_columns(self):
        df = load_train_data()
        expected = {"id", "age", "job", "marital", "education", "subscribe"}
        assert expected.issubset(set(df.columns))

    def test_raises_on_missing_target(self, tmp_path):
        bad_csv = tmp_path / "bad.csv"
        pd.DataFrame({"col1": [1, 2]}).to_csv(bad_csv, index=False)
        with pytest.raises(ValueError, match="缺少目标列"):
            load_train_data(bad_csv)


class TestLoadTestData:
    def test_loads_successfully(self):
        df = load_test_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert TARGET_COL not in df.columns

    def test_raises_when_target_present(self, tmp_path):
        bad_csv = tmp_path / "bad.csv"
        pd.DataFrame({"col1": [1], TARGET_COL: ["yes"]}).to_csv(bad_csv, index=False)
        with pytest.raises(ValueError, match="不应包含目标列"):
            load_test_data(bad_csv)


class TestGetColumns:
    def test_feature_columns_exclude_id_and_target(self):
        df = load_train_data()
        features = get_feature_columns(df)
        assert "id" not in features
        assert TARGET_COL not in features

    def test_categorical_columns(self):
        df = load_train_data()
        cat_cols = get_categorical_columns(df)
        assert "job" in cat_cols
        assert "marital" in cat_cols
        assert TARGET_COL not in cat_cols

    def test_numerical_columns(self):
        df = load_train_data()
        num_cols = get_numerical_columns(df)
        assert "age" in num_cols
        assert "duration" in num_cols
