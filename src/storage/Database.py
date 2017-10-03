import ssl
import pprint

import datetime
from pymongo import MongoClient


class Database:
	"""
	Class for work with MongoDB
	"""
	def __init__(self, db_name='translationDB', expire_after=3 * 24 * 60 * 60):
		mongoserver_uri = 'mongodb://iam_tomato:spaceman31@translationcluster-shard-00-00-uszjc.mongodb.net:27017,' \
		                  'translationcluster-shard-00-01-uszjc.mongodb.net:27017,translationcluster-shard-00-02-' \
		                  'uszjc.mongodb.net:27017/test?ssl=true&replicaSet=TranslationCluster-shard-0&authSource=admin'
		client = MongoClient(host=mongoserver_uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
		self._db = client[db_name]
		if len(self._db.collection_names()) < 0:
			self.new_collection(expire_after)
		self._posts = self._db.posts


	# ------- Public -------
	def add_translation(self, source_lang, source_text, target_lang, target_text):
		"""
		Adds translation to database
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:param target_text: Translation
		:return: True if operation was successful, False otherwise
		"""
		post = self._get_post_if_exists(source_lang, source_text, target_lang, target_text)
		if post is not None:
			post[source_lang] = source_text
			post[target_lang] = target_text
			return self._update_post(post)

		try:
			self._posts.insert_one({
						source_lang: source_text,
						target_lang: target_text,
						'updatedTime': datetime.datetime.utcnow()
			})
		except Exception as e:
			return False
		return True

	def get_translation(self, source_lang, source_text, target_lang):
		"""
		Returns trnslation from database
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: Translation if in db, None otherwise
		"""
		try:
			post = self._posts.find_one({source_lang: source_text, target_lang: {'$exists': True}})
			return post[target_lang]
		except Exception as e:
			return None

	def get_translation_many(self, source_lang, source_text, not_translated_lang):
		translations = []
		for target_lang in not_translated_lang:
			post = self._posts.find_one({source_lang: source_text, target_lang: {'$exists': True}})
			if post is not None:
				translations.append(post[target_lang])
				break
			translations.append(post)

		for target_lang in not_translated_lang[len(translations):]:
			if target_lang in post:
				translations.append(post[target_lang])
			else:
				translations.append(None)
		return translations

	def clear(self):
		"""
		Deletes all records in current collection
		"""
		self._posts.delete_many({})

	def clear_db(self):
		"""
		Deletes all collections in db
		"""
		try:
			for collection in self._db.collection_names():
				collection = self._db[collection]
				collection.drop()
		except Exception as e:
			pass

	def new_collection(self, expire_after):
		"""
		Creates a new collection in db with given expiring time of records
		:param expire_after: ttl for records
		"""
		self.clear_db()
		self._posts = self._db.posts
		self._posts.create_index("updatedTime", expireAfterSeconds=expire_after)

	# ------- Private -------
	def _get_post_if_exists(self, lang_1, text_1, lang_2, text_2):
		"""
		Looks for a post in db which has at least one pair (lang : text)
		:param lang_1: Code of source language
		:param text_1: Text for translation
		:param lang_2: Code of target language
		:param text_2: Translation
		:return: post if in db, None otherwise
		"""
		try:
			post = self._posts.find_one({lang_1: text_1, lang_2: text_2})
			if post is None:
				post = self._posts.find_one({lang_1: text_1})
				if post is None:
					post = self._posts.find_one({lang_2: text_2})
		except Exception as e:
			return None
		return post

	def _update_post(self, post):
		"""
		Updates existing post with new data
		:param post: post from db
		:return: True if operation was successful, False otherwise
		"""
		try:
			post['updatedTime'] = datetime.datetime.utcnow()
			self._posts.update_one({'_id': post['_id']}, {"$set": post}, upsert=False)
		except Exception as e:
			return False
		return True
