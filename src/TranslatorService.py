from src.Cache import Cache
from src.Database import Database
from src.TranslationFacade import TranslationFacade
from hashlib import sha1

class TranslatorService:
	def __init__(self):
		self.max_saved_text = 30
		self.tf = TranslationFacade()
		self.cache = Cache()
		self.db = Database()

	def translate(self, source_lang, target_lang, text):
		translation = None
		text = self.escape_special_characters(text)

		if len(text) < self.max_saved_text:
			translation = self.check_cache(text, target_lang)
			if translation is None:
				translation = self.check_databese(source_lang, text)
		if translation is None:
			translation = self.tf.translate(source_lang, target_lang, text)
			self.save_to_cache(source_lang, target_lang, text, translation)
		return translation

	def hash_text(self, text):
		hash_object = sha1(text.encode())
		return hash_object.hexdigest()

	def save_to_cache(self, source_lang, target_lang, source_text, translation):
		print('Saving to cache')
		self.cache.set(self.to_cache_key(source_text, target_lang), translation)
		self.cache.set(self.to_cache_key(translation, source_lang), source_text)

	def escape_special_characters(self, text) -> str:
		print('Prepossessing text')
		# TODO: check for special symbols
		return text

	def check_databese(self, source_lang, text):
		print('Checking database')
		return self.db.get_translation(source_lang, text)

	def check_cache(self, source_text, target_lang):
		print('Checking cache')
		return self.cache.get(self.to_cache_key(source_text, target_lang))

	def to_cache_key(self, source_text, target_lang):
		return self.hash_text(source_text + target_lang)
		