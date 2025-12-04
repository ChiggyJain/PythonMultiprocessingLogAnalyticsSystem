import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import multiprocessing
from app.loader.log_loader import LogLoader
from app.config import BATCH_SIZE, WORKER_COUNT, LOG_FILE_PATH


def test_loader_reads_batches(tmp_path, monkeypatch):
    """
    Replace log file path with a temporary file,
    then validate loader batching & stop signals.
    """

    # Create temporary file with 25 lines
    temp_log = tmp_path / "temp_access.log"
    content = "\n".join([f"line {i}" for i in range(25)])
    temp_log.write_text(content)

    # Patch the LOG_FILE_PATH to point to this temporary file
    monkeypatch.setattr("app.loader.log_loader.LOG_FILE_PATH", temp_log)

    # Create queue
    task_queue = multiprocessing.Queue()

    # Create loader with smaller batch size for test
    monkeypatch.setattr("app.loader.log_loader.BATCH_SIZE", 10)
    monkeypatch.setattr("app.loader.log_loader.WORKER_COUNT", 2)

    loader = LogLoader(task_queue)
    loader.start()
    loader.join()

    # Collect outputs
    outputs = []
    while not task_queue.empty():
        outputs.append(task_queue.get())

    # There should be 3 batches (10, 10, 5) + 2 stop signals
    batches = outputs[:-2]
    stops = outputs[-2:]

    assert len(batches) == 3
    assert len(batches[0]) == 10
    assert len(batches[1]) == 10
    assert len(batches[2]) == 5

    assert stops == [None, None]
