from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class CheckResult:
    success: bool
    data: Optional[Any] = None
