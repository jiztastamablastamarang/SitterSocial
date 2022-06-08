import concurrent.futures
import json
import requests
import random
import names
import os
import secrets

GENDER = [
    'female',
    'male',
]

DEEP_AI_API_KEY = 'c3df3049-02c2-4513-b93d-4e95033e2b6b'


def get_config(path='config.json'):
    with open(path, 'r') as f:
        data = json.load(f)
    if isinstance(data, dict):
        return {key: int(value) for (key, value) in data.items()}
    else:
        print('error loading config')
        return {}


def content_gen(trigger):
    r = requests.post(
        'https://api.deepai.org/api/text-generator',
        data={
            'text': trigger,
        },
        headers={'api-key': DEEP_AI_API_KEY}
    )
    if r.status_code == 200:
        return r.json()['output']
    else:
        return 'error loading content from DeepAI'


def password_gen(nbytes=16):
    return secrets.token_urlsafe(nbytes)


def credentials_gen(*args, **kwargs):
    data = dict()
    data['gender'] = random.choice(GENDER)
    data['username'] = names.get_full_name(gender=data['gender'])
    data['email'] = '@'.join(data['username'].split()).lower() + '.com'
    data['password'] = password_gen()
    return data


def randint(number):
    return random.randint(1, number)


def users_gen(config):
    user_range = range(config.get('number_of_users'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 5) as executor:
        results = executor.map(credentials_gen, user_range)
    users = []
    for result in results:
        user = dict(
            number_of_likes=randint(config.get('max_likes_per_user')),
            number_of_posts=randint(config.get('max_posts_per_user'))
        )
        user.update(result)
        users.append(user)
    return users
