from src.translators.YandexTranslator import YandexTranslator


class TranslationFacade:
	def __init__(self):
		self.translator = YandexTranslator()

	def translate(self, source_lang, source_text, target_lang):
		return self.translator.translate(source_lang, source_text, target_lang)