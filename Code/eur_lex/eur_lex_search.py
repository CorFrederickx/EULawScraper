"""mimicking the Advanced Search of the EUR-Lex website"""

from search import BaseSearchURL

class EurLexSearch(BaseSearchURL):
    
    """Class for building search URLs for Eur-Lex's advanced search, extending BaseSearchURL"""

    valid_collections = {
        # EU law and case-law
        'ALL_ALL' : 'All',
        'TREATIES' : 'Treaties',
        'LEGISLATION' : 'Legal acts',
        'CONSLEG' : 'Consolidated texts',
        'EU_CASE_LAW' : 'Case-law',
        'INTER_AGREE' : 'International agreements',
        'PRE_ACTS' : 'Preparatory documents',
        'EFTA' : 'EFTA documents',
        'LEGAL_PROCEDURE' : 'Lawmaking procedures',
        'PAR_QUESTION' : 'Parliamentary questions',
        # National law and case-law
        'MNE' : 'National transposition',
        'NAT_CASE_LAW' : 'National case-law',
        'JURE' : 'JURE case-law'
    }
    
    valid_types_of_act = {
        'regulation': 'Regulation',
        'directive': 'Directive',
        'decision': 'Decision',
        'courtCase': 'EU Court Case',
        'comJoin': 'COM and JOIN documents',
        'secSwd': 'SEC or SWD documents',
    }
    
    valid_authors = {
        'council': 'Council of the European Union',
        'auditors': 'Court of Auditors',
        'cb': 'European Central Bank',
        'commission': 'European Commission',
        'regionCommittee': 'European Committee of the Regions',
        'euCouncil': 'European Council',
        'ecoCommitee': 'European Economic and Social Committee',
        'ep': 'European Parliament',
        'euParlAndCouncil': 'European Parliament and Council',
        'nationalCourt': 'National Courts of Justice'
    }

    valid_date_types = {
        'ALL': 'All dates',
        'DD': 'Date of document',
        'PD': 'Date of publication',
        'IF': 'Date of effect',
        'EV': 'Date of end of validity',
        'NF': 'Date of notification',
        'SG': 'Date of signature',
        'TP': 'Date of transposition',
        'LO': 'Date lodged',
        'DH': 'Delivery date',
        'DL': 'Date of deadline',
        'RP': 'Reply date',
        'VO': 'Date of vote',
        'DB': 'Date of debate'
    }

    def __init__(self):

        """
        Initialize an instance of the URL builder with the EUR-Lex Advanced Search base URL
        All search parameters are set to their default (None or empty lists).
        """

        super().__init__(base_url='https://eur-lex.europa.eu/search.html?')

        self.collection = None
        self.domain = None
        self.collections = []
        self.text_params_0 = []
        self.text_params_1 = []
        self.text_scope_0 = None
        self.text_scope_1 = None
        self.year = None
        self.document_number = None
        self.type_of_act = []
        self.author = None
        self.CELEX_number = None
        self.date_type = None
        self.theme = None
    
    def set_collection(self, collection: str):

        """
        Sets a single collection to search in. Also sets the domain (EU or national law).
        If the chosen collection is not a valid option, an error is raised.

        :param collection: Key from valid_collections.
        """

        if collection not in self.valid_collections:
            raise ValueError(f"Invalid collection: '{collection}'. Must be one of: {list(self.valid_collections.keys())}")
        self.collection = collection
        self.domain = self.domain = 'EU_LAW' if collection in list(self.valid_collections)[:10] else 'NATIONAL_LAW'

    def set_multiple_collections(self, collections: list[str]):

        """
        Adds multiple valid collections to the search.
        If the chosen collections are not valid options, an error is raised.

        :param collections: A list of keys from valid_collections.
        """

        for collection in collections:
            if collection not in self.valid_collections:
                raise ValueError(f"Invalid collection: '{collection}'. Must be one of: {list(self.valid_collections.keys())}")
            self.collections.append(collection)

    def set_first_text(self, text: str, scope='ti-te'):

        """
        Defines the primary search text and its scope.

        :param text: Terms to search (supporting exact matches denoted by quotation marks, and wildcards like '?' or '*').
        :param scope: Where to search: 'ti' (title), 'te' (text) or 'ti-te' (both).
        """

        for term in text.split():
            encoded_term = term
            if '"' in encoded_term: # exact match case (quotation marks around text)
                encoded_term = encoded_term.replace('"', '%22')
            if '?' in encoded_term:
                encoded_term = encoded_term.replace('?', '%3F') # varying text case (contains question mark (or asterisk, but use of asterisk does not change anything in the URL))
            self.text_params_0.append(encoded_term)
        self.text_scope_0 = scope

    def set_extra_text(self, text: str, boolean_operator='and', scope='ti-te'):

        """
        Defines additional search text, joined to the first by a boolean operator.

        :param text: Additional search terms (supporting exact matches denoted by quotation marks, and wildcards like '?' or '*').
        :param boolean_operator: Logical connectors 'and', 'or', 'not'.
        :param scope: 'ti', 'te' or 'ti-te'.
        """

        for term in text.split():
            encoded_term = term
            if '"' in encoded_term:
                encoded_term = encoded_term.replace('"', '%22')
            if '?' in encoded_term:
                encoded_term = encoded_term.replace('?', '%3F')
            self.text_params_1.append(encoded_term)
        self.boolean_operator = boolean_operator
        self.text_scope_1 = scope
    
    def set_document_year (self, year: int):

        """
        Sets the preferred publication year.

        :param year: Four digit integer.
        """

        self.year = year
    
    def set_document_number (self, document_number: int):

        """
        Sets the document number.

        :param document_number: Integer value of the document's identifier.
        """

        self.document_number = document_number

    def set_type_of_act(self, types_of_act: list):

        """
        Sets one or more types of legal acts to filter by.
        If the chosen types of acts are not valid options, an error is raised.

        :param types_of_act: List of keys from valid_types_of_act.
        """

        for type in types_of_act:
            if type not in self.valid_types_of_act:
                raise ValueError(f"Invalid type: '{type}'. Must be one of: {list(self.valid_types_of_act.keys())}")
            self.type_of_act.append(type)

    def set_author (self, author: str):
        """
        Sets the authoring institution of the document. Must match an author in the `valid_authors` dictionary.
        If the chose author is not valid, an error is raised.

        :param author: Key from valid_authors.
        """

        if author not in self.valid_authors:
            raise ValueError(f"Invalid author: '{author}'. Must be one of: {list(self.valid_authors.keys())}")
        self.author = author

    def set_CELEX_number (self, celex: str):

        """
        Sets the CELEX number. Character '*' is added automatically if missing.

        :param celex: CELEX identifier as a string.
        """

        if '?' in celex:
                celex = celex.replace('?', '%3F')
        if not celex.endswith('*'):
            celex += '*'

        self.CELEX_number = celex
    
    def set_date_range(self, date_type, start_date, end_date):
       
       """
       Applies a date filter to the search results.
       If chosen date filter is not valid, an error is raised.
       
       :param date_type: Key from valid_date_types.
       :param start_date: Start of the date range in ddmmyyyy format.
       :param end_date: End of the date range in ddmmyyyy format.
       """
       
       if date_type not in self.valid_date_types:
           raise ValueError(
               f"Invalid date type: '{date_type}'. Must be one of: {list(self.valid_date_types.keys())}"
               )
       super().set_date_range(start_date, end_date)
       self.date_type = date_type

    # search by theme
    def set_theme (self, EUROVOC_descriptor):

        """
        Filters search results by EUROVOC labels.
        :param EUROVOC_descriptor: String label from the EUROVOC taxonomy.
        """

        self.theme = EUROVOC_descriptor

    def build(self):

        """
        Constructs the final URL string using all the parameters set so far.

        :return: A fully-formed EUR-Lex advanced search URL.
        """

        url = self.BASE_URL + '&lang=en&type=advanced'  # static parameters
        if self.collection is not None:
            url += f'&SUBDOM_INIT={self.collection}&DTS_SUBDOM={self.collection}&DTS_DOM={self.domain}'
        if self.collections:
            url += f'&dom={"%2C".join(self.collections)}'
        if self.text_scope_0 and self.text_params_0:
            url += f'&textScope0={self.text_scope_0}&andText0={"+".join(self.text_params_0)}'
        if self.text_scope_1 and self.text_params_1:
            url += f'&textScope1={self.text_scope_1}&{self.boolean_operator}Text1={"+".join(self.text_params_1)}'
        if self.year is not None:
            url += f'&DTA={self.year}'
        if self.document_number is not None:
            url += f'&DTN={self.document_number}'
        if self.type_of_act:
            url += f'&DB_TYPE_OF_ACT={"%2C".join(self.type_of_act)}'
        if self.author:
            url += f'&DB_AUTHOR={self.author}'
        if self.CELEX_number:
            url += f'&or0=DN%3D{self.CELEX_number}%2C'
        if self.date_range and self.date_type:
            url += f'&date0={self.date_type}%3A{self.date_range[0]}%7C{self.date_range[1]}'
        if self.theme:
            url += f'&DC_CODED={self.theme}'

        return url
