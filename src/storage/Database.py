import ssl
import pprint

import datetime
from pymongo import MongoClient


class Database:
	def __init__(self, db_name='translationDB', expire_after=3 * 24 * 60 * 60):
		mongoserver_uri = 'mongodb://iam_tomato:spaceman31@translationcluster-shard-00-00-uszjc.mongodb.net:27017,' \
		                  'translationcluster-shard-00-01-uszjc.mongodb.net:27017,translationcluster-shard-00-02-' \
		                  'uszjc.mongodb.net:27017/test?ssl=true&replicaSet=TranslationCluster-shard-0&authSource=admin'
		client = MongoClient(host=mongoserver_uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
		self.db = client[db_name]
		if len(self.db.collection_names()) > 0:
			self.posts = self.db.posts
			self.new_collection(expire_after)


	# ------- Public -------
	def add_translation(self, source_lang, source_s, target_lang, target_s):
		post = self._get_post_if_exists(source_lang, source_s, target_lang, target_s)
		if post is not None:
			post[source_lang] = source_s
			post[target_lang] = target_s
			return self._update_post(post)

		try:
			self.posts.insert_one({
						source_lang: source_s,
						target_lang: target_s,
						'updatedTime': datetime.datetime.utcnow()
			})
		except Exception as e:
			return False
		return True

	def get_translation(self, source_lang, source_s, target_lang):
		try:
			post = self.posts.find_one({source_lang: source_s, target_lang: {'$exists': True}})
			return post[target_lang]
		except Exception as e:
			return None

	def clear(self):
		self.posts.delete_many({})

	def remove_current_collection(self):
		try:
			self.posts = self.db.posts
			self.posts.drop()
		except Exception as e:
			pass

	def new_collection(self, expire_after):
		self.remove_current_collection()
		self.posts = self.db.posts
		self.posts.create_index("updatedTime", expireAfterSeconds=expire_after)

	# ------- Private -------
	def _get_post_if_exists(self, source_lang, source_s, target_lang, target_s):
		post = self._get_two_keys(source_lang, source_s, target_lang, target_s)
		if post is None:
			post = self._get_one_key(source_lang, source_s)
			if post is None:
				post = self._get_one_key(target_lang, target_s)
		return post

	def _update_post(self, post):
		try:
			post['updatedTime'] = datetime.datetime.utcnow()
			self.posts.update_one({'_id': post['_id']}, {"$set": post}, upsert=False)
		except Exception as e:
			return False
		return True

	def _get_one_key(self, key, value):
		try:
			return self.posts.find_one({key: value})
		except Exception as e:
			return None

	def _get_two_keys(self, s1_lang, s1, s2_lang, s2):
		try:
			return self.posts.find_one({s1_lang: s1, s2_lang: s2})
		except Exception as e:
			return None
