from testing.order.utils import url
import random as rd
import unittest
import requests
from faker import Faker

def send_request(data):
    r = requests.post(f'{url}/', json=data)
    print(r.json())
    return r.json()

class TestOrder(unittest.TestCase):

    def test_test(self):
        for i in range(10):
            faker = Faker(locale='zh_CN')
            example = {
                      "sku_list": "[{\"sku_id\":461,\"num\":%s},{\"sku_id\":460,\"num\":%s}]"%(rd.randint(1,5),rd.randint(1,5)),
                      "pay_count": 3,
                      "business_id": 60,
                      "customer_id": 27,
                      "receiver_phone": "18181689437",
                      "deliver_address": "青海省郑州市沙市西安路E座 926178",
                      "logistic_order_id": 0,
                      "receiver_address": "河南省齐齐哈尔市西峰许街C座 722951",
                      "receiver_name": "邓婷婷"
                    }
            r = send_request(example)
            self.assertEqual(r['code'], 200, 'status should be 200')
