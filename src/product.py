from typing import Any, List, Type, TypeVar

T = TypeVar("T", bound="Product")


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {int(self.__price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не может быть отрицательной или равной нулю")
            return

        if new_price < self.__price:
            answer = input(
                f"Понизить цену с {self.__price} руб. на {new_price}? (y/n): "
            )
            if answer.lower() != "y":
                print("Цена не изменена")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls: Type[T], name: str, products: List[T], **kwargs: Any) -> T:
        for product in products:
            if isinstance(product, cls) and product.name == kwargs["name"]:
                product.quantity += kwargs["quantity"]
                if kwargs["price"] > product.price:
                    product.price = kwargs["price"]
                return product

        return cls(**kwargs)
