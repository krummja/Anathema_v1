from __future__ import annotations
from typing import Any, Dict, Optional


class Config:

    def __init__(self, conf: Dict[str, Any]):
        self._config = conf

    def get_property(self, property_name) -> Optional[Any]:
        return self._config[property_name]