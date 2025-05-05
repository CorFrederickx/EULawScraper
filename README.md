# EULawScraper

Welcome to EULawScraper, a Python-based tool designed to mimic the search engines of several official European Union websites and scrape the resulting legislation from the web (including handy metadata when possible).

## Supported websites

1. The advanced search of [EUR-Lex](https://eur-lex.europa.eu/advanced-search-form.html)

2. The search box that you can find on the different websites of the [European Commission](https://commission.europa.eu/index_en?wt-search=yes)

3. The advanced search on the website of the [European Environment Agency](https://www.eea.europa.eu/en/advanced-search?)

4. The advanced search of the [Think Thank of the European Parliament](https://www.europarl.europa.eu/thinktank/en/research/advanced-search)

## How it works

Each website has its own set of files:

- **search file**: constructs a URL leading to the search results page. (by adding parameters to the url)
- **scraper file**: extracts data from the search results page.
- **run file**: takes user input for search parameters and combines the functionalities of the search and scraper files.

Additionally, there are three independent files that provide common functionalities:

- **scraper.py**: contains general scraping functions used across different modules.
- **search.py**: contains general search functions used across different modules.
- **file_utils.py**: manages the creation of folders and moving of scraped files to specified directories.

## Getting Started

Run the main.py file and:

1. **Choose a module**: select one of the four supported websites, the respective run file will be executed, so you can:
2. **Provide search parameters**: enter the required search parameters and specify the directory where you want the scraped documents to be stored. All the valid search parameters can be found in this [cheat sheet](valid_input_cheat_sheet.md). They are also specified in the different search files themselves.

Based on your input the run file will further execute, performing the search and scraping the documents. 

## Nice to know

- The website of the European Environment Agency loads dynamically. For that reason, the scraper makes use of [Selenium Webdriver](https://www.selenium.dev/documentation/webdriver/). This means that the code will automatically open a Chrome window to navigate to the right spot to scrape

- The scraper for the website of the Think Thank of the European Parliament, makes use of a pdf file that is automatically generated on the website after every search. It can be found in the upper right corner of the search results page and contains a handy overview of everything

## Good to Know

- The European Environment Agency's website loads content dynamically. To handle this, the scraper uses [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/). When the scraper runs, it will automatically launch a Chrome browser instance to navigate and extract the necessary data.

- The scraper for the European Parliament Think Tank leverages a downloadable PDF summary that is auto-generated on the website after each search. This PDF can be found in the upper right corner of the search results page and provides a concise overview of all matching documents.




