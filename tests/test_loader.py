import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import multiprocessing
from app.loader.log_loader import LogLoader

def test_loader_reads_batches(tmp_path, monkeypatch):
    """
    Replace log file path with a temporary file,
    then validate loader batching & stop signals.
    """

    # Create temporary file with 25 lines using inbuilt pytest-fixtures tmp_path
    # after test, tmp_path will be not automatically deleted
    print(f"tmp_path: {tmp_path}\n")
    temp_log = tmp_path / "temp_access.log"
    content = "\n".join([f"line {i}" for i in range(25)])
    temp_log.write_text(content)

    # Patch the LOG_FILE_PATH to point to this temporary file
    # monkeypatch by pytes and Override variables/functions safely during tests
    monkeypatch.setattr("app.loader.log_loader.LOG_FILE_PATH", temp_log)
    monkeypatch.setattr("app.loader.log_loader.BATCH_SIZE", 10)
    monkeypatch.setattr("app.loader.log_loader.WORKER_COUNT", 2)

    # Create queue [multiprocessing.Queue()] because this type of queue is applicable only in multiprocessing concept
    # it can be available/share in multiple process
    task_queue = multiprocessing.Queue()
    loader = LogLoader(task_queue)
    loader.start()
    loader.join()

    # Collect outputs and reading data from queue until is not empty
    outputs = []
    while not task_queue.empty():
        outputs.append(task_queue.get())

    # There should be 3 batches (10, 10, 5) + 2 stop signals
    print(f"outputs: {outputs}\n")
    batches = outputs[:-2]
    stops = outputs[-2:]

    assert len(batches) == 3
    assert len(batches[0]) == 10
    assert len(batches[1]) == 10
    assert len(batches[2]) == 5
    assert stops == [None, None]
