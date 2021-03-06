import re
import requests
from src.translators.ATranslator import ATranslator


class YandexTranslator(ATranslator):
	_api_key = 'trnsl.1.1.20170926T124116Z.2bd1508a7ffae706.5cbed5dc27c8ea5b76a36ad193fcd826fbe1a366'

	def translate(self, source_lang, source_text, target_lang):
		"""
		Translates given text using Yandex Translation API
		:param source_lang: Code of source language
		:param source_text: Text for translation
		:param target_lang: Code of target language
		:return: translation string if translation is possible, None otherwise
		"""
		source_text = self._escape_special_chars(source_text)
		request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' \
		          'key=' + self._api_key + \
		          '&text=' + source_text + \
		          '&lang=' + source_lang + '-' + target_lang

		no_res = True
		counter = 0
		try:
			while no_res is True:
				translation = requests.post(request)
				if 'code' not in translation.json():
					no_res = False
				counter += 1
				if counter > 10:
					break
			js = translation.json()
			print(js)
			if 'code' in js:
				return None
			return translation.json()['text'][0]
		except requests.exceptions.ConnectionError as e:
			print(e)
			return None
		except Exception as e:
			print(e)
			return None

	def _escape_special_chars(self, source_text):
		return source_text.translate(str.maketrans({
			"-": r"\-",
			"]": r"\]",
			"\\": r"\\",
			"^": r"\^",
			"$": r"\$",
			"*": r"\*",
			"\"": r"\"",
			"\'": r"\'",
			"&": r"\&"
		}))
		# return source_text


