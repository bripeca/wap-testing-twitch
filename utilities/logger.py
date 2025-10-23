import logging
import os
import sys
from datetime import datetime
from pathlib import Path


# basic logger utility to troubleshoot if needed
def get_logger(name="tests"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers when called repeatedly

    logger.setLevel(logging.INFO)

    # Resolve project root
    project_root = Path(__file__).resolve().parents[1]

    # Create a logs and use that folder in root directory
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Separate file per worker if running with multiple workers
    worker = os.getenv("PYTEST_XDIST_WORKER", "main")
    log_file = log_dir / f"{worker}.log"

    filehandler = logging.FileHandler(log_file, encoding="utf-8")
    filehandler.setLevel(logging.INFO)

    # console handler
    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    filehandler.setFormatter(formatter)
    streamhandler.setFormatter(formatter)

    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)

    # divider after each run to make it easier to distinguish between scripts
    divider = "=" * 60
    logger.info(divider)
    logger.info("New Test Script started at %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(divider)

    return logger
