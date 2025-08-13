import unittest

from src.product import Product


class TestProductQuantity(unittest.TestCase):
    def rest_zero_quantity_value_error(self) -> None:
        with self.assertRaises(ValueError) as e:
            Product('Тестовый продукт', 'Тест', 100.0, 0)

        self.assertEqual(str(e.exception), 'Количество товара должно быть положительным числом')

    def test_negative_quantity_value_error(self) -> None:
        with self.assertRaises(ValueError) as e:
            Product('Тестовый продукт', 'Тест', 100.0, -1)

        self.assertEqual(str(e.exception), 'Количество товара должно быть положительным числом')

    def test_positive_quantity_value_error(self) -> None:
        product = Product('Тестовый продукт', 'Тест', 100.0, 1)
        self.assertEqual(product.quantity, 1)


if __name__ == '__main__':
    unittest.main()