import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.utils.parsers import parse_log_line
from app.shared.schemas import LogEntry


def test_parse_valid_log():
    line = '192.168.1.10 - - [10/Oct/2025:13:55:36 +0530] "GET /home HTTP/1.1" 200 532 0.123'
    entry = parse_log_line(line)
    assert isinstance(entry, LogEntry)
    assert entry.ip == "192.168.1.10"
    assert entry.method == "GET"
    assert entry.url == "/home"
    assert entry.status == 200
    assert entry.size == 532
    assert entry.response_time == 0.123


def test_parse_invalid_log():
    line = "INVALID LOG LINE"
    entry = parse_log_line(line)
    assert entry is None
