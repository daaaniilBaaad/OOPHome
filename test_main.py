from typing import List

import pytest

from main import Product, Category


@pytest.fixture
def sample_products() -> List[Product]:
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    return [product1, product2, product3]


@pytest.fixture
def addictional_product() -> Product:
    return Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)


@pytest.fixture
def combined_products(sample_products: List[Product], addictional_product: Product) -> List[Product]:
    return sample_products + [addictional_product]


@pytest.fixture
def sample_category(combined_products: List[Product]) -> Category:
    return Category(
        "Смартфоны и телевизоры",
        (
            "Смартфоны и телевизоры, как средство не только "
            "коммуникации, но и получения дополнительных функций "
            "для удобства жизни"
        ),
        combined_products,
    )


def test_product_init() -> None:
    product = Product("Product Name", "Product Description", 1090.90, 5)
    assert product.name == "Product Name"
    assert product.description == "Product Description"
    assert product.price == 1090.90
    assert product.quantity == 5


def test_product_negative_price() -> None:
    with pytest.raises(ValueError):
        Product("Wrong Product", "Product Description", -1090.90, 5)


def test_product_zero_price() -> None:
    product = Product("Product With Zero Price", "Product Description", 0.0, 5)
    assert product.price == 0.0


def test_product_zero_quantity() -> None:
    product = Product("Product With Zero Quantity", "Product Description", 1090.90, 0)
    assert product.quantity == 0


def test_category_init(combined_products: List[Product]) -> None:
    category = Category("Category Name", "Category Description", combined_products)
    assert category.name == "Category Name"
    assert category.description == "Category Description"
    assert len(category.products) == 4


def test_category_count(combined_products: List[Product]) -> None:
    init_category_count = Category.category_count
    init_product_count = Category.product_count
    category = Category("Category Name", "Category Description", combined_products)
    assert Category.category_count == init_category_count + 1
    assert Category.product_count == init_product_count + len(category.products)


def test_empty_products_category() -> None:
    category = Category("Empty Category", "Nothing Here", [])
    assert category.name == "Empty Category"
    assert category.description == "Nothing Here"
    assert len(category.products) == 0


def test_category_product_list(combined_products: List[Product]) -> None:
    category = Category("Category Name", "Category Description", combined_products)
    assert category.products[0].name == "Samsung Galaxy S23 Ultra"
    assert category.products[1].name == "Iphone 15"
    assert category.products[2].name == "Xiaomi Redmi Note 11"
    assert category.products[3].name == "55\" QLED 4K"


def test_addictional_product(addictional_product: Product) -> None:
    assert addictional_product.name == "55\" QLED 4K"
    assert addictional_product.description == "Фоновая подсветка"
    assert addictional_product.price == 123000.0
    assert addictional_product.quantity == 7


def test_additional_category(sample_category: Category) -> None:
    """Проверяет свойства категории с комбинированными продуктами."""
    assert sample_category.name == "Смартфоны и телевизоры"
    assert (
        sample_category.description == "Смартфоны и телевизоры, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )
    assert len(sample_category.products) == 4  # Проверяем, что 4 продукта в категории
    assert sample_category.products[3].name == "55\" QLED 4K"


def test_category_with_single_product() -> None:
    """Проверяет категорию с одним продуктом."""
    product = Product("Single Product", "Description", 1090.90, 1)
    category = Category("Single Product Category", "Description", [product])

    assert len(category.products) == 1
    assert Category.product_count == 17


def test_category_update() -> None:
    """Проверяет обновление свойств категории."""
    category = Category("Initial Category", "Initial Description", [])
    category.name = "Updated Name"
    category.description = "Updated Description"

    assert category.name == "Updated Name"
    assert category.description == "Updated Description"