import logging

from utils import get_config, create_database, get_controller


# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("log.txt", mode="w"), 
                              logging.StreamHandler()])
def main():
    config = get_config()

    # Database configuration
    database = create_database(config)

    # Facebook scraper configuration
    controller = get_controller(config, database)


    # Run the process
    controller.run_all()  # To get all posts
    # controller.run()  # To get only the first page of posts

if __name__ == "__main__":
    main()
