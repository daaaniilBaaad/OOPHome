import json
import unittest
from typing import List
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import Category
from src.utils import Product
from src.utils import load_data_from_json


class TestLoadDataFromJson(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "name": "Электроника",
                    "description": "Техника",
                    "products": [{"name": "Смартфон", "description": "Мощный", "price": 50000.0, "quantity": 10}],
                }
            ]
        ),
    )
    def test_load_data_from_json_single_category_single_product(self, mock_file: MagicMock) -> None:
        """
        Функция тестирует загрузку данных из JSON, когда файл содержит:
        - одну категорию
        - с одним товаром

        Проверяет:
        1. Что возвращается список с одной категорией
        2. Что атрибуты категории заполнены корректно
        3. Что в категории ровно один товар
        4. Что атрибуты товара заполнены корректно
        """
        categories: List[Category] = load_data_from_json("dummy_path.json")

        self.assertEqual(len(categories), 1)
        self.assertIsInstance(categories[0], Category)
        self.assertEqual(categories[0].name, "Электроника")
        self.assertEqual(categories[0].description, "Техника")

        self.assertEqual(len(categories[0].products), 1)
        self.assertIsInstance(categories[0].products[0], Product)
        self.assertEqual(categories[0].products[0].name, "Смартфон")
        self.assertEqual(categories[0].products[0].price, 50000.0)
        self.assertEqual(categories[0].products[0].quantity, 10)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "name": "Электроника",
                    "description": "Техника",
                    "products": [
                        {"name": "Смартфон", "description": "Мощный", "price": 50000.0, "quantity": 10},
                        {"name": "Ноутбук", "description": "Игровой", "price": 100000.0, "quantity": 5},
                    ],
                },
                {
                    "name": "Одежда",
                    "description": "Модная",
                    "products": [{"name": "Футболка", "description": "Хлопковая", "price": 2000.0, "quantity": 50}],
                },
            ]
        ),
    )
    def test_load_data_from_json_multiple_categories_products(self, mock_file: MagicMock) -> None:
        """
        Функция тестирует загрузку данных из JSON, когда файл содержит:
        - несколько категорий (2)
        - разное количество товаров в категориях (2 и 1)

        Проверяет:
        1. Что возвращается список с двумя категориями
        2. Что названия категорий соответствуют ожидаемым
        3. Что количество товаров в каждой категории верное
        4. Что общее количество товаров корректно суммируется
        """
        categories: List[Category] = load_data_from_json("dummy_path.json")

        self.assertEqual(len(categories), 2)

        # Проверяем первую категорию
        self.assertEqual(categories[0].name, "Электроника")
        self.assertEqual(len(categories[0].products), 2)

        # Проверяем второй категорию
        self.assertEqual(categories[1].name, "Одежда")
        self.assertEqual(len(categories[1].products), 1)

        # Проверяем общее количество продуктов
        total_products: int = sum(len(cat.products) for cat in categories)
        self.assertEqual(total_products, 3)

    def test_load_data_from_json_empty_file(self) -> None:
        """
        Функция тестирует обработку пустого JSON файла.

        Проверяет:
        1. Что функция возвращает пустой список
        2. Что не возникает исключений при обработке пустого файла
        """
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps([])):
            categories: List[Category] = load_data_from_json("empty.json")
            self.assertEqual(len(categories), 0)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_data_from_json_file_not_found(self, mock_file: MagicMock) -> None:
        """
        Функция тестирует обработку ситуации, когда файл не найден.

        Проверяет:
        1. Что функция выбрасывает исключение FileNotFoundError
        2. Что исключение возникает именно при попытке открыть несуществующий файл
        """
        with self.assertRaises(FileNotFoundError):
            load_data_from_json("nonexistent.json")


if __name__ == "__main__":
    unittest.main()