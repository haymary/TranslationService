import memcache
from hashlib import sha1
from src.storage.AStorage import AStorage


class Cache(AStorage):
	"""
	Class for work with Memcached
	"""
	def __init__(self, hostname="127.0.0.1", port="11211", expiry=3600):
		self.hostname = "%s:%s" % (hostname, port)
		self.server = memcache.Client([self.hostname])
		self.expiry = expiry

	# ------- Public -------
	def add_translation(self, source_lang, source_text, target_lang, target_text):
		"""
		Adds translation to cache
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:param target_text: Translation
		:return: True if operation was successful, False otherwise
		"""
		try:
			self._add(self._to_cache_key(source_text, target_lang), target_text)
			self._add(self._to_cache_key(target_text, source_lang), source_text)
		except Exception as e:
			return False
		return True

	def get_translation(self, source_lang, source_text, target_lang):
		"""
		Looks for translation in cache
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: translation if in db, None otherwise
		"""
		return self._get(self._to_cache_key(source_text, target_lang))

	def delete(self, key):
		"""
		Deletes entry with specified key from cache
		:param key: string
		:return: True if operation was successful, False otherwise
		"""
		try:
			self.server.delete(self._to_cache_key(key))
		except Exception as e:
			return False
		return True

	def clear(self):
		"""
		Deletes all records from cache
		:return: True if operation was successful, False otherwise
		"""
		try:
			self.server.flush_all()
		except Exception as e:
			return False
		return True

	# ------- Private -------
	def _add(self, key, value):
		"""
		Adds key-value pair to cache
		:return: True if operation was successful, False otherwise
		"""
		try:
			res = self.server.set(key, value, self.expiry)
			if res != 0:
				return True
		except Exception as e:
			pass
		return False

	def _get(self, key):
		"""
		Adds key-value pair to cache
		:return: value if operation was successful, None otherwise
		"""
		try:
			return self.server.get(key)
		except Exception as e:
			return None

	def _to_cache_key(self, source_text, target_lang):
		"""
		Transforms input to key for caching
		:param source_text: text from which we r translating
		:param target_lang: code of lang ti which we r translating
		:return: key for cache
		"""
		return self._hash_text(source_text + target_lang)

	def _hash_text(self, text):
		hash_object = sha1(text.encode())
		return hash_object.hexdigest()
