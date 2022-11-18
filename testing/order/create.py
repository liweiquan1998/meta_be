from testing.product.utils import *

import unittest
import requests
from faker import Faker

def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()

class TestOrder(unittest.TestCase):

    def test_test(self):
        faker = Faker(locale='zh_CN')
        example = {
                "business_id": faker.pyint(),
                "create_time": faker.unix_time(start_datetime="-7d",end_datetime="now"),
                "unit": "件",
                "name": faker.license_plate(),
                "meta_obj_id": faker.pyint(),
                "desc" : faker.pystr()
            }
        r = send_request(example)
        self.assertEqual(r['code'], 200, 'status should be 200')
