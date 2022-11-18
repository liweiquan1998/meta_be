from testing.product.utils import *

import unittest
import requests
from testing.product.utils import faker


def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()

class TestProduct(unittest.TestCase):

    def test_test(self):
        for i in range(120):
            product = faker.product()
            example = {
                    "business_id": faker.pyint(50,100),
                    "unit": product.item,
                    "name": product.name,
                    "desc" : product.desc
                }
            r = send_request(example)
            self.assertEqual(r['code'], 200, 'status should be 200')

