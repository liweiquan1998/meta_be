import random
import requests
from faker import Faker

url = 'http://192.168.199.27:50003/live_account'


def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()


def create():  # sourcery skip: remove-redundant-slice-index
    faker = Faker(locale='zh_CN')
    example = {
        "name": faker.name(),
        "address": faker.uri(),
        "platform": random.choice(['抖音', 'B站', '虎牙', '斗鱼']),
        "key": faker.md5()[0:10],
        "token": faker.md5()[0:10],
        "creator_id": faker.pyint(5, 10)
    }
    send_request(example)


if __name__ == '__main__':
    for _ in range(10):
        create()
