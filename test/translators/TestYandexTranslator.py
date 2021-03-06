import unittest

from src.translators.YandexTranslator import YandexTranslator


class TestYandexTranslator(unittest.TestCase):
	def setUp(self):
		self._translator = YandexTranslator()

	def test_translation(self):
		text = 'Примечание. Все специальные символы должны быть экранированы.'
		source = 'ru'
		target = 'en'

		translation = self._translator.translate(source, text, target)

		if translation is not None:
			print(translation)
		else:
			print("Error happened")
		self.assertEqual('Note. All special characters must be escaped.', translation)

	def test_with_special_characters(self):
		text = 'Примечание. " : % ^ & Все специальные символы должны быть экранированы.'
		source = 'ru'
		target = 'en'

		translation = self._translator.translate(source, text, target)
		print()
		print(text)
		print(translation)
		self.assertNotEqual(translation, None)
