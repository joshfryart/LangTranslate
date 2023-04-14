from typing import Union
from pydantic import BaseModel
from translate import Translator

class InvalidLanguageCodeError(Exception):
    """A custom exception class for invalid language codes."""

# Define the tool class
class LangTranslateAPIWrapper(BaseModel):
    output_lang: str
    
    def run(self, input_text: str) -> str:
        """
        Translates the input text to the specified output language.
        
        Args:
            input_text: The text to be translated.
            
        Returns:
            The translated text in the specified output language or an error message.
        """
        # Validate input
        if not input_text.strip():
            return "Input text is empty. Please provide some text to translate."
        try:
            # Call API to translate text
            translator = Translator(to_lang=self.output_lang)
            output_text = translator.translate(input_text)
            return output_text
        except ValueError:
            return f"Invalid output language: {self.output_lang}. Please provide a valid ISO 639-1 language code."
        except Exception as e:
            return f"Error occurred during translation: {str(e)}"

class LANGTOOL:
    def __init__(self, api_wrapper: LangTranslateAPIWrapper):
        self.api_wrapper = api_wrapper

    def run(self, query: str) -> str:
        return self._run(query)
    
    async def arun(self, query: str) -> str:
        return await self._arun(query)
    
    def _run(self, query: str) -> str:
        raise NotImplementedError("The _run method should be implemented in the derived class.")
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("The _arun method should be implemented in the derived class.")
        
class LangTranslateRun(LANGTOOL):
    """LangTranslate - a standalone module that automatically translates text from one language to another."""

    name = "LangTranslate"
    description = (
        """LangTranslate is a standalone module that automatically translates text from one language to another. 
        It takes input text and an output language as inputs and returns the translated text in the specified language.
        """
    )
    final_answer_format = "Translated Text: {output_text}"

    def _run(self, query: str) -> str:
        """Use the LangTranslate tool."""
        output_text = self.api_wrapper.run(query)
        return f"Translated Text: {output_text}"
    
    async def _arun(self, query: str) -> str:
        """Use the LangTranslate tool asynchronously."""
        raise NotImplementedError("LangTranslateRun does not support async")
