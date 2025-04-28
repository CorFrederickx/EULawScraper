from search import BaseSearchURL

class EuroparlSearch(BaseSearchURL):

    valid_publication_types = {
    'AT_A_GLANCE' : 'At a Glance',
    'BRIEFING' : 'Briefing',
    'FACT_SHEET' : 'EU Fact Sheets',
    'IN_DEPTH_ANALYSIS' : 'In-Depth Analysis',
    'STUDY' : 'Study'
    }

    def __init__(self):
        super().__init__(base_url = 'https://www.europarl.europa.eu/thinktank/en/research/advanced-search/pdf?')

        self.publication_types = []
        self.format = None


    def set_publication_type (self, publication_types):
        for type in publication_types.split():
            if type not in self.valid_publication_types:
                raise ValueError(f"Invalid type: '{publication_type}'. Must be one of: {list(self.valid_publication_types.keys())}")
            else:
                self.publication_types.append(type)

    def build(self):
        url = self.BASE_URL

        url += f'textualSearch={"+".join(self.text)}' # impossible to do a search without text

        if self.date_range[0]:
            url += f'&startDate={self.date_range[0][:2]}%2F{self.date_range[0][2:4]}%2F{self.date_range[0][4:]}'
        if self.date_range[1]:
            url += f'&endDate={self.date_range[1][:2]}%2F{self.date_range[1][2:4]}%2F{self.date_range[1][4:]}'

        if self.publication_types:
            for type in self.publication_types:
                url += f'&publicationTypes={type}'

        return url
