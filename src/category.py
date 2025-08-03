from typing import List, TypeVar

from src.product import Product

T = TypeVar("T", bound="Product")


class Category:

    def count_unique_products(self) -> int:
        return len(self.__products)

    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.total_categories += 1
        Category.total_products += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.total_products += 1

    def __repr__(self) -> str:
        return f"Category('{self.name}', товаров: {len(self.products)})"

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> List[Product]:
        return self.__products

    @products.setter
    def products(self, value: List[Product]) -> None:
        self.__products = value
