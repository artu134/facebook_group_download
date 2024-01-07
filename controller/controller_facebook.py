from database.base_orm import BaseORM
from loader.facebook_loader import FacebookGroupScraper
from database.message import Message

class FacebookController: 
    '''
        Controller for the Facebook group scraper
    '''

    def __init__(self, scraper: FacebookGroupScraper, database: BaseORM, group_ids ) -> None:
        self.scraper = scraper
        self.database = database
        self.group_ids = group_ids

    def run_all(self):
        '''
            Get all the post from the group and add them to the database
        '''
        # Get all posts from the Facebook group
        self.load_groups_by_method(self.group_ids, self.scraper.get_all_posts)

    def load_groups_by_method(self, groups, action_to_load):
        for group_id in groups:
            posts = action_to_load([group_id]) # will take a very long time probably days
            for _, group_posts in posts.items():
                self.database.add(Message(id=group_posts['id'], group_id=group_id, message=group_posts['message'], language='est'))

    def run(self):
        '''
            Get first page of the post from the group and add them to the database
        '''
        # Get all posts from the Facebook group
        self.load_groups_by_method(self.group_ids, self.scraper.get_first_page_posts)