import unittest
from src.storage.Cache import Cache


class TestCache(unittest.TestCase):
	cache = Cache()
	test_sets = [('ru', 'Привет', 'en', 'Hello'),
	             (('ru', 'Примечание. Все специальные символы должны быть экранированы.',
	               'en', 'Note. All special characters must be escaped.'))
	             ]

	def setUp(self):
		self.test_set = self.test_sets[1]

	def tearDown(self):
		self.cache.clear()

	def test_to_cache_key(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		h1 = self.cache._to_cache_key(source_text, target_lang)
		h2 = self.cache._to_cache_key(source_text, target_lang)
		self.assertEqual(h1, h2)

	def test_saving(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		h1 = self.cache._to_cache_key(source_text, target_lang)
		self.cache._add(h1, target_text)
		translation = self.cache._get(h1)
		self.assertEqual(target_text, translation)

	def test_finding(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		self.cache.add_translation(source_lang, source_text, target_lang, target_text)
		tr = self.cache.get_translation(source_lang, source_text, target_lang)

		print('')
		print('Source text: %s' % source_text)
		print('From cache: %s' % tr)

		self.assertNotEqual(tr, None)

	def test_translation_saves_right(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		self.cache.add_translation(source_lang, source_text, target_lang, target_text)
		tr = self.cache.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(tr, target_text)