from __future__ import annotations
from typing import *
import os
import json


ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, "_assets")
CONTENT_DIR = os.path.join(ROOT_DIR, "content")


def get_data(path: str) -> str:
    assert os.path.exists(ASSET_DIR), f"Cannot find asset path: {ASSET_DIR}"
    return os.path.join(ASSET_DIR, path)
