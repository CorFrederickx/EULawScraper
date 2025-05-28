"""mimicking the Advanced Search of the EUR-Lex website"""

from search import BaseSearchURL

class GetAdvancedSearchURL(BaseSearchURL):
    
    """Class for building search URLs. Builds on the abstract base class BaseSearchURL"""

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

        This sets up all possible search parameters as None or empty lists, ready to be set using the following functions.
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
        #self.document_languages = []
    
    # collection
    def set_collection(self, collection: str):

        """
        Checks if the collection you want to search in belongs to the valid options. These are listed in the above valid_collections dictionary, also in the cheatsheet.
        If not valid, an error is raised.
        If valid, the right domain is also set, based on the chosen collection.

        :param collection: The collection you want to search in.
        """

        if collection not in self.valid_collections:
            raise ValueError(f"Invalid collection: '{collection}'. Must be one of: {list(self.valid_collections.keys())}")
        self.collection = collection
        self.domain = self.domain = 'EU_LAW' if collection in list(self.valid_collections)[:10] else 'NATIONAL_LAW'

    def set_multiple_collections(self, collections: list[str]):

        """
        Checks if the collections you want to search in belong to the valid options. These are listed in the above valid_collections dictionary, also in the cheatsheet.
        If not valid, an error is raised.

        :param collections: A python list of multiple collections to search within. 
        """

        for collection in collections:
            if collection not in self.valid_collections:
                raise ValueError(f"Invalid collection: '{collection}'. Must be one of: {list(self.valid_collections.keys())}")
            self.collections.append(collection)


    # text search:
    def set_first_text(self, text, scope='ti-te'):

        """
        Defines the search text and its scope (title, text, or both). Special characters like quotes and question marks are URL-encoded.

        :param text: Search terms (use quotation marks for exact match, '?' or '*' for wildcards).
        :param scope: Where to search: in the title ('ti'), text ('te') or both ('ti-te')
        """

        for term in text.split():
            encoded_term = term
            if '"' in encoded_term: # exact match case (quotation marks around text)
                encoded_term = encoded_term.replace('"', '%22')
            if '?' in encoded_term:
                encoded_term = encoded_term.replace('?', '%3F') # varying text case (contains question mark (or asterisk, but use of asterisk does not change anything in the URL))
            self.text_params_0.append(encoded_term)
        self.text_scope_0 = scope

    def set_extra_text(self, text, boolean_operator='and', scope='ti-te'):

        """
        Defines additional search text to refine the query. Works in combination with the first search text, connected by a boolean operator.

        :param text: Additional search terms.
        :param boolean_operator: Logical connector between first and extra text ('and', 'or', 'not').
        :param scope: Search scope (title, text, or both). Same options as `set_first_text`.
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
    
    # document reference
    def set_document_year (self, year: int):
        """
        Sets the year of the document.

        :param year: A four-digit integer representing the document's year.
        """
        self.year = year
    
    def set_document_number (self, document_number: int):
        self.document_number = document_number

    def set_type_of_act(self, types_of_act: str):
        for type in types_of_act:
            if type not in self.valid_types_of_act:
                raise ValueError(f"Invalid type: '{type}'. Must be one of: {list(self.valid_types_of_act.keys())}")
            self.type_of_act.append(type)

    # Author of the document
    def set_author (self, author):
        """
        Specifies the author of the document. Must match an author in the `valid_authors` dictionary.

        :param author: A valid author as a string.
        """

        if author not in self.valid_authors:
            raise ValueError(f"Invalid author: '{author}'. Must be one of: {list(self.valid_authors.keys())}")
        self.author = author

    # Search by CELEX number
    def set_CELEX_number (self, celex: str):
        """
        Sets the CELEX number to search for. Automatically URL-encodes '?' and appends an '*' if not present.

        :param celex: CELEX number as a string.
        """

        if '?' in celex:
                celex = celex.replace('?', '%3F')
        if not celex.endswith('*'):
            celex += '*'

        self.CELEX_number = celex
    
    # search by date
    def set_date_range(self, date_type, start_date, end_date):
       
       """
       Sets a date range filter for the search.

       :param date_type: Type of date to filter by (must be in `valid_date_types dictionary`).
       :param start_date: Start of the date range, as a string in ddmmyyyy format.
       :param end_date: End of the date range, as a string in ddmmyyyy format. Same as start_date when looking for a specific day.
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
        Filters documents by EUROVOC labels.
        :param EUROVOC_descriptor: A string identifier for the theme a document belongs to.
        """

        self.theme = EUROVOC_descriptor

    def build(self):

        """
        Construct the final search URL based on all the parameters set.

        Returns:
            A string containing the complete, encoded EUR-Lex advanced search link.
        """

        url = self.BASE_URL + '&lang=en&type=advanced'  # add static parameters

        # collection
        if self.collection is not None:
            url += f'&SUBDOM_INIT={self.collection}&DTS_SUBDOM={self.collection}&DTS_DOM={self.domain}'
        if self.collections:
            url += f'&dom={"%2C".join(self.collections)}'
            
        # text
        if self.text_scope_0 and self.text_params_0:
            url += f'&textScope0={self.text_scope_0}&andText0={"+".join(self.text_params_0)}'

        if self.text_scope_1 and self.text_params_1:
            url += f'&textScope1={self.text_scope_1}&{self.boolean_operator}Text1={"+".join(self.text_params_1)}'

        # document reference
        if self.year is not None:
            url += f'&DTA={self.year}'
        if self.document_number is not None:
            url += f'&DTN={self.document_number}'
        if self.type_of_act:
            url += f'&DB_TYPE_OF_ACT={"%2C".join(self.type_of_act)}'

        # author of the document
        if self.author:
            url += f'&DB_AUTHOR={self.author}'

        # CELEX number
        if self.CELEX_number:
            url += f'&or0=DN%3D{self.CELEX_number}%2C'

        # date range
        if self.date_range and self.date_type:
            url += f'&date0={self.date_type}%3A{self.date_range[0]}%7C{self.date_range[1]}'

        # theme
        if self.theme:
            url += f'&DC_CODED={self.theme}'

        # language(s)
        #if self.document_languages:
        #   url += f'&wh0=andCOMPOSE%3D{"%3BCOMPOSE%3D".join(self.document_languages)}'

        return url
