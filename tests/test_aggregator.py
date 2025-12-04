import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import multiprocessing
from app.aggregator.metrics_aggregator import MetricsAggregator


def test_aggregator_merges_metrics():
    # Create queue [multiprocessing.Queue()] because this type of queue is applicable only in multiprocessing concept
    result_queue = multiprocessing.Queue()
    worker_count = 2

    ## metrics-aggreator process instances is created and it will start reading generated metrics from each worker
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    agg = MetricsAggregator(result_queue, worker_count, shared_dict)
    agg.start()

    # Worker-1 metrics-result stored into result-queue
    result_queue.put({
        "total_requests": 2,
        "status_counts": {200: 2},
        "ip_counts": {"ip1": 2},
        "url_counts": {"/a": 2},
    })

    # Worker-2 metrics-result stored into result-queue
    result_queue.put({
        "total_requests": 3,
        "status_counts": {404: 1, 200: 2},
        "ip_counts": {"ip2": 3},
        "url_counts": {"/b": 3},
    })

    # Stop signals
    result_queue.put(None)
    result_queue.put(None)

    agg.join()

    final = agg.get_final_metrics()
    print(f"final-metrics: {final}\n")

    assert final["total_requests"] == 5
    assert final["status_counts"][200] == 4
    assert final["status_counts"][404] == 1
    assert final["ip_counts"]["ip1"] == 2
    assert final["ip_counts"]["ip2"] == 3
    assert final["url_counts"]["/a"] == 2
    assert final["url_counts"]["/b"] == 3
