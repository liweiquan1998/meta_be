import random
import requests
from faker import Faker

url = 'http://192.168.199.27:50003/live_streaming'


def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()


def create():  # sourcery skip: remove-redundant-slice-index
    faker = Faker(locale='zh_CN')
    example = {
                "name": faker.name(),
                "address": faker.uri(),
                "status": 0,
                "work_space": faker.md5()[0:10],
                "virtual_human_id": faker.pyint(5, 10),
                "special_effects_id": faker.pyint(5, 10),
                "background_id": faker.pyint(5, 10),
                "creator_id": faker.pyint(5, 10),
                "live_account_id": faker.pyint(5, 10)
                }
    send_request(example)


if __name__ == '__main__':
    for _ in range(10):
        create()
