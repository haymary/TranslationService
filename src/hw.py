from bottle import route, run, request, template, response
from src.TranslatorService import TranslatorService


@route('/translate')
def translate():
	# source_lang = request.json['source_lang']
	# source_text = request.json['source_text']
	# target_langs = request.json['target_langs']

	response.content_type = 'application/json'

	req = request.json
	print(req)
	return ts.translate_json(req)


ts = TranslatorService()
run(host='localhost', port=8080, debug=True)
