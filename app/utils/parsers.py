import re
from typing import Optional
from app.shared.schemas import LogEntry

# Real Apache log regex
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '             # IP Address
    r'\S+ \S+ '                 # Ident & user (ignored)
    r'\[(?P<timestamp>.*?)\] '  # Timestamp
    r'"(?P<method>\S+) '        # HTTP Method
    r'(?P<url>\S+) '            # URL
    r'(?P<protocol>[^"]+)" '    # Protocol
    r'(?P<status>\d{3}) '       # Status Code
    r'(?P<size>\S+)'            # Response size
    r'(?: (?P<response_time>[\d.]+))?'  # Optional response time
)


def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single Apache/Nginx access log line.
    Returns LogEntry or None if the line is malformed.
    """
    match = LOG_PATTERN.match(line)
    # print(f"match: {match}\n")
    if not match:
        return None
    data = match.groupdict()
    return LogEntry(
        ip=data["ip"],
        timestamp=data["timestamp"],
        method=data["method"],
        url=data["url"],
        protocol=data["protocol"],
        status=int(data["status"]),
        size=int(data["size"]) if data["size"] != "-" else 0,
        response_time=float(data["response_time"]) if data["response_time"] else None,
    )
