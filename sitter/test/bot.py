from generators import content_gen, users_gen, get_config
from rest_framework import status
import concurrent.futures
from tqdm import tqdm
import requests
import time
import random
import os
import re

VOTES = [1, -1]
LOCAL_HOST = 'http://localhost:8000/'
CONFIG_PATH = './config.json'
MAX_WORKERS = os.cpu_count()

API_ENDPOINTS = dict(
    signup='user_signup/',
    login='user_login/',
    feed='network/',
    vote='network/vote/'
)

class Bot:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.localhost = LOCAL_HOST
        self.cookies = None
        self.csrftoken = None

    def signup(self, **kwargs):
        if not kwargs:
            kwargs = self.__dict__
        kwargs.update(
            dict(password1=self.password, password2=self.password))
        r = requests.post(
            url=f'{self.localhost}{API_ENDPOINTS.get("signup")}',
            data=kwargs
        )
        if r.status_code == status.HTTP_201_CREATED:
            self.cookies = r.cookies
            self.csrftoken = self.cookies.get('csrftoken')
        else:
            print('\nsignup went wrong')

    def login(self, **kwargs):
        if not kwargs:
            kwargs = self.__dict__
        kwargs = {key: kwargs[key] for key in ["username", "password"]}
        r = requests.post(
            url=f'{self.localhost}{API_ENDPOINTS.get("login")}',
            data=kwargs
        )
        if not r.status_code == status.HTTP_200_OK:
            print('\nlogin went wrong')

    def create_post(self, *args, **kwargs):
        content = content_gen(self.username)
        r = requests.post(
            url=f'{self.localhost}{API_ENDPOINTS.get("feed")}',
            data={
                'text': content,
                'username': self.username,
                'csrftoken': self.csrftoken
            },
            cookies=self.cookies,
        )
        if not r.status_code == status.HTTP_200_OK:
            print('\ncreating post went wrong')

    def mass_post_create(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(self.create_post, range(self.number_of_posts))

    def vote(self, post_id):
        r = requests.post(
            url=f'{self.localhost}{API_ENDPOINTS.get("vote")}{post_id}',
            data={
                'vote': random.choice(VOTES),
                'username': self.username,
                'post_id': post_id,
                'csrftoken': self.csrftoken
            },
            cookies=self.cookies,
        )

    def mass_vote(self):
        # Get post ids
        r = requests.get(f'{self.localhost}{API_ENDPOINTS.get("feed")}')
        if r.status_code == status.HTTP_200_OK:
            post_ids = [int(match.group(1)) for match in re.finditer(fr'{API_ENDPOINTS.get("vote")}(\d+)', r.text)]
            # Send like/dislike
            if self.number_of_likes > len(post_ids):
                self.number_of_likes = len(post_ids)
            vote_range = random.sample(post_ids, self.number_of_likes)
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.map(self.vote, vote_range)
        else:
            print('\nmass vote went wrong')


def main():
    config = get_config(CONFIG_PATH)
    users = users_gen(config)
    sleep_time = 3
    bots = []

    print('Creating bots and posting:')
    with tqdm(iterable=users) as process:
        for user in users:
            bot = Bot(**user)
            bot.signup()
            bot.mass_post_create()
            bots.append(bot)
            process.update()

    print('Voting:')
    with tqdm(iterable=users) as process:
        for bot in bots:
            bot.login()
            bot.mass_vote()
            time.sleep(sleep_time)
            process.update()


if __name__ == "__main__":
    main()
