# --- Cấu hình logger ---
import logging
from apps.logging.kibana_log import *
logger = logging.getLogger("ecom_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# ANSI màu cho console
CYAN = "\033[96m"
RESET = "\033[0m"

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)

# --- Hàm log ---
def log_info(request_id, func_name, message, **kwargs):
    logger.info(f"{CYAN}{request_id}{RESET} | [{func_name}] | {message} | {kwargs}")
    # send_log_to_kibana(request_id= request_id,level= func_name, msg=message, metadata=kwargs)

