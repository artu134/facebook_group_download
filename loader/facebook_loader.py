import logging
import re
import requests
import json
import time

class FacebookGroupScraper:
    def __init__(self, access_token, batch_size=100):
        self.access_token = access_token
        self.batch_size = batch_size

    def get_facebook_uri(self, group_id):
        return f"https://graph.facebook.com/v14.0/{group_id}/feed"

    def get_all_posts(self, group_ids, max_calls=150):
        all_posts = {}
        call_count = 0

        for group_id in group_ids:
            all_posts[group_id] = []
            params = {
                'limit': self.batch_size,
                'access_token': self.access_token
            }

            while call_count < max_calls:
                try:
                    response = requests.get(self.get_facebook_uri(group_id), params=params)
                    call_count += 1

                    if response.status_code == 200:
                        data = json.loads(response.content)
                        all_posts[group_id].extend(data['data'])

                        if 'paging' in data and 'next' in data['paging']:
                            params['after'] = data['paging']['cursors']['after']
                        else:
                            break
                    else:
                        response.raise_for_status()

                except requests.exceptions.HTTPError as err:
                    if response.status_code == 429:
                        logging.debug("Rate limit exceeded. Waiting to retry...")
                        time.sleep(3600)  # Wait for 1 hour
                        continue
                    else:
                        logging.debug(f"HTTP Error occurred: {err}")
                        break

                except Exception as e:
                    logging.debug(f"An error occurred: {e}")
                    break

            if call_count >= max_calls:
                logging.debug("Maximum calls reached, waiting for next hour.")
                time.sleep(3600)  # Wait for 1 hour
                call_count = 0

        return all_posts

    def get_first_page_posts(self, group_ids):
        first_page_posts = {}
        for group_id in group_ids:
            try:
                response = requests.get(
                    self.get_facebook_uri(group_id), 
                    params={'limit': self.batch_size, 'access_token': self.access_token}
                )

                if response.status_code == 200:
                    data = json.loads(response.content)
                    first_page_posts[group_id] = data['data']
                else:
                    response.raise_for_status()

            except Exception as e:
                logging.debug(f"An error occurred while fetching first page posts for group {group_id}: {e}")

        return first_page_posts

    def filter_messages(self, messages, regex_patterns):
        filtered_messages = []
        for message in messages:
            for pattern in regex_patterns:
                if re.search(pattern, message['message']):
                    filtered_messages.append(message)
                    break
        return filtered_messages