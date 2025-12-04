
import logging
from multiprocessing import Process, Queue
from typing import List
from app.config import (
    BASE_DIR,
    LOGS_DIR,
    OUTPUT_DIR,
    LOG_FILE_PATH,
    CPU_COUNT,
    WORKER_COUNT,
    BATCH_SIZE,
    REPORT_FILE
)

# this class is inherit from inbuilt python process class
class LogLoader(Process):
    """
    The LogLoader reads the log file in batches and pushes batches to the task_queue.
    """

    ## constructor
    def __init__(self, task_queue: Queue):
        super().__init__(name="LogLoader")
        self.task_queue = task_queue

    # defined own function
    def read_in_batches(self, batch_size: int):
        """
        Generator: Reads the log file in streaming mode and yields batches of lines.
        """
        batch = []
        with open(LOG_FILE_PATH, "r") as f:
            for line in f:
                batch.append(line.rstrip("\n"))
                if len(batch) >= batch_size:
                    # returning the respective batch
                    yield batch
                    batch = []
        # returning remaining lines
        if batch:
            yield batch

    # inbuilt function of python process-class and override into this class
    def run(self):
        logging.info(f"📥 Loader started. Reading logs from: {LOG_FILE_PATH}")
        # reading each batch and sending into task queue
        for batch in self.read_in_batches(BATCH_SIZE):
            self.task_queue.put(batch)
            logging.info(f"📦 Loader pushed batch of size: {len(batch)}")
        # Send STOP signals to all worker processes
        for _ in range(WORKER_COUNT):
            self.task_queue.put(None)
        logging.info("🛑 Loader finished sending all batches & stop signals.")
