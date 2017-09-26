from src.Cache import Cache
from src.TranslationFacade import TranslationFacade
from hashlib import sha1

class TranslatorService:
	def __init__(self):
		self.max_saved_text = 30
		self.tf = TranslationFacade()
		self.cache = Cache()

	def translate(self, source_lang, target_lang, text):
		translation = None
		text_preprocessed = self.escape_special_characters(text)

		text_hash = self.hash_text(text)

		if len(text) < self.max_saved_text:
			translation = self.check_cache(text_hash)
			if translation is None:
				translation = self.check_databese(text)
		if translation is None:
			translation = self.tf.translate(source_lang, target_lang, text_preprocessed)
			self.save_to_cache(text_preprocessed, translation)
		return translation

	def hash_text(self, text):
		hash_object = sha1(text.encode())
		return hash_object.hexdigest()

	def save_to_cache(self, text_preprocessed, translation):
		print('Saving to cache')
		self.cache.set(self.hash_text(text_preprocessed), translation)
		self.cache.set(self.hash_text(translation), text_preprocessed)

	def escape_special_characters(self, text) -> str:
		print('Prepossessing text')
		# TODO: check for special symbols
		return text

	def check_databese(self, text):
		print('Checking database')
		# TODO: check database
		return None

	def check_cache(self, text):
		print('Checking cache')
		return self.cache.get(text)
		