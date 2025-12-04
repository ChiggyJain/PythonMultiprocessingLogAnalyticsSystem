
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    """
    Represents a parsed log entry from Apache/Nginx access logs.
    """
    ip: str
    timestamp: str
    method: str
    url: str
    protocol: str
    status: int
    size: int
    response_time: Optional[float] = None  # may not exist in all logs


@dataclass
class WorkerMetrics:
    """
    Represents the aggregated metrics computed by each worker.
    """
    total_requests: int
    status_counts: dict
    ip_counts: dict
    url_counts: dict

    def to_dict(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "status_counts": self.status_counts,
            "ip_counts": self.ip_counts,
            "url_counts": self.url_counts,
        }
