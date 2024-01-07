import logging
import datetime
from utils import get_config, get_controller, get_database

def get_timestamped_log_filename(base="log_weekly.log"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}"

# Configure logging
log_filename = get_timestamped_log_filename()
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler(log_filename, mode="w"), 
                              logging.StreamHandler()])

def main():
    logging.info("Script started.")

    config = get_config()
    database = get_database(config)

    # Facebook scraper configuration
    controller = get_controller(config, database)

    controller.run()  # To get first posts weekly

    logging.info("Script completed successfully.")

if __name__ == "__main__":
    main()
