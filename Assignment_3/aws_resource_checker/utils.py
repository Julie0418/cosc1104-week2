import json
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(message, level="INFO"):
    """
    Logs a message with the given severity level.
    """
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)

def save_report(data, filepath):
    """
    Saves the compliance check results to a JSON file.
    Creates the directory if it doesn't exist.
    """
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        log_message(f"Report saved to {filepath}")
    except Exception as e:
        log_message(f"Failed to save report: {e}", level="ERROR")
