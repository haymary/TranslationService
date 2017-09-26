import time

from src.TranslatorService import TranslatorService
import unittest


class TestTranslatorService(unittest.TestCase):
	def setUp(self):
		self.ts = TranslatorService()

	def test_dubble_translation(self):
		text = 'Hello, My name is Maria'

		times = []
		for _ in range(2):
			start = time.time()
			t = self.ts.translate('en', 'ru', text)
			end = time.time()
			times.append(end-start)
		self.assertLess(times[1], times[0])
