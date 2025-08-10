import pytest

from src.product import Product
from src.lawn_grass import LawnGrass


def test_lawn_grass_init() -> None:

    lawn_grass = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0,
                           20, "Россия", "7 дней", "Зеленый")

    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.description == "Элитная трава для газона"
    assert lawn_grass.price == 500.0
    assert lawn_grass.quantity == 20
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_lawn_grass_repr() -> None:

    lawn_grass = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0,
                           20, "Россия", "7 дней", "Зеленый")
    expected_repr = ("Product('Газонная трава', 500.0 руб., 20 шт., Россия Страна., " 
                     "7 дней Период прорастания., Зеленый Цвет)"
    )

    assert repr(lawn_grass) == expected_repr


def test_lawn_grass_add_success() -> None:

    lawngrass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0,
                           20, "Россия", "7 дней", "Зеленый")
    lawngrass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0,
                           15, "США", "5 дней", "Темно-зеленый")

    assert lawngrass1 + lawngrass2 == 35



def test_lawn_grass_inheritance() -> None:

    assert issubclass(LawnGrass, Product)
