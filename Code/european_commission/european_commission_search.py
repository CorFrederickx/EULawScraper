"""mimicking European Commission search"""

from search import BaseSearchURL

class EuropeanCommissionSearch(BaseSearchURL):

    """
    Class for building search URLs for the European Commission's search interface, extending BaseSearchURL.
    """

    valid_dates = {
        '*': 'All',
        '-7': 'Last week',
        '-31': 'Last month',
        '-365': 'Last year',
    }

    valid_languages = {
        'bg': 'Bulgarski',
        'cs': 'Cestina',
        'da': 'Dansk',
        'de': 'Deutsch',
        'et': 'Eesti Keel',
        'el': 'Greek',
        'en': 'English',
        'es': 'Espanol',
        'fr': 'Francais',
        'ga': 'Gaeilge',
        'hr': 'Hrvatski',
        'it': 'Italiano',
        'lv': 'Latviesu Valoda',
        'lt': 'Lietuviu Kalba',
        'hu': 'Magyar',
        'mt': 'Malti',
        'nl': 'Nederlands',
        'pl': 'Polski',
        'pt': 'Portugues',
        'ro': 'Romana',
        'sk': 'Slovencina',
        'sl': 'Slovenscina',
        'fi': 'Suomi',
        'sv': 'Svenska',
        'ot': 'Other'
    }

    valid_formats = {
        '*': 'All',
        'htm': 'Web',
        'doc': 'Word',
        'xls': 'Excel',
        'pdf': 'PDF',
        'ppt': 'Powerpoint',
    }

    def __init__(self):

        """
        Initialize an instance of the URL builder with the European Commission search base URL.
        All search parameters are initialized as None.
        """

        super().__init__(base_url='https://ec.europa.eu/search/?')
        self.date = None
        self.language = None
        self.format = None

    def set_date (self, date='*'):

        """
        Applies a date filter to the search results.
        If chosen date filter is not valid, an error is raised.

        :param date: Key from valid_dates. Can be '*', '-7', '-31', or '-365'.
        """

        if date not in self.valid_dates:
             raise ValueError(f"Invalid type: '{date}'. Must be one of: {list(self.valid_dates.keys())}")
        self.date = date

    def set_language (self, language='en'):

        """
        Applies a language filter to the search results.
        If chosen language is not valid, an error is raised.

        :param language: Key from valid_languages.
        """

        if language not in self.valid_languages:
            raise ValueError(f"Invalid type: '{language}'. Must be one of: {list(self.valid_languages.keys())}")
        self.language = language

    def set_format (self, format='*'):

        """
        Applies a file format filter to the search results.
        If chosen file format is not valid, an error is raised.

        :param format: Key from valid_formats indicating preferred document format.
        """

        if format not in self.valid_formats:
            raise ValueError(f"Invalid type: '{format}'. Must be one of: {list(self.valid_formats.keys())}")
        self.format = format

    def build(self):

        """
        Constructs the final URL string using all the parameters set so far.

        :return: A fully-formed search URL for the European Commission website.
        """

        url = self.BASE_URL
        url += f'queryText={"+".join(self.text)}'
        url += '&query_source=europa_default&page=&filter=&swlang=en&filterSource=europa_default' # static parameters
        if self.date is not None:
            url += f'&more_options_date={self.date}'
        if self.language is not None:
            url += f'&more_options_language={self.language}'
        if self.format is not None:
            url += f'&more_options_f_formats={self.format}'
        return url
    