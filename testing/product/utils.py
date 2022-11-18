import base64
from dataclasses import dataclass
from typing import Optional
from faker.providers import BaseProvider
from faker import Faker
import random as rd

class Product():
    def __init__(self,*args):
        self.name = args[0] + args[1]
        self.item = '件'
        self.desc = '这是一'+self.item+self.name+'，特点：'+args[0]

class ProductProvider(BaseProvider):
    attr = ['现代化','轻便','厚重','巨大','灵巧','高级','中级','普通','初级','科技感','少女感']
    prod = '服装、鞋、帽、袜子、手套、围巾、领带、配饰、包、伞、蛋、水产品、菜、调味品、糖、茶及饮料、干鲜瓜果、糕点饼干、液体乳及乳制品、在外用膳食品及其他食品'.split('、')

    def product(self):
        return Product(rd.choice(ProductProvider.attr),rd.choice(ProductProvider.prod))

faker = Faker(locale='zh_CN')
faker.add_provider(ProductProvider)


url = 'http://localhost:8080/product'
