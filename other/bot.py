#!/usr/bin/env python3

import os
import sys
import random
import string
import requests

from randomtimestamp import randomtimestamp
from configparser import ConfigParser

# Set start dirs
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def start_bot():
    """
    Function for starting this bot
    """

    bot_config = ConfigParser()
    bot_config.read('config.ini')
    number_of_users = int(bot_config['MAIN']['number_of_users'])
    max_posts_per_user = int(bot_config['MAIN']['max_posts_per_user'])
    max_likes_per_user = int(bot_config['MAIN']['max_likes_per_user'])

    project_config = ConfigParser()
    project_config.read('../configs/main.ini')
    server_port = project_config['MAIN']['server_port']

    registration_url = f'http://localhost:{server_port}/api/registration/'
    login_url = f'http://localhost:{server_port}/api/login/'
    create_post_url = f'http://localhost:{server_port}/api/create_post/'
    like_url = f'http://localhost:{server_port}/api/like_post/'
    dislike_url = f'http://localhost:{server_port}/api/dislike_post/'

    users = list()
    number_of_posts = 0

    for __ in range(number_of_users):
        new_username = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        new_password = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        users.append({'username': new_username, 'password': new_password})

        requests.post(registration_url, data={'username': new_username, 'password': new_password})

        data = requests.post(login_url, data={'username': new_username, 'password': new_password}).json()
        access_token = data['data']['access_token']

        for _ in range(random.randint(0, max_posts_per_user)):
            title = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
            text = ''.join(random.choice(string.ascii_lowercase) for i in range(256))
            timestamp = int(randomtimestamp(2010, text=False).timestamp())

            requests.post(
                create_post_url,
                headers={'Authorization': f'Bearer {access_token}'},
                data={'title': title, 'text': text, 'timestamp': timestamp}
            )

            number_of_posts += 1

    for user in users:
        data = requests.post(login_url, data=user).json()
        access_token = data['data']['access_token']

        for _ in range(random.randint(0, max_likes_per_user)):
            like_type = random.choice(['like', 'dislike'])
            post_id = random.randint(1, number_of_posts)
            timestamp = int(randomtimestamp(2010, text=False).timestamp())

            if like_type == 'like':
                requests.post(
                    like_url,
                    headers={'Authorization': f'Bearer {access_token}'},
                    data={'post_id': post_id, 'timestamp': timestamp}
                )

            else:
                requests.post(
                    dislike_url,
                    headers={'Authorization': f'Bearer {access_token}'},
                    data={'post_id': post_id, 'timestamp': timestamp}
                )


if __name__ == '__main__':
    print('In progress...')
    start_bot()
    print('Done!')
