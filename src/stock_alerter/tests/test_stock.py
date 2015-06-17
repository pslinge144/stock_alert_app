import unittest
from datetime import datetime, timedelta
import collections

from ..stock import Stock


class StockTest(unittest.TestCase):

	def setUp(self):
		self.goog = Stock("GOOG")
		
	def test_price_of_a_new_stock_class_should_be_None(self):
		self.assertIsNone(self.goog.price)

	def test_stock_update(self):
		"""An update should set the price on the stock object
		We will be using the 'datetime' module for the timestamp
		"""
		self.goog.update(datetime(2014, 2, 12), price=10)
		self.assertEqual(10, self.goog.price)

	def test_negative_price_should_throw_ValueError(self):
		self.assertRaises(ValueError, self.goog.update,
			datetime(2014, 2, 13), -1)

	def test_stock_price_should_give_the_latest_price(self):
		self.goog.update(datetime(2014, 2, 12), price=10)
		self.goog.update(datetime(2014, 2, 13), price=8.4)
		self.assertAlmostEqual(8.4, self.goog.price, delta=0.0001)

	def test_stock_price_should_give_the_latest_price_by_timestamp(self):
		self.goog.update(datetime(2014, 2, 13), price=10)
		self.goog.update(datetime(2014, 2, 12), price=8.4)
		self.assertAlmostEqual(10, self.goog.price, delta=0.0001)

class StockTrendTest(unittest.TestCase):

	def setUp(self):
		self.goog = Stock("GOOG")

	def given_a_series_of_prices(self, prices):
		timestamps = [datetime(2014, 2, 11), datetime(2014, 2, 12),
			datetime(2014, 2, 13)]
		for timestamp, price in zip(timestamps, prices):
			self.goog.update(timestamp, price)

	def test_increasing_trend_is_true_if_price_increases_for_3_updates(self):
		self.given_a_series_of_prices([8, 10, 12])
		self.assertTrue(self.goog.is_increasing_trend())

	def test_increasing_trend_is_false_if_price_decreases(self):
		self.given_a_series_of_prices([8, 12, 10])
		self.assertFalse(self.goog.is_increasing_trend())

	def test_increasing_trend_is_false_if_price_equal(self):
		self.given_a_series_of_prices([8, 10, 10])
		self.assertFalse(self.goog.is_increasing_trend())

	def test_increasing_trend_is_true_when_updates_out_of_order(self):
		self.goog.update(datetime(2014, 2, 14), 12)
		self.goog.update(datetime(2014, 2, 13), 10)
		self.goog.update(datetime(2014, 2, 12), 8)
		self.assertTrue(self.goog.is_increasing_trend())

class StockCrossOverSignalTest(unittest.TestCase):
	def setUp(self):
		self.goog = Stock("GOOG")

	def _flatten(self, timestamps):
		if not isinstance(timestamp, collections.Iterable):
			yield timestamp
		else:
			for value in self._flatten(timestamp):
				yield value

	def _generate_timestamp_for_date(self, date, price_list):
		if not isinstance(price_list, collections.Iterable):
			return date
		else:
			delta = 1.0/len(price_list)
			return [date + i*timedelta(delta) for i in range(len(price_list))]

	def _generate_timestamps(self, price_list):
		return list(self._flatten([
			self._generate_timestamp_for_date(datetime(2014, 2, 13) - timedelta(i),
				price_list[len(price_list)-i-1])
			for i in range(len(price_list) - 1, -1, -1)
			if price_list[len(price_list) - i - 1] is not None]))

	def given_a_series_of_prices(self, price_list):
		timestamps = self._generate_timestamps(price_list)
		for timestamp, price in zip(timestamps,
					list(self._flatten([p
							for p in price_list
							if p is not None]))):
			self.goog.update(timestamp, price)	
