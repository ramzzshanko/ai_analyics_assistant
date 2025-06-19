import logging
import os
import sys
from dotenv import load_dotenv, find_dotenv

from app.database.load_data_sources import load_dummy_loan_dataframes
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import duckdb
import threading
import time

# Stream handler for console output
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# File handler for logging to a file
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

load_dotenv(find_dotenv(), override=True)

def refresh_omari_loan_data():
    logger.info("Loading OMari loan dataframes")
    omari_loan_data = load_dummy_loan_dataframes()
    logger.info(f"Loaded {len(omari_loan_data)} dataframes from OMari loan data")
    for table_name, df in omari_loan_data.items():
        logger.info(f"Register {table_name} into DuckDB")
        db_conn.register(table_name, df)
        logger.info(f"Registered {len(df)} rows into {table_name}")

def periodic_refresh(interval_seconds=3600):
    while True:
        refresh_omari_loan_data()
        time.sleep(interval_seconds)

logger.info("Creating DuckDB connection")
db_conn = duckdb.connect(database='data/app.db', read_only=False)

# Initial load
refresh_omari_loan_data()

# Start background thread for periodic refresh
refresh_thread = threading.Thread(target=periodic_refresh, args=(int(os.getenv("DATA_REFRESH_INTERVAL")),), daemon=True)
refresh_thread.start()