import pprint
import time
import datetime
import unittest

from src.Database import Database


class TestDatabase(unittest.TestCase):

	expire_time = 60
	db = Database()
	db.new_collection(expire_after=expire_time)

	def tearDown(self):
		self.db.clear_database()

	def test_adding(self):
		s1_l = 'ru'
		s1 = 'Привет'
		s2_l = 'en'
		s2 = 'Hello'

		res = self.db.add_translation(s1_l, s1, s2_l, s2)
		self.assertNotEqual(res, False)

	def test_finding(self):
		s1_l = 'ru'
		s1 = 'Привет'
		s2_l = 'en'
		s2 = 'Hello'

		self.db.add_translation(s1_l, s1, s2_l, s2)
		tr = self.db.get_translation(s1_l, s1, s2_l)
		self.assertNotEqual(tr, None)

	def test_translation_saves_right(self):
		s1_l = 'ru'
		s1 = 'Привет'
		s2_l = 'en'
		s2 = 'Hello'

		self.db.add_translation(s1_l, s1, s2_l, s2)
		tr = self.db.get_translation(s1_l, s1, s2_l)
		self.assertEqual(tr[s1_l], s1)
		self.assertEqual(tr[s2_l], s2)

	def test_expiring(self):
		s1_l = 'ru'
		s1 = 'Привет'
		s2_l = 'en'
		s2 = 'Hello'
		self.db.add_translation(s1_l, s1, s2_l, s2)

		time.sleep(self.expire_time + 60)

		tr = self.db.get_translation(s1_l, s1, s2_l)
		self.assertEqual(tr, None)

	def test_updating(self):
		s1_l = 'ru'
		s1 = 'Привет'
		s2_l = 'en'
		s2 = 'Hello'
		self.db.add_translation(s1_l, s1, s2_l, s2)

		s3_l = 'sp'
		s3 = 'Hola'
		self.db.add_translation(s3_l, s3, s2_l, s2)
		tr = self.db.get_translation(s1_l, s1, s2_l)

		self.assertEqual(tr[s1_l], s1)
		self.assertEqual(tr[s2_l], s2)
		self.assertEqual(tr[s3_l], s3)