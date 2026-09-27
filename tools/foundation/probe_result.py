from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ProbeResult:
    status: Literal["PASS", "FAIL", "BLOCKED_DEP"]
    command: list[str]
    reason: str
    artifact: str | None = None
