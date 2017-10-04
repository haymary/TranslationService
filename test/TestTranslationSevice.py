import time
import unittest
from src.TranslationService import TranslatorService
import json

from src.exceptions.ServiceUnavailableException import ServiceUnavailableException


class TestTranslatorService(unittest.TestCase):
	def setUp(self):
		self.ts = TranslatorService()
		self.ts._cache.clear()
		self.ts._db.clear()

	def test_store_decrease_time(self):
		text = 'Hello, My name is Maria'

		times = []
		for _ in range(2):
			start = time.time()
			t = self.ts._translate('en', 'ru', text)
			end = time.time()
			times.append(end-start)
		self.assertLess(times[1], times[0])

	def test_data_saved_to_db(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_lang = 'ru'

		translation = self.ts._translate(source_lang, source_text, target_lang)
		translation_db = self.ts._db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation[0], translation_db)

	def test_data_saved_to_cache(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_lang = 'ru'

		translation = self.ts._translate(source_lang, source_text, target_lang)
		translation_c = self.ts._cache.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(translation[0], translation_c)

	def test_translate_many(self):
		source_lang = 'en'
		source_text = 'Hello, My name is Maria'
		target_langs = ['ru', 'it', 'ja']
		tr_json = {"user_info": 0, 'source_lang':source_lang, 'source_text':source_text, 'target_langs':target_langs}
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
		tr_json = {"user_info": 0, 'source_lang': source_lang, 'source_text': source_text, 'target_langs': target_langs}
		translations = json.loads(self.ts.translate_json(tr_json))
		self.assertEqual(translations['translation'][0], target_text)

	def test_translate_many_not_none(self):
		req = {
			"user_info": 0,
			"source_lang": "en",
			"source_text": "Hello, My name is Maria",
			"target_langs": [
				"ru","it","ja","de","no","sk","ru","be","ca","cs","da","el","es","et","fi","fr","hu","lt","lv",
				"mk",
				"nl"
			]
		}
		translations = json.loads(self.ts.translate_json(req))
		print(translations)
		for translation in translations['translation']:
			self.assertNotEqual(translation, None)