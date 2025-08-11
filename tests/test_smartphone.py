import pytest

from src.product import Product
from src.smartphone import Smartphone


def test_smartphone_init() -> None:

    smartphone = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый"
    )

    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_smartphone_repr() -> None:

    smartphone = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый"
    )

    expected_repr = ("Smartphone('Samsung Galaxy S23 Ultra', 256GB, Серый цвет, 200MP камера, "
                     "180000.0, 5, 95.5, S23 Ultra, 256, Серый)")
    assert repr(smartphone) == expected_repr


def test_smartphone_add_success() -> None:

    smartphone1 = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый"
    )

    smartphone2 = Smartphone(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
        efficiency=98.2,
        model="15",
        memory=512,
        color="Gray space"
    )

    total_quantity = smartphone1 + smartphone2
    assert total_quantity == 13
