from src.storage.Cache import Cache
from src.storage.Database import Database
from src.TranslationFacade import TranslationFacade


class TranslatorService:
	def __init__(self):
		self.max_saved_text = 30
		self.tf = TranslationFacade()
		self.cache = Cache()
		self.db = Database()

	def translate(self, source_lang, source_text, target_lang):
		source_text = self.escape_special_characters(source_text)
		translation = self._check_in_storage(source_lang, source_text, target_lang)
		if translation is None:
			translation = self.tf.translate(source_lang, source_text, target_lang)
			self._save_to_storage(source_lang, source_text, target_lang, translation)
		return translation

	def _save_to_storage(self, source_lang, source_text, target_lang, translation):
		if len(source_text) > self.max_saved_text: return None
		self.cache.add_translation(source_lang, target_lang, source_text, translation)
		self.db.add_translation(source_lang, source_text, target_lang, translation)

	def _check_in_storage(self, source_lang, source_text, target_lang):
		if len(source_text) > self.max_saved_text: return None
		translation = self.cache.get_translation(source_lang, source_text, target_lang)
		if translation is None:
			translation = self.db.get_translation(source_lang, source_text, target_lang)
		return translation

	def escape_special_characters(self, text) -> str:
		print('Prepossessing text')
		# TODO: check for special symbols
		return text