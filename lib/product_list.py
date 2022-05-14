from typing import List

from lib.geektime_api import GeekTimeApi


class ProductInfo:
    def __init__(self, productId: int, productTitle: str):
        self.productId = productId
        self.productTitle = productTitle


class ProductListGetter:
    def __init__(self):
        self.api = GeekTimeApi()

    def get_product_list(self) -> List[ProductInfo]:
        result = self.api.my_product_list()

        my_product_list = []

        for r in result:
            my_product_list.append(ProductInfo(r['id'], r['title']))

        return my_product_list
