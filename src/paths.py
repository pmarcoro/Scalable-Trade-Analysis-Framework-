# src/config.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"
RAW_PATH_EXP_STRUCTURE = RAW_PATH / "export structure"
