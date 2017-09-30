from abc import ABC, abstractmethod

class ATranslator(ABC):

	@abstractmethod
	def translate(self, source_lang, source_text, target_lang):
		pass