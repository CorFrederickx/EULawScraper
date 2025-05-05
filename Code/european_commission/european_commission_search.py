from search import BaseSearchURL

class EuropeanCommissionSearch(BaseSearchURL):

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
        super().__init__(base_url='https://ec.europa.eu/search/?')
        # is the self.base_url part missing here? like its now only works if base class is used for everything (I think?)
        self.date = None
        self.language = None
        self.format = None

    def set_date (self, date='*'):
        if date not in self.valid_dates:
             raise ValueError(f"Invalid type: '{date}'. Must be one of: {list(self.valid_dates.keys())}")
        self.date = date

    def set_language (self, language='en'):
        if language not in self.valid_languages:
            raise ValueError(f"Invalid type: '{language}'. Must be one of: {list(self.valid_languages.keys())}")
        self.language = language

    def set_format (self, format='*'):
        if format not in self.valid_formats:
            raise ValueError(f"Invalid type: '{format}'. Must be one of: {list(self.valid_formats.keys())}")
        self.format = format

    def build(self):
        url = self.BASE_URL

        url += f'queryText={"+".join(self.text)}' # impossible to do a search without text
        url += '&query_source=europa_default&page=&filter=&swlang=en&filterSource=europa_default' # static part of the url

        if self.date is not None:
            url += f'&more_options_date={self.date}'
        
        if self.language is not None:
            url += f'&more_options_language={self.language}'
        
        if self.format is not None:
            url += f'&more_options_f_formats={self.format}'

        return url
    