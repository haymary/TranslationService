import time
import unittest

from src.storage.Database import Database


class TestDatabase(unittest.TestCase):

	expire_time = 60
	db = Database()
	db.new_collection(expire_after=expire_time)

	test_sets = [('ru', 'Привет', 'en', 'Hello'),
	             (('ru', 'Примечание. Все специальные символы должны быть экранированы.',
	               'en', 'Note. All special characters must be escaped.'))
	             ]

	def setUp(self):
		self.test_set = self.test_sets[1]

	def tearDown(self):
		self.db.clear()

	def test_adding(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set

		res = self.db.add_translation(source_lang, source_text, target_lang, target_text)

		self.assertNotEqual(res, False)

	def test_finding(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set

		self.db.add_translation(source_lang, source_text, target_lang, target_text)
		tr = self.db.get_translation(source_lang, source_text, target_lang)
		print(tr)
		self.assertNotEqual(tr, None)

	def test_translation_saves_right(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set

		self.db.add_translation(source_lang, source_text, target_lang, target_text)
		tr = self.db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(tr, target_text)

	def test_expiring(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		self.db.add_translation(source_lang, source_text, target_lang, target_text)

		time.sleep(self.expire_time + 60)

		tr = self.db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(tr, None)

	def test_updating(self):
		(source_lang, source_text, target_lang, target_text) = self.test_set
		self.db.add_translation(source_lang, source_text, target_lang, target_text)

		another_lang = 'sp'
		another_text = 'Hola'
		self.db.add_translation(another_lang, another_text, target_lang, target_text)

		tr = self.db.get_translation(source_lang, source_text, target_lang)
		self.assertEqual(tr, target_text)

		tr = self.db.get_translation(source_lang, source_text, another_lang)
		self.assertEqual(tr, another_text)