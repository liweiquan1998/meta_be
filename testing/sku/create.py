from testing.product.utils import *

import unittest
import requests
from faker import Faker

def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()

class TestIdCardOcr(unittest.TestCase):

    def test_test(self):
        faker = Faker(locale='zh_CN')
        example = {
                "product_id": faker.pyint(),
                "sku_attr": faker.pystr(),
                "sku_name": faker.pystr(),
                "price": faker.pyint(5,2000),
                "stock" : faker.pyint(1,100),
            }
        r = send_request(example)
        self.assertEqual(r['code'], 200, 'status should be 200')
