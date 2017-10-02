import json

from src.storage.Cache import Cache
from src.storage.Database import Database
from src.translators.YandexTranslator import YandexTranslator


class TranslatorService:
	def __init__(self):
		self._max_saved_text = 30
		self._tf = YandexTranslator()
		self._cache = Cache()
		self._db = Database()

	# ------- Public -------
	def translate_json(self, tr_json):
		"""
		Subtracts data from json for translation and gives to translation method
		:param tr_json: JSON with parameters (source_lang, source_text, target_lang)
		:return: JSON with fields (source_lang, source_text, target_lang, translation)
		which contains result in translation field
		"""
		tr_json = json.loads(tr_json)
		source_lang, source_text, target_langs = tr_json['source_lang'], tr_json['source_text'], tr_json['target_langs']
		if len(target_langs) == 1:
			tr = self.translate(source_lang, source_text, target_langs[0])
		else:
			tr = self.translate_many(source_lang, source_text, target_langs)
		tr_json['translation'] = tr
		return json.dumps(tr_json)

	def translate(self, source_lang, source_text, target_lang):
		"""
		Translates given text. Looks for translation in local storage (memcached and db)
		if nothing found looks in online translator
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: translations string in array if possible, None otherwise
		"""
		translation = self._check_in_storage(source_lang, source_text, target_lang)
		if translation is None:
			translation = self._tf.translate(source_lang, source_text, target_lang)
			self._save_to_storage(source_lang, source_text, target_lang, translation)
		return [translation]

	def translate_many(self, source_lang, source_text, target_langs):
		"""
		Translates given text. Looks for translation in local storage (memcached and db)
		if nothing found looks in online translator
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_langs: Codes of target languages
		:return: translations string if possible, None otherwise
		"""
		translations = self._check_in_storage_many(source_lang, source_text, target_langs)
		for translation, target_lang in zip(translations, target_langs):
			if translation is None:
				translation = self._tf.translate(source_lang, source_text, target_lang)
				self._save_to_storage(source_lang, source_text, target_lang, translation)
		return translations

	# ------- Private -------
	def _save_to_storage(self, source_lang, source_text, target_lang, translation):
		"""
		Saves translation to local storage
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:param translation: Text of translation
		"""
		if len(source_text) > self._max_saved_text: return
		self._cache.add_translation(source_lang, target_lang, source_text, translation)
		self._db.add_translation(source_lang, source_text, target_lang, translation)

	def _check_in_storage(self, source_lang, source_text, target_lang):
		"""
		Checks if translation of a given text to the given language is in local storage
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: translation string if exists, None otherwise
		"""
		if len(source_text) > self._max_saved_text: return None
		translation = self._cache.get_translation(source_lang, source_text, target_lang)
		if translation is None:
			translation = self._db.get_translation(source_lang, source_text, target_lang)
		return translation

	def _check_in_storage_many(self, source_lang, source_text, target_langs):
		"""
		Checks if translation of a given text to the given language is in local storage
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_langs: Codes of target language
		:return: translation string if exists, None otherwise
		"""
		if len(source_text) > self._max_saved_text: return None

		translations = [None] * len(target_langs)
		not_translated_ind, not_translated_lang = self.check_cache_many(source_lang, source_text,
		                                                                              target_langs, translations)

		if len(not_translated_lang) > 0:
			translations_db = self._db.get_translation_many(source_lang, source_text, not_translated_lang)
			for i, translation in zip(not_translated_ind, translations_db):
				translations[i] = translation
		return translations

	def check_cache_many(self, source_lang, source_text, target_langs, translations):
		not_translated_lang = []
		not_translated_ind = []
		for i, target_lang in enumerate(target_langs):
			translation = self._cache.get_translation(source_lang, source_text, target_lang)
			if translation is None:
				not_translated_lang.append(target_lang)
				not_translated_ind.append(i)
			else:
				translations[i] = translation
		return not_translated_ind, not_translated_lang
