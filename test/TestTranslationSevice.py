import time
import unittest
from src.TranslatorService import TranslatorService
import json

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
		translation_db = self.ts._db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation, translation_db)

	def test_data_saved_to_cache(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_lang = 'ru'

		translation = self.ts.translate(source_lang, source_text, target_lang)
		translation_c = self.ts._cache.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation, translation_c)

	def test_translate_many(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_langs = ['ru', 'it', 'ja']
		tr_json = json.dumps({'source_lang':source_lang, 'source_text':source_text, 'target_langs':target_langs})
		translations = json.loads(self.ts.translate_json(tr_json))
		for tr in translations:
			self.assertNotEqual(tr, None)
		print()
		print(translations['translation'])

	def test_translation(self):
		source_lang = 'ru'
		source_text = 'Примечание. Все специальные символы должны быть экранированы.'
		target_langs = ['en']
		target_text = 'Note. All special characters must be escaped.'
		tr_json = json.dumps({'source_lang': source_lang, 'source_text': source_text, 'target_langs': target_langs})
		translations = json.loads(self.ts.translate_json(tr_json))
		self.assertEqual(translations['translation'][0], 'Note. All special characters must be escaped.')