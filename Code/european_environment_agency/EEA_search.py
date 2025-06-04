"""mimicking the Advanced Search of the European Environment Agency website"""

from search import BaseSearchURL

class EEASearch(BaseSearchURL):

    """
    Class for building search URLs for the EEA's advanced search, extending BaseSearchURL.
    """

    valid_topics = [
    'Agriculture and food',
    'Air pollution',
    'Bathing water quality',
    'Biodiversity',
    'Bioeconomy',
    'Buildings and construction',
    'Chemicals',
    'Circular economy',
    'Climate change adaptation',
    'Climate change mitigation',
    'Electric vehicles',
    'Energy',
    'Energy efficiency',
    'Environmental health impacts',
    'Environmental inequalities',
    'Extreme weather',
    'Fisheries and aquaculture',
    'Forests and forestry',
    'Industry',
    'Land use',
    'Nature protection and restoration',
    'Nature-based solutions',
    'Noise',
    'Plastics',
    'Pollution',
    'Production and consumption',
    'Renewable energy',
    'Resource use and materials',
    'Road transport',
    'Seas and coasts',
    'Soil',
    'Sustainability challenges',
    'Sustainability solutions',
    'Sustainable finance',
    'Textiles',
    'Transport and mobility',
    'Urban sustainability',
    'Waste and recycling',
    'Water'
]

    valid_websites = {
        'cca': 'Climate Adaptation Platform',
        'bise': 'Biodiversity Information System for Europe',
        'etc': 'European Environment Information and Observation Network (Eionet)',
        'eea': 'European Environment Agency',
        # incomplete
    }

    valid_time_periods = [
        'All time',
        'Last week',
        'Last month',
        'Last 3 months',
        'Last year',
        'Last 2 years',
        'Last 5 years',
    ]

    valid_countries = [
        'Albania', 
        'Austria', 
        'Belgium', 
        'Bosnia and Herzegovina', 
        'Bulgaria', 
        'Croatia', 
        'Cyprus', 
        'Czechia', 
        'Denmark', 
        'Estonia', 
        'Finland', 
        'France', 
        'Germany', 
        'Greece', 
        'Hungary', 
        'Iceland', 
        'Ireland', 
        'Italy', 
        'Kosovo', 
        'Latvia', 
        'Liechtenstein', 
        'Lithuania', 
        'Luxembourg', 
        'Malta', 
        'Montenegro', 
        'Netherlands', 
        'North Macedonia', 
        'Norway', 
        'Poland', 
        'Portugal', 
        'Romania', 
        'Serbia', 
        'Slovakia', 
        'Slovenia', 
        'Spain', 
        'Sweden', 
        'Switzerland', 
        'Türkiye'
    ]

    valid_languages = {
    'en': 'English (en)',
    'ar': 'العربية (ar)',
    'sr': 'Српски (sr)',
    'sq': 'Shqip (sq)',
    'bg': 'Български (bg)',
    'bs': 'bosanski (bs)',
    'cs': 'čeština (cs)',
    'hr': 'Hrvatski (hr)',
    'da': 'dansk (da)',
    'nl': 'Nederlands (nl)',
    'el': 'ελληνικά (el)',
    'et': 'eesti (et)',
    'fi': 'Suomi (fi)',
    'fr': 'Français (fr)',
    'ga': 'Gaeilge (ga)',
    'de': 'Deutsch (de)',
    'hu': 'magyar (hu)',
    'is': 'Íslenska (is)',
    'it': 'italiano (it)',
    'lv': 'Latviešu (lv)',
    'lt': 'lietuvių (lt)',
    'mk': 'македонски (mk)',
    'mt': 'Malti (mt)',
    'no': 'Norsk (no)',
    'pl': 'polski (pl)',
    'pt': 'Português (pt)',
    'ro': 'Română (ro)',
    'ru': 'русский (ru)',
    'sk': 'slovenčina (sk)',
    'sl': 'Slovenščina (sl)',
    'es': 'Español (es)',
    'sv': 'Svenska (sv)',
    'tr': 'Türkçe (tr)'
}

    valid_content_types = [
    'Adaptation option',
    'Article',
    'Briefing',
    'Case study',
    'Chart (interactive)',
    'Collection',
    'Country fact sheet',
    'Dashboard',
    'Data set',
    'Event',
    'External data reference',
    'FAQ',
    'Figure (chart/map)',
    'File',
    'Funding oportunity',
    'Glossary term',
    'Guidance',
    'Indicator',
    'Infographic',
    'Information portal',
    'Link',
    'Map (interactive)',
    'Mission story',
    'Mission tool',
    'News',
    'Organisation',
    'Publication reference',
    'Report',
    'Research and knowledge project',
    'Subsite',
    'Tool',
    'Topic page',
    'Video',
    'Webpage'
]

    def __init__(self):

        """
        Initialize an instance of the URL builder with the EEA Advanced Search base URL
        All search parameters are set to their default (None or empty lists).
        """

        super().__init__(base_url='https://www.eea.europa.eu/en/advanced-search?')

        self.initial_topic = None
        self.topics = []
        self.websites = []
        self.time_period = None
        self.countries = []
        self.content_types = []
        self.languages = []
    
    def set_initial_topic(self, topic):

        """
        Sets the primary search topic.
        If the chosen topic is not a valid option, an error is raised.

        :param topic: String from valid_topics.
        """

        if topic not in self.valid_topics:
                raise ValueError(f"Invalid type: '{topic}'. Must be one of: {list(self.valid_topics)}")
        if ' ' in topic:
            topic = topic.replace(' ', '%20')
        self.initial_topic = topic
    
    def set_topic(self, topics):

        """
        Adds one or more secondary topics to the search filter.
        If any topic is not valid, an error is raised.

        :param topics: String of space-separated topic names from valid_topics.
        """
         
        for topic in topics.split():
            if topic not in self.valid_topics:
                raise ValueError(f"Invalid type: '{topic}'. Must be one of: {list(self.valid_topics)}")
            if ' ' in topic:
                topic = topic.replace(' ', '%20')
            self.topics.append(topic)

    def set_website(self, websites):

        """
        Filters results by the source website (platform).
        If any website key is not valid, an error is raised.

        :param websites: List of keys from valid_websites.
        """

        for website in websites:
            if website not in self.valid_websites:
                raise ValueError(f"Invalid type: '{website}'. Must be one of: {list(self.valid_websites.keys())}")
            if ' ' in website:
                website = website.replace(' ', '%20')
            self.websites.append(website)

    def set_time_period(self, time_period):

        """
        Filters documents by the time period in which they were published.
        If the period is not valid, an error is raised.

        :param time_period: String from valid_time_periods.
        """

        if time_period not in self.valid_time_periods:
            raise ValueError(f"Invalid type: '{time_period}'. Must be one of: {list(self.valid_time_periods)}")
        if ' ' in time_period:
            time_period = time_period.replace(' ', '%20')
        self.time_period = time_period

    def set_countries (self, countries: list):

        """
        Filters results by countries.
        If any country is not valid, an error is raised.

        :param countries: List of country names from valid_countries.
        """

        for country in countries:
            if country not in self.valid_countries:
                raise ValueError(f"Invalid type: '{country}'. Must be one of: {list(self.valid_countries)}")
            if ' ' in country:
                country = country.replace(' ', '%20')
            self.countries.append(country)

    def set_content_type (self, content_types: str):

        """
        Filters search results by type of content (for example: report, dataset, video).
        If any content type is not valid, an error is raised.

        :param content_types: Space-separated string of types from valid_content_types.
        """

        for type in content_types.split():
            if type not in self.valid_content_types:
                raise ValueError(f"Invalid type: '{type}'. Must be one of: {list(self.valid_content_types)}")
            if ' ' in type:
                topic = topic.replace(' ', '%20')
            self.content_types.append(type)

    def set_language (self, languages: str):

        """
        Filters results by content language.
        If any language is not valid, an error is raised.

        :param languages: Space-separated string of language keys from valid_languages.
        """

        for language in languages.split():
            if language not in self.valid_languages:
                raise ValueError(f"Invalid type: '{language}'. Must be one of: {list(self.valid_languages.keys())}")
            self.languages.append(language)

    def build(self):

        """
        Constructs the final URL string using all search parameters set so far.
        (in every step an indexed filter is appended as required by the structure of the EEA search URL query)

        :return: A fully-formed EEA search URL.
        """

        url = self.BASE_URL
        filter_index = 0
        if self.text:
            url += f'q={"%20".join(self.text)}'
            url += '&size=n_10_n'
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=readingTime&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D%5Bname%5D=All&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D%5BrangeType%5D=fixed&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        # always add language first, if present
        if self.languages:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=language'
            for language in self.languages:
                url += f'&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D={language}&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        if self.time_period is not None:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=issued.date&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D={self.time_period}&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        if self.content_types:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=objectProvides'
            value_index = 0
            for content_type in self.content_types:
                url += f'&filters%5B{filter_index}%5D%5Bvalues%5D%5B{value_index}%5D={content_type}'
                value_index += 1
            url += f'&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        if self.topics:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=topic'
            for topic in self.topics:
                url += f'&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D={topic}'
            url += f'&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        if self.websites:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=cluster_name'
            for website in self.websites:
                url += f'&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D={self.valid_websites[website]}'
            url += f'&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1
        if self.countries:
            url += f'&filters%5B{filter_index}%5D%5Bfield%5D=spatial'
            for country in self.countries:
                url += f'&filters%5B{filter_index}%5D%5Bvalues%5D%5B0%5D={country}'
            url += f'&filters%5B{filter_index}%5D%5Btype%5D=any'
            filter_index += 1

        return url



