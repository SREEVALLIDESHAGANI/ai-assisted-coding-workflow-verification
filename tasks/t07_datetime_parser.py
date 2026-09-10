# Task 7: Robust Datetime ISO Parser
from datetime import datetime, timezone
import re

def parse_iso_datetime(dt_str: str) -> datetime:
    # Normalize trailing Z
    dt_str = dt_str.strip()
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(dt_str)
    except Exception as e:
        raise ValueError(f"Invalid ISO datetime string '{dt_str}': {e}")
