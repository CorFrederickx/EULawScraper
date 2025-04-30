# EULawScraper
Searching and scraping European legislation

This repository combines Python code allows you to mimic the behaviour of the search engines of several official websites of the European Union, and scrape the found legislation from the web. These websites are:

1. The advanced search of [EUR-Lex](https://eur-lex.europa.eu/advanced-search-form.html)

2. The search box that you can find on the different websites of the [European Commission](https://commission.europa.eu/index_en?wt-search=yes)

3. The advanced search on the website of the [European Environment Agency](https://www.eea.europa.eu/en/advanced-search?)

4. The advanced search of the [Think Thank of the European Parliament](https://www.europarl.europa.eu/thinktank/en/research/advanced-search)

How it works:

In the code folder you can find separate folders per website, each containing search, scraper and run file. The search file builds a url that leads to the search results page, which can be scraped by the scraper file. The run file takes the search parameters as input and combines the functionalities of the two other files.

An independent scraper.py file and a search.py file contain some functionalities that appear in every case and don't have to be repeated everytime.

(more in depth about the websites themselves?)

use:

When running main.py file that's also in the code folder, you will be asked to make a choice between the four different modules. 
Which website do you want to collect documents from?

Once you've decided, you will be asked to provide some search parameters, as well as details about the where you want the scraped documents to be stored. Enter an empty string if you do not want to specify a certain parameter.

