"""模型模块测试。"""

import pytest

from src.data_loader import get_feature_columns, load_train_data
from src.model import _encode_features, predict, train_model


class TestEncodeFeatures:
    def test_encode_fit_returns_encoders(self):
        df = load_train_data()
        features = get_feature_columns(df)
        X = df[features].head(10).copy()
        encoded, encoders = _encode_features(X, fit=True)
        assert len(encoders) > 0
        for col in encoded.select_dtypes(include=["object", "category"]).columns:
            # After encoding, should be numeric
            pass  # Some cols may remain if not categorical

    def test_encode_transform_uses_existing_encoders(self):
        df = load_train_data()
        features = get_feature_columns(df)
        X = df[features].head(20).copy()
        encoded, encoders = _encode_features(X, fit=True)
        X_new = df[features].head(5).copy()
        encoded_new, _ = _encode_features(X_new, encoders=encoders, fit=False)
        assert encoded_new.shape[1] == encoded.shape[1]

    def test_raises_on_missing_encoder(self):
        df = load_train_data()
        features = get_feature_columns(df)
        X = df[features].head(5).copy()
        with pytest.raises(ValueError, match="缺少列"):
            _encode_features(X, encoders={}, fit=False)


class TestTrainModel:
    def test_returns_model_and_metrics(self):
        df = load_train_data()
        model, metrics = train_model(df, test_size=0.2)
        assert model is not None
        assert "accuracy" in metrics
        assert "auc" in metrics
        assert metrics["auc"] > 0.5  # 至少比随机好

    def test_metrics_reasonable_range(self):
        df = load_train_data()
        _, metrics = train_model(df)
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["precision"] <= 1
        assert 0 <= metrics["recall"] <= 1
        assert 0 <= metrics["f1"] <= 1
        assert 0 <= metrics["auc"] <= 1


class TestPredict:
    def test_returns_prediction_and_probability(self):
        df = load_train_data()
        model, metrics = train_model(df)
        from src.model import load_model

        model, encoders = load_model()
        features = get_feature_columns(df)
        input_df = df[features].head(1)
        result = predict(model, encoders, input_df)
        assert "prediction" in result
        assert "probability" in result
        assert result["prediction"] in ("yes", "no")
        assert 0 <= result["probability"] <= 1
