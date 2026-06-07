"""Streamlit 应用基本测试（非 E2E，仅验证导入和模块加载）。"""


def test_app_module_imports():
    """验证 app 模块可以被导入（不执行 Streamlit 渲染）。"""
    import src.app

    assert hasattr(src.app, "st")


def test_data_loader_imports():
    """验证 data_loader 模块可以被导入。"""
    import src.data_loader

    assert hasattr(src.data_loader, "load_train_data")


def test_analysis_imports():
    """验证 analysis 模块可以被导入。"""
    import src.analysis

    assert hasattr(src.analysis, "data_overview")


def test_model_imports():
    """验证 model 模块可以被导入。"""
    import src.model

    assert hasattr(src.model, "train_model")


def test_config_imports():
    """验证 config 模块可以被导入。"""
    import src.config

    assert hasattr(src.config, "APP_PORT")
    assert src.config.APP_PORT == 8004
