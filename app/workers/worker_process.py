import logging
from multiprocessing import Process, Queue
from app.utils.parsers import parse_log_line
from app.shared.schemas import WorkerMetrics

# this class is inherit from inbuilt python process class
class WorkerProcess(Process):
    """
    Worker receives log batches from task_queue,
    computes metrics, and pushes results to result_queue.
    """

    ## constructor
    def __init__(self, task_queue: Queue, result_queue: Queue, worker_id: int):
        super().__init__(name=f"Worker-{worker_id}")
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.worker_id = worker_id

    # defined own function
    def compute_metrics(self, batch):
        """Compute metrics for a batch of log lines."""
        total_requests = 0
        status_counts = {}
        ip_counts = {}
        url_counts = {}
        # iterating each line in given batch
        for line in batch:
            # getting info in dict-form-human-readble of given line
            entry = parse_log_line(line)
            if entry is None:
                # skip invalid lines
                continue
            total_requests += 1
            # Count status code
            status_counts[entry.status] = status_counts.get(entry.status, 0) + 1
            # Count IPs
            ip_counts[entry.ip] = ip_counts.get(entry.ip, 0) + 1
            # Count URLs
            url_counts[entry.url] = url_counts.get(entry.url, 0) + 1
        return WorkerMetrics(
            total_requests=total_requests,
            status_counts=status_counts,
            ip_counts=ip_counts,
            url_counts=url_counts,
        )

    # inbuilt function of python process-class and override into this class
    def run(self):
        logging.info(f"👷 Worker-{self.worker_id} started.")
        # infinte loop until queue is not empty
        while True:
            batch = self.task_queue.get()
            if batch is None:
                logging.info(f"🛑 Worker-{self.worker_id} received stop signal.")
                break
            # generating metrics of given respective batch and respective contains list of lines
            metrics = self.compute_metrics(batch)
            # storing generated metrics in another multiprocessing queue
            self.result_queue.put(metrics.to_dict())
            logging.info(
                f"📤 Worker-{self.worker_id} processed batch: "
                f"{metrics.total_requests} requests found."
            )
        logging.info(f"👋 Worker-{self.worker_id} exiting.")
