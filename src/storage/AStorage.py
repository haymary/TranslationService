from abc import ABC, abstractmethod


class AStorage(ABC):

	@abstractmethod
	def add_translation(self, source_lang, source_text, target_lang, target_text) -> bool:
		pass

	@abstractmethod
	def get_translation(self, source_lang, source_text, target_lang) -> str:
		pass

	@abstractmethod
	def clear(self):
		pass