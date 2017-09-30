import time
import unittest
from src.TranslatorService import TranslatorService


class TestTranslatorService(unittest.TestCase):
	def setUp(self):
		self.ts = TranslatorService()

	def test_store_decrease_time(self):
		text = 'Hello, My name is Maria'

		times = []
		for _ in range(2):
			start = time.time()
			t = self.ts.translate('en', 'ru', text)
			end = time.time()
			times.append(end-start)
		self.assertLess(times[1], times[0])

	def test_data_saved_to_db(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_lang = 'ru'

		translation = self.ts.translate(source_lang, source_text, target_lang)
		translation_db = self.ts.db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation, translation_db)

	def test_data_saved_to_cache(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_lang = 'ru'

		translation = self.ts.translate(source_lang, source_text, target_lang)
		translation_c = self.ts.cache.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation, translation_c)