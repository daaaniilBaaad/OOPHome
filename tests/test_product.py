import unittest
from io import StringIO  # для перехвата вывода в консоль
from typing import Any
from unittest.mock import patch

from src.product import Product


# Создаем класс для тестирования функционала, связанного с ценой продукта
class TestProductPrice(unittest.TestCase):
    def setUp(self) -> None:
        """Метод setUp выполняется перед каждым тестом.
        Здесь создаем тестовый продукт с начальными параметрами:
        название, описание, цена=100.0, количество=10"""
        self.product = Product("Тестовый товар", "Описание", 100.0, 10)

    def test_price_getter(self) -> None:
        """Тест проверяет корректность работы геттера для цены.
        Убеждаемся, что возвращается правильное значение цены."""
        self.assertEqual(self.product.price, 100.0)

    def test_price_setter_valid(self) -> None:
        """Тест проверяет установку корректного значения цены.
        Устанавливаем новую цену 150.0 и проверяем, что она сохранилась."""
        self.product.price = 150.0
        self.assertEqual(self.product.price, 150.0)

    def test_price_setter_invalid_negative(self) -> None:
        """Тест проверяет обработку попытки установить отрицательную цену."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.product.price = -50.0
            self.assertEqual(self.product.price, 100.0)
            self.assertIn("Цена не может быть отрицательной или равной нулю", fake_out.getvalue())

    def test_price_setter_invalid_zero(self) -> None:
        """Тест аналогичен предыдущему, но для нулевой цены."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.product.price = 0.0
            self.assertEqual(self.product.price, 100.0)
            self.assertIn("Цена не может быть отрицательной или равной нулю", fake_out.getvalue())


    @patch("builtins.input", return_value="y")
    def test_price_decrease_with_confirmation(self, mock_input: Any) -> None:
        """Тест проверяет понижение цены с подтверждением пользователя.
        Используем декоратор patch для имитации ввода 'y' (yes).
        Цена должна успешно измениться на 80.0."""
        self.product.price = 80.0
        self.assertEqual(self.product.price, 80.0)

    @patch("builtins.input", return_value="n")
    def test_price_decrease_with_rejection(self, mock_input: Any) -> None:
        """Тест проверяет понижение цены, когда пользователь отказывается (вводит 'n')."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.product.price = 80.0
            self.assertEqual(self.product.price, 100.0)
            self.assertIn("Цена не изменена", fake_out.getvalue())

    def test_price_increase_no_confirmation_needed(self) -> None:
        """Тест проверяет повышение цены без необходимости подтверждения.
        В этом случае цена должна меняться сразу без дополнительных вопросов."""
        self.product.price = 120.0
        self.assertEqual(self.product.price, 120.0)


if __name__ == "__main__":
    unittest.main()