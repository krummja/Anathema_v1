from __future__ import annotations
from typing import Dict, Any

from dataclasses import dataclass


@dataclass
class EventData:
    # Did the Action succeed?
    success: bool = False
    done: bool = False
    # What does the Action require?
    require: Dict[str, Any] = None
    # What can I expect back from its completion?
    expect: Dict[str, Any] = None
    # Additional useful data to do something with
    result: Dict[str, Any] = None
