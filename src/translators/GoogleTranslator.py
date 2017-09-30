from google.cloud import translate

from src.translators.ATranslator import ATranslator


class GoogleTranslator(ATranslator):

	def translate(self, source_lang, source_text, target_lang):

		translate_client = translate.Client()

		translation = translate_client.translate(
			source_text,
			target_language=target_lang)
		return translation