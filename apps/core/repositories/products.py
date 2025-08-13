from django.db import connection
from apps.core.models import Product


class ProductRepository:
    @staticmethod
    def create(data):
        product = Product.objects.create(**data)
        print(connection.queries[-1])
        return product
