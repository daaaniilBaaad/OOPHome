from typing import Any

import pytest

from src.category import Category
from src.product import Product


@pytest.fixture
def sample_product() -> Product:
    return Product("Телевизор", "4K OLED", 100000.0, 10)


@pytest.fixture
def empty_category() -> Category:
    return Category("Пустая категория", "Без товаров", [])


@pytest.fixture
def category_with_products(sample_product: Product) -> Category:
    return Category("Электроника", "Техника", [sample_product])


def test_add_product_to_empty_category(empty_category: Category, sample_product: Product) -> None:
    """Тестирует добавление продукта в пустую категорию."""
    # Проверяем начальное состояние
    assert len(empty_category.products) == 0
    assert Category.total_products == 0

    # Добавляем продукт
    empty_category.add_product(sample_product)

    # Проверяем результаты
    assert len(empty_category.products) == 1
    assert empty_category.products[0] == sample_product
    assert Category.total_products == 1


def test_add_product_to_non_empty_category(category_with_products: Category) -> None:
    """Тестирует добавление продукта в непустую категорию."""
    initial_count = len(category_with_products.products)
    initial_total = Category.total_products

    # Создаем и добавляем новый продукт
    new_product = Product("Ноутбук", "Игровой", 150000.0, 5)
    category_with_products.add_product(new_product)

    # Проверяем результаты
    assert len(category_with_products.products) == initial_count + 1
    assert category_with_products.products[-1] == new_product
    assert Category.total_products == initial_total + 1


def test_products_property_getter(category_with_products: Category, sample_product: Product) -> None:
    """Тестирует геттер products на возврат оригинального списка (без копии)."""
    products1 = category_with_products.products
    products2 = category_with_products.products

    assert products1 == products2  # Содержимое одинаковое
    assert products1 is products2  # Это один и тот же объект (не копия)
    assert isinstance(products1, list)
    assert products1[0] == sample_product


def test_products_property_returns_original(category_with_products: Category) -> None:
    """Тестирует, что property возвращает оригинальный список продуктов (не копию)."""
    # Получаем список продуктов через property
    products_reference = category_with_products.products
    original_products = category_with_products._Category__products  # Получаем доступ к оригиналу

    # Проверяем, что это один и тот же объект
    assert products_reference is original_products, "Геттер должен возвращать оригинальный список"

    # Создаем тестовый продукт
    test_product = Product(
        name="Тестовый продукт",
        description="Тестовое описание",
        price=100.0,
        quantity=1
    )

    # Запоминаем исходную длину
    original_length = len(original_products)

    # Изменяем полученный список
    products_reference.append(test_product)

    # Проверяем, что оригинальный список ИЗМЕНИЛСЯ
    assert len(original_products) == original_length + 1, "Оригинальный список должен изменяться"
    assert test_product in original_products, "Тестовый продукт должен появиться в оригинальном списке"


@pytest.mark.parametrize(
    "invalid_value",
    [
        "не продукт",  # str
        123,  # int
        {},  # dict
        None,  # None
        ["список", "продуктов"],  # list
    ],
)
def test_add_product_invalid_type(empty_category: Category, invalid_value: Any) -> None:
    """Тестирует обработку невалидных типов при добавлении продукта."""
    with pytest.raises(TypeError) as exc_info:
        empty_category.add_product(invalid_value)

    assert "только объекты класса Product" in str(exc_info.value)
    assert len(empty_category.products) == 0


class TestCategoryStr:

    def test_empty_category(self) -> None:
        category = Category("Пустая категория", "Без товаров", [])
        assert str(category) == "Пустая категория, количество продуктов: 0 шт."

    def test_single_product(self) -> None:
        product = Product("Телефон", "Смартфон", 60000, 10)
        category = Category("Электроника", "Гаджеты", [product])
        assert str(category) == "Электроника, количество продуктов: 10 шт."

    def test_multiple_products(self) -> None:
        products = [
            Product("Тестовый товар 1", "Описание 1", 100, 1),
            Product("Тестовый товар 2", "Описание 2", 200, 2),
            Product("Тестовый товар 3", "Описание 3", 300, 3)
        ]
        category = Category("Техника", "Разное", products)
        assert str(category) == "Техника, количество продуктов: 6 шт."
