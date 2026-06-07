"""模型训练、保存、加载与预测。"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.config import MODELS_DIR, TARGET_COL
from src.data_loader import get_categorical_columns, get_feature_columns

MODEL_PATH = MODELS_DIR / "model.joblib"
ENCODERS_PATH = MODELS_DIR / "encoders.joblib"


def _encode_features(
    df: pd.DataFrame, encoders: dict[str, LabelEncoder] | None = None, fit: bool = False
) -> tuple[pd.DataFrame, dict[str, LabelEncoder]]:
    """对分类特征进行 LabelEncoder 编码。返回 (编码后 DataFrame, encoders 字典)。"""
    df = df.copy()
    cat_cols = get_categorical_columns(df)
    if encoders is None:
        encoders = {}
    for col in cat_cols:
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            if col not in encoders:
                raise ValueError(f"缺少列 '{col}' 的编码器")
            df[col] = encoders[col].transform(df[col].astype(str))
    return df, encoders


def train_model(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[GradientBoostingClassifier, dict]:
    """训练模型，返回 (模型, 评估指标字典)。"""
    feature_cols = get_feature_columns(df)
    X = df[feature_cols].copy()
    y = (df[TARGET_COL] == "yes").astype(int)

    X_encoded, encoders = _encode_features(X, fit=True)

    X_train, X_val, y_train, y_val = train_test_split(
        X_encoded, y, test_size=test_size, random_state=random_state, stratify=y
    )

    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=random_state,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred),
        "f1": f1_score(y_val, y_pred),
        "auc": roc_auc_score(y_val, y_proba),
    }

    # 保存模型和编码器
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)

    return model, metrics


def load_model(
    model_path: Path | str | None = None,
    encoders_path: Path | str | None = None,
) -> tuple[GradientBoostingClassifier, dict[str, LabelEncoder]]:
    """加载已保存的模型和编码器。"""
    mp = model_path or MODEL_PATH
    ep = encoders_path or ENCODERS_PATH
    model = joblib.load(mp)
    encoders = joblib.load(ep)
    return model, encoders


def predict(
    model: GradientBoostingClassifier,
    encoders: dict[str, LabelEncoder],
    input_df: pd.DataFrame,
) -> dict:
    """预测输入数据，返回 {"prediction": "yes"/"no", "probability": float}。"""
    df_encoded, _ = _encode_features(input_df, encoders=encoders, fit=False)
    proba = model.predict_proba(df_encoded)[:, 1]
    pred = model.predict(df_encoded)
    return {
        "prediction": "yes" if pred[0] == 1 else "no",
        "probability": float(np.round(proba[0], 4)),
    }
