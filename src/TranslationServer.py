from bottle import HTTPResponse
from bottle import route, run, request, template, response

from src.TranslationService import TranslatorService

from src.exceptions.UnauthorizedException import UnauthorizedException
from src.exceptions.PaymentRequiredException import PaymentRequiredException
from src.exceptions.ServiceUnavailableException import ServiceUnavailableException


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
	try:
		r_body = ts.translate_json(request.json)
	except UnauthorizedException as e:
		return HTTPResponse(status=401)
	except PaymentRequiredException as e:
		return HTTPResponse(status=402)
	except ServiceUnavailableException as e:
		return HTTPResponse(status=503)
	return HTTPResponse(status=200, body=r_body)

ts = TranslatorService()
run(host='localhost', port=8080, debug=True)
