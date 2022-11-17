from testing.customer.utils import *

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
            "password": faker.password(),
            "tel_phone": faker.phone_number(),
            "email_address": faker.email()}
        r = send_request(example)
        self.assertEqual(r['code'], 200, 'status should be 200')
