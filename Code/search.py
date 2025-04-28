import abc

class BaseSearchURL(abc.ABC):
    """Abstract base class for building search URLs"""

    def __init__(self, base_url: str):
        self.BASE_URL = base_url
        self.text = []
        self.date_range = []
        self.languages = []

    def set_text(self, text):
        for term in text.split():
            if '?' in term:
                term = term.replace('?', '%3F')
            self.text.append(term)

    def set_date_range(self, start_date='', end_date=''): # format is ddmmyyyy
        self.date_range = [start_date, end_date]

    def set_language (self, languages):
        for language in languages.split():
            self.languages.append(language)

    @abc.abstractmethod
    def build(self):
        raise NotImplementedError("Subclasses must implement the build method")




    