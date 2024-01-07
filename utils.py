import configparser
from controller.controller_facebook import FacebookController
from database.base_orm import Base
from database.facebook_orm import FacebookORM
from loader.facebook_loader import FacebookGroupScraper



def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_controller(config, database):
    access_token = config['facebook']['access_token']
    batch_size = int(config['facebook']['batch_size'])
    # Load group IDs from config
    group_ids = config['facebook_groups']['group_ids'].split(',')

    # Initialize Facebook scraper and controller
    scraper = FacebookGroupScraper(access_token, batch_size)
    controller = FacebookController(scraper, database, group_ids)
    return controller

def create_database(config):
    db_url = config['database']['db_url']

    # Initialize database (creates it if it doesn't exist)
    database = FacebookORM(db_url)
    Base.metadata.create_all(database.engine)
    return database

def get_database(config):
    db_url = config['database']['db_url']

    # Initialize database (creates it if it doesn't exist)
    database = FacebookORM(db_url)
    return database
