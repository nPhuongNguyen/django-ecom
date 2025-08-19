# --- Cấu hình logger ---
import logging

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
    if kwargs:
        message = f"{message} | {kwargs}"
    logger.info(f"{CYAN}{request_id}{RESET} | [{func_name}] | {message}")

