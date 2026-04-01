from pathlib import Path
import sys


def get_app_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = get_app_base_dir()
DATA_DIR = APP_DIR / "SalesData"
DATA_DIR.mkdir(exist_ok=True)