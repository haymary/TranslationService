from google.cloud import translate

from src.translators.ATranslator import ATranslator


class GoogleTranslator(ATranslator):

	def translate(self, source_lang, source_text, target_lang):
		"""
		Translates given text using Google Translation API
		:param source_lang: Name of source language
		:param source_text: Text for translation
		:param target_lang: Name of target language
		:return: translation string if translation is possible, None otherwise
		"""

		translate_client = translate.Client()

		translation = translate_client.translate(
			source_text,
			target_language=target_lang)
		return translation