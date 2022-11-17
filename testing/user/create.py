from tqdm import tqdm

from testing.user.utils import *

import unittest
import requests
from faker import Faker

def send_request(data):
    r = requests.post(f'{url}/create', json=data)
    print(r.json())
    return r.json()

class TestIdCardOcr(unittest.TestCase):

    def test_test(self):
        faker = Faker(locale='zh_CN')
        example = {
            "username": faker.name(),
            "password_hash": faker.password(),
            "tel_phone": faker.phone_number(),
            "email_address": faker.email(),
            "storename": f"{faker.company_prefix()}元宇宙旗舰店",}
        r = send_request(example)
        self.assertEqual(r['code'], 200, 'status should be 200')

# if __name__ == '__main__':
#     for _ in tqdm(range(50)):
#         faker = Faker(locale='zh_CN')
#         example = {
#             "username": faker.name(),
#             "password_hash": faker.password(),
#             "tel_phone": faker.phone_number(),
#             "email_address": faker.email(),
#             "storename": f"{faker.company_prefix()}元宇宙旗舰店", }
#         r = send_request(example)