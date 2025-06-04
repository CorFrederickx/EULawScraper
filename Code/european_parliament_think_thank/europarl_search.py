"""mimicking the Advanced Search of the European Parliament's 'Think Tank' website"""

from search import BaseSearchURL

class EuroparlSearch(BaseSearchURL):

    """
    Class for building search URLs for the European Parliament's 'Think Tank' website, extending BaseSearchURL.
    """

    valid_publication_types = {
    'AT_A_GLANCE' : 'At a Glance',
    'BRIEFING' : 'Briefing',
    'FACT_SHEET' : 'EU Fact Sheets',
    'IN_DEPTH_ANALYSIS' : 'In-Depth Analysis',
    'STUDY' : 'Study'
    }

    def __init__(self):

        """
        Initialize an instance of the URL builder for the European Parliament search interface.
        Search parameters are set to their default (None or empty lists).
        """
         
        super().__init__(base_url = 'https://www.europarl.europa.eu/thinktank/en/research/advanced-search/pdf?')

        self.publication_types = []
        self.format = None


    def set_publication_type (self, publication_types):

        """
        Applies one or more publication type filters to the search results.
        Raises an error if any provided type is invalid.

        :param publication_types: A space-separated string of keys from valid_publication_types.
        """
         
        for type in publication_types.split():
            if type not in self.valid_publication_types:
                raise ValueError(f"Invalid type: '{publication_type}'. Must be one of: {list(self.valid_publication_types.keys())}")
            else:
                self.publication_types.append(type)

    def build(self):

        """
        Constructs the final URL string using all parameters set so far.

        :return: A fully-formed search URL for the European Parliament's 'Think Tank' website.
        """

        url = self.BASE_URL
        url += f'textualSearch={"+".join(self.text)}'
        if self.date_range[0]:
            url += f'&startDate={self.date_range[0][:2]}%2F{self.date_range[0][2:4]}%2F{self.date_range[0][4:]}'
        if self.date_range[1]:
            url += f'&endDate={self.date_range[1][:2]}%2F{self.date_range[1][2:4]}%2F{self.date_range[1][4:]}'
        if self.publication_types:
            for type in self.publication_types:
                url += f'&publicationTypes={type}'

        return url
