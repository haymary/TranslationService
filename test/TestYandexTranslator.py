import unittest

from src.translators.YandexTranslator import YandexTranslator


class TestYandexTranslator(unittest.TestCase):
	def setUp(self):
		self.yt = YandexTranslator()

	def test_translation(self):
		# The text to translate
		text = 'Примечание. Все специальные символы должны быть экранированы.'
		source = 'ru'
		target = 'en'

		translation = self.yt.translate(source, target, text)

		if translation is not None:
			print(translation.json())
		else:
			print("Error happened")
		self.assertEqual('Note. All special characters must be escaped.', translation.json()['text'][0])
