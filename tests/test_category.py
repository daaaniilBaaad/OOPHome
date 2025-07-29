# import unittest
# from src.product import Product
# from src.category import Category
#
#
# class TestCategory(unittest.TestCase):
#
#
#     def setUp(self):
#         self.product1 = Product("Product1", "Description1", 100, 5)
#         self.product2 = Product("Product2", "Description2", 200, 3)
#         self.products = [self.product1, self.product2]
#         self.category = Category("Electronics", "Electronic products", self.products)
#
#     def tearDown(self):
#         Category.total_categories = 0
#         Category.total_products = 0
#
#     def test_initialization(self):
#         self.assertEqual(self.category.name, "Electronics")
#         self.assertEqual(self.category.description, "Electronic products")
#         self.assertEqual(len(self.category.products), 2)
#         self.assertEqual(Category.total_categories, 1)
#         self.assertEqual(Category.total_products, 2)
#
#     def test_add_product(self):
#         product3 = Product("Product3", "Description3", 300, 1)
#         self.category.add_product(product3)
#         self.assertEqual(len(self.category.products), 3)
#         self.assertEqual(Category.total_products, 3)
#
#     def test_add_invalid_product(self):
#         with self.assertRaises(TypeError):
#             self.category.add_product("Not a product")
#
#     def test_count_unique_products(self):
#         self.assertEqual(self.category.count_unique_products(), 2)
#
#     def test_products_property(self):
#         self.assertEqual(self.category.products, self.products)
#
#     def test_products_setter(self):
#         new_products = [self.product1]
#         self.category.products = new_products
#         self.assertEqual(self.category.products, new_products)
#         self.assertEqual(Category.total_products, 2)
#
#     def test_repr(self):
#         self.assertEqual(repr(self.category), "Category('Electronics', товаров: 2)")
#
#
# if __name__ == "__main__":
#     unittest.main()


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


def test_add_product_to_non_empty_category(category_with_products: Category, sample_product: Product) -> None:
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