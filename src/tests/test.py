import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from utils.OrderBook import OrderBook
import unittest


class TestUtils(unittest.TestCase):

    def test_simple_buys(self):
        book = OrderBook()
        book.add({"qty": 1, "price": 1.00, "side": "BUY"})
        self.assertEqual(book.get_best_bid(), 1.00)

    def test_simple_offer(self):
        book = OrderBook()
        book.add({"qty": 1, "price": 1.00, "side": "SELL"})
        self.assertEqual(book.get_best_offer(), 1.00)

    def test_simple_fair_price(self):
        book = OrderBook()
        book.add({"qty": 1, "price": 1.10, "side": "SELL"})
        book.add({"qty": 1, "price": 0.90, "side": "BUY"})
        self.assertEqual(book.get_fair_price(), 1.00)

    def test_cross_spread_on_offer(self):
        orders = [
            {"qty": 1, "price": 0.80, "side": "BUY"},
            {"qty": 1, "price": 0.90, "side": "BUY"},
            {"qty": 1, "price": 1.90, "side": "BUY"},
            {"qty": 0.5, "price": 0.90, "side": "SELL"},
            {"qty": 1.5, "price": 1.20, "side": "SELL"}
        ]
        book = OrderBook()
        for order in orders:
            book.add(order)

        self.assertEqual(book.get_best_bid(), 0.8)
        self.assertIsNone(book.get_best_offer())

    def test_cross_spread_on_bid(self):
        orders = [
            {"qty": 1, "price": 0.80, "side": "SELL"},
            {"qty": 1, "price": 0.90, "side": "SELL"},
            {"qty": 1, "price": 1.00, "side": "SELL"},
            {"qty": 0.5, "price": 0.90, "side": "BUY"},
            {"qty": 1.5, "price": 1.20, "side": "BUY"}
        ]
        book = OrderBook()
        for order in orders:
            book.add(order)

        self.assertEqual(book.get_best_offer(), 1.0)
        self.assertIsNone(book.get_best_bid())


if __name__ == '__main__':
    unittest.main()