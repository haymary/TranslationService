import memcache
from hashlib import sha1
from src.storage.AStorage import AStorage


class Cache(AStorage):
	def __init__(self, hostname="127.0.0.1", port="11211", expiry=3600):
		self.hostname = "%s:%s" % (hostname, port)
		self.server = memcache.Client([self.hostname])
		self.expiry = expiry

	def add_translation(self, source_lang, source_text, target_lang, target_text):
		try:
			self.add(self.to_cache_key(source_text, target_lang), target_text)
			self.add(self.to_cache_key(target_text, source_lang), source_text)
		except Exception as e:
			return False
		return True

	def get_translation(self, source_lang, source_text, target_lang):
		return self.get(self.to_cache_key(source_text, target_lang))

	def add(self, key, value):
		self.server.set(key, value, self.expiry)

	def get(self, key):
		return self.server.get(key)

	def delete(self, key):
		self.server.delete(key)

	def disconnect(self):
		self.server.disconnect_all()

	def clear(self):
		self.server.flush_all()

	def to_cache_key(self, source_text, target_lang):
		return self.hash_text(source_text + target_lang)

	def hash_text(self, text):
		hash_object = sha1(text.encode())
		return hash_object.hexdigest()
