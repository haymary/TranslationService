from abc import ABC, abstractmethod

class ATranslator(ABC):

	@abstractmethod
	def translate(self, source_lang, target_lang, text):
		pass