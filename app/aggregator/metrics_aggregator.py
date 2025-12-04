import logging
from multiprocessing import Process, Queue

# this class is inherit from inbuilt python process class
class MetricsAggregator(Process):
    """
    Aggregator receives partial metrics from workers via result_queue,
    merges them, and stores global metrics for final reporting.
    """

    ## constructor
    def __init__(self, result_queue: Queue, worker_count: int):
        super().__init__(name="MetricsAggregator")
        self.result_queue = result_queue
        self.worker_count = worker_count
        self.total_requests = 0
        self.status_counts = {}
        self.ip_counts = {}
        self.url_counts = {}

    # defined own function
    def _merge_dict(self, target: dict, src: dict):
        """Merge count dictionaries."""
        for k, v in src.items():
            target[k] = target.get(k, 0) + v

    # defined own function
    def merge_metrics(self, m: dict):
        """Merge worker metric dict into global metrics."""
        self.total_requests += m["total_requests"]
        self._merge_dict(self.status_counts, m["status_counts"])
        self._merge_dict(self.ip_counts, m["ip_counts"])
        self._merge_dict(self.url_counts, m["url_counts"])

    # defined own function
    def get_final_metrics(self):
        return {
            "total_requests": self.total_requests,
            "status_counts": self.status_counts,
            "ip_counts": self.ip_counts,
            "url_counts": self.url_counts,
        }
    
    # inbuilt function of python process-class and override into this class
    def run(self):
        print("📊 Aggregator started.")
        logging.info("📊 Aggregator started.")
        stop_signals_received = 0
        # infinite loop until result-queue is not become empty OR all worker task is done and stopped immediately
        while True:
            event = self.result_queue.get()
            # STOP SIGNAL
            if event is None:
                stop_signals_received += 1
                logging.info(
                    f"🛑 Aggregator received stop signal "
                    f"({stop_signals_received}/{self.worker_count})"
                )
                if stop_signals_received == self.worker_count:
                    break
                continue
            # Normal metrics merge
            self.merge_metrics(event)
        logging.info("📈 Aggregator finished merging metrics.")
        logging.info(
            f"📌 Total Requests: {self.total_requests}, "
            f"Unique IPs: {len(self.ip_counts)}, "
            f"Unique URLs: {len(self.url_counts)}"
        )

    
