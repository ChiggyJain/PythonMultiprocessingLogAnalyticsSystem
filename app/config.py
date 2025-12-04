from pathlib import Path
import multiprocessing

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "sample_logs"
OUTPUT_DIR = BASE_DIR / "output"

# Log file to process
LOG_FILE_PATH = LOGS_DIR / "access.log"

# Number of worker processes (default: CPU cores)
CPU_COUNT = multiprocessing.cpu_count()
WORKER_COUNT = CPU_COUNT

# Batch size: how many log lines per task
BATCH_SIZE = 10_000

# Output file
REPORT_FILE = OUTPUT_DIR / "report.json"
