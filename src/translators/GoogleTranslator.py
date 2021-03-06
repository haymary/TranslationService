from google.cloud import translate
from src.translators.ATranslator import ATranslator


class GoogleTranslator(ATranslator):

	_api_key = 'AIzaSyD4gj1X_ndXYumI8ZcTq_h4xxQo7KT7QNQ'

	def __init__(self):

		self.translate_client = translate.Client()

	def translate(self, source_lang, source_text, target_lang):
		"""
		Translates given text using Google Translation API
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: translation string if translation is possible, None otherwise
		"""
		try:
			translation = self.translate_client.translate(
				source_text,
				source_language=source_lang,
				target_language=target_lang)
		except Exception as e:
			return None
		return translation['translatedText']