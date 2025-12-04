import logging
from pathlib import Path
from multiprocessing import Queue
from .config import (
    BASE_DIR,
    LOGS_DIR,
    OUTPUT_DIR,
    LOG_FILE_PATH,
    CPU_COUNT,
    WORKER_COUNT,
    BATCH_SIZE,
    REPORT_FILE,
)
from app.loader.log_loader import LogLoader


def setup_logging() -> None:
    """Configure basic logging for the project."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(processName)s - %(message)s",
    )


def ensure_directories() -> None:
    """Ensure required directories exist."""
    for path in [LOGS_DIR, OUTPUT_DIR]:
        Path(path).mkdir(parents=True, exist_ok=True)


def print_environment_summary() -> None:
    """Print a quick summary of the environment & config."""
    logging.info("🔧 Python Multiprocessing Log Analytics System")
    logging.info(f"📁 Base directory     : {BASE_DIR}")
    logging.info(f"📁 Logs directory     : {LOGS_DIR}")
    logging.info(f"📁 Output directory   : {OUTPUT_DIR}")
    logging.info(f"📄 Log file path      : {LOG_FILE_PATH}")
    logging.info(f"📄 Report file        : {REPORT_FILE}")
    logging.info(f"🧠 CPU cores detected : {CPU_COUNT}")
    logging.info(f"👷 Worker processes   : {WORKER_COUNT}")
    logging.info(f"📦 Batch size (lines) : {BATCH_SIZE}")


def main() -> None:
    setup_logging()
    ensure_directories()
    print_environment_summary()
    logging.info("✅ Project skeleton initialized successfully.")

    # Create queue [multiprocessing.Queue()] because this type of queue is applicable only in multiprocessing concept
    # it can be available/share in multiple process
    task_queue = Queue()
    loader = LogLoader(task_queue)
    loader.start()
    loader.join()

    # Collect outputs and reading data from queue until is not empty
    outputs = []
    while not task_queue.empty():
        outputs.append(task_queue.get())

    # There should be 3 batches (10, 10, 5) + 2 stop signals
    print(f"outputs: {outputs}\n")
    

if __name__ == "__main__":
    main()
