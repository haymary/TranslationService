from google.cloud import translate

from src.translators.ATranslator import ATranslator


class GoogleTranslator(ATranslator):

	def translate(self, source_lang, target_lang, text):

		translate_client = translate.Client()

		translation = translate_client.translate(
			text,
			target_language=target_lang)
		return translation