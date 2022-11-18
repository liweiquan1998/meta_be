from faker.providers import BaseProvider
from faker import Faker
import random as rd

class Sku():
    def __init__(self,*args):
        self.attr = '类型：'+args[0] + '尺寸大小:'+args[1]+'颜色：'+args[2]
        self.name = args[0] + args[1] + args[2]
        self.price = rd.randint(1,100) + round(rd.random(),1)
        self.stock = rd.randint(100,1000)
        self.product_id = rd.randint(2,200)

class SkuProvider(BaseProvider):
    attr = ['类型1','类型2','类型3','A型','B型','C型']
    attr2 = ['小号','中号','大号']
    attr3 = '红色 白色 绿色 紫色 黄色 青色 灰色 五颜六色'.split()

    def sku(self) -> Sku:
        return Sku(rd.choice(SkuProvider.attr),rd.choice(SkuProvider.attr2),rd.choice(SkuProvider.attr3))

faker = Faker(locale='zh_CN')
faker.add_provider(SkuProvider)

url = 'http://localhost:8080/sku'
