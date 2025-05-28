"""mimicking the search engines of several official European Union websites """

import abc

class BaseSearchURL(abc.ABC):

    """Abstract base class for building search URLs"""

    def __init__(self, base_url: str):

        """
        Initialize an instance of the search URL builder with a base_url

        :param base_url: The URL of the search engine of your choice that can be completed with additional parameters.
        """

        self.BASE_URL = base_url
        self.text = []
        self.date_range = []
        self.languages = []

    def set_text(self, text):

        """Define what you're looking for. Put spaces between different keywords."""

        for term in text.split():
            if '?' in term:
                term = term.replace('?', '%3F')
            self.text.append(term)

    def set_date_range(self, start_date='', end_date=''):

        """set the date range in which you're searching. The format is ddmmyyy"""

        self.date_range = [start_date, end_date]

    def set_language (self, languages):

        """set the language of the documents you're looking for"""

        for language in languages.split():
            self.languages.append(language)

    @abc.abstractmethod
    def build(self):

        """making sure there is a build method implemented in the subclass"""

        raise NotImplementedError("Subclasses must implement the build method")




    