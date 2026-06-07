"""项目配置常量。"""

from pathlib import Path

# 路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"

# 目标列
TARGET_COL = "subscribe"

# 端口
APP_PORT = 8004
