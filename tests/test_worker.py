import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import multiprocessing
from app.workers.worker_process import WorkerProcess


def test_worker_computes_metrics():
    # Create queue [multiprocessing.Queue()] because this type of queue is applicable only in multiprocessing concept
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    # worker process instances
    worker = WorkerProcess(task_queue, result_queue, worker_id=1)
    worker.start()
    # adding task in queue manually. Right now one-batch have two lines of log only
    task_queue.put([
        '192.168.1.10 - - [10/Oct/2025:13:55:36 +0530] "GET /home HTTP/1.1" 200 532 0.123',
        '192.168.1.20 - - [10/Oct/2025:13:55:37 +0530] "GET /home HTTP/1.1" 404 120 0.234'
    ])
    # stop signal
    task_queue.put(None)  
    worker.join()
    # getting stored metrics result from another queue
    metrics = result_queue.get()
    print(f"\nmetrics: {metrics}\n")
    assert metrics["total_requests"] == 2
    assert metrics["status_counts"][200] == 1
    assert metrics["status_counts"][404] == 1
    assert metrics["ip_counts"]["192.168.1.10"] == 1
    assert metrics["url_counts"]["/home"] == 2
