import unittest
from src.Cache import Cache


class TestCache(unittest.TestCase):
	def test_put(self):
		key, value = 'key', 'value'
		print('%s  %s' % (key, value))
		self.cache.set(key, value)
		res_value = self.cache.get(key)
		print(res_value)
		self.assertEqual(value, res_value)

	def test_put_wrong_key(self):
		key, value = 'key', 'value'
		print('%s  %s' % (key, value))
		self.cache.set(key, value)
		res_value = self.cache.get(key + 'ff')
		print(res_value)
		self.assertNotEqual(value, res_value)

	def setUp(self):
		self.cache = Cache()

	def tearDown(self):
		self.cache.disconnect()