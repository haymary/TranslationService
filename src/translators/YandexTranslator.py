import requests

from src.translators.ATranslator import ATranslator


class YandexTranslator(ATranslator):
	api_key = 'trnsl.1.1.20170926T124116Z.2bd1508a7ffae706.5cbed5dc27c8ea5b76a36ad193fcd826fbe1a366'

	def translate(self, source_lang, source_text, target_lang):
		request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' \
		          'key=' + self.api_key +\
		          '&text=' + source_text +\
		          '&lang=' + source_lang + '-' + target_lang

		no_res = True
		while no_res is True:
			try:
				translation = requests.post(request)
				no_res = False
			except requests.exceptions.ConnectionError as e:
				return None
			except Exception as e:
				print(e)
				return None
			print(translation.json())
		return translation.json()['text'][0]
