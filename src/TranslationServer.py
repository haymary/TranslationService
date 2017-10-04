from bottle import route, run, request, template, response
from src.TranslationService import TranslatorService


@route('/translate')
def translate():
	"""
	Translates given text to given languages
	Takes json with fields:
		source_lang: language code of the text to translate
		source_text: text to translate
		target_langs: array of codes of languages to which
		supplied text should be translated
	:return: supplied json with extra field "translation" with
	array of translations ordered correspondingly to targel_langs
	"""
	response.content_type = 'application/json'
	return ts.translate_json(request.json)

ts = TranslatorService()
run(host='localhost', port=8080, debug=True)
