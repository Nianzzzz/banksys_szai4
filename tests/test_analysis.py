"""数据分析模块测试。"""

import pandas as pd

from src.analysis import (
    correlation_matrix,
    data_overview,
    group_conversion_rate,
    target_distribution,
    value_counts,
)
from src.data_loader import load_train_data


class TestDataOverview:
    def test_returns_dict_with_expected_keys(self):
        df = load_train_data()
        result = data_overview(df)
        assert "rows" in result
        assert "cols" in result
        assert "dtypes" in result
        assert "missing" in result
        assert "missing_pct" in result

    def test_row_count_matches(self):
        df = load_train_data()
        result = data_overview(df)
        assert result["rows"] == len(df)

    def test_col_count_matches(self):
        df = load_train_data()
        result = data_overview(df)
        assert result["cols"] == len(df.columns)


class TestValueCounts:
    def test_returns_series(self):
        df = load_train_data()
        result = value_counts(df, "job")
        assert isinstance(result, pd.Series)
        assert len(result) > 0


class TestCorrelationMatrix:
    def test_returns_square_matrix(self):
        df = load_train_data()
        corr = correlation_matrix(df)
        assert corr.shape[0] == corr.shape[1]

    def test_diagonal_is_one(self):
        df = load_train_data()
        corr = correlation_matrix(df)
        for i in range(len(corr)):
            assert abs(corr.iloc[i, i] - 1.0) < 1e-10


class TestGroupConversionRate:
    def test_returns_dataframe(self):
        df = load_train_data()
        result = group_conversion_rate(df, "job")
        assert isinstance(result, pd.DataFrame)
        assert "conversion_rate" in result.columns

    def test_values_between_0_and_1(self):
        df = load_train_data()
        result = group_conversion_rate(df, "job")
        assert (result["conversion_rate"] >= 0).all()
        assert (result["conversion_rate"] <= 1).all()


class TestTargetDistribution:
    def test_returns_series(self):
        df = load_train_data()
        result = target_distribution(df)
        assert isinstance(result, pd.Series)
        assert "yes" in result.index
        assert "no" in result.index
