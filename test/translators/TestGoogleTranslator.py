import unittest
from src.translators.GoogleTranslator import GoogleTranslator


class TestGoogleTranslator(unittest.TestCase):

	def setUp(self):
		self.gt = GoogleTranslator()

	def test_translation(self):
		# The text to translate
		text = u'Hello, world!'
		sourse = 'en'
		target = 'ru'

		translation = self.gt.translate(sourse, target, text)

		print(u'Text: {}'.format(text))
		print(u'Translation: {}'.format(translation['translatedText']))