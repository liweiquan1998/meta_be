import unittest
import requests
from testing.sku.utils import *
from app.models.product import Product as Product_model
from app.models.database import SessionLocal
db = SessionLocal()

def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()

class TestIdCardOcr(unittest.TestCase):

    def test_test(self):
        for i in range(300):
            item = faker.sku()
            item.name += db.query(Product_model).filter(Product_model.id==item.product_id).first().name
            example = {
                    "product_id": item.product_id,
                    "sku_attr": item.attr,
                    "sku_name": item.name,
                    "price": item.price,
                    "stock": item.stock,
                }
            print(example)
            r = send_request(example)
            self.assertEqual(r['code'], 200, 'status should be 200')
