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


## cheat sheet of the input you can use:

## Eurlex

| Parameter Category | Parameter Key        | Description                 |
| :----------------- | :--------------------- | :-------------------------- |
| **Collections** | `ALL_ALL`              | All                         |
|                    | `TREATIES`             | Treaties                    |
|                    | `LEGISLATION`          | Legal acts                  |
|                    | `CONSLEG`              | Consolidated texts          |
|                    | `EU_CASE_LAW`          | Case-law                    |
|                    | `INTER_AGREE`          | International agreements    |
|                    | `PRE_ACTS`             | Preparatory documents       |
|                    | `EFTA`                 | EFTA documents              |
|                    | `LEGAL_PROCEDURE`      | Lawmaking procedures        |
|                    | `PAR_QUESTION`         | Parliamentary questions     |
|                    | `MNE`                  | National transposition      |
|                    | `NAT_CASE_LAW`         | National case-law           |
|                    | `JURE`                 | JURE case-law              |
| **Types of Act** | `regulation`           | Regulation                  |
|                    | `directive`            | Directive                   |
|                    | `decision`             | Decision                    |
|                    | `courtCase`            | EU Court Case               |
|                    | `comJoin`              | COM and JOIN documents      |
|                    | `secSwd`               | SEC or SWD documents        |
| **Authors** | `council`              | Council of the European Union |
|                    | `auditors`             | Court of Auditors           |
|                    | `cb`                   | European Central Bank       |
|                    | `commission`           | European Commission         |
|                    | `regionCommittee`      | European Committee of the Regions |
|                    | `euCouncil`            | European Council            |
|                    | `ecoCommitee`          | European Economic and Social Committee |
|                    | `ep`                   | European Parliament         |
|                    | `euParlAndCouncil`     | European Parliament and Council |
|                    | `nationalCourt`        | National Courts of Justice  |
| **Date Types** | `ALL`                  | All dates                   |
|                    | `DD`                   | Date of document            |
|                    | `PD`                   | Date of publication         |
|                    | `IF`                   | Date of effect              |
|                    | `EV`                   | Date of end of validity     |
|                    | `NF`                   | Date of notification        |
|                    | `SG`                   | Date of signature           |
|                    | `TP`                   | Date of transposition       |
|                    | `LO`                   | Date lodged                 |
|                    | `DH`                   | Delivery date               |
|                    | `DL`                   | Date of deadline            |
|                    | `RP`                   | Reply date                  |
|                    | `VO`                   | Date of vote                |
|                    | `DB`                   | Date of debate              |

## European Commission

| Parameter Category | Parameter Key | Description   |
| :----------------- | :------------ | :------------ |
| **Dates** | `*`           | All           |
|                    | `-7`          | Last week     |
|                    | `-31`         | Last month    |
|                    | `-365`        | Last year     |
| **Languages** | `bg`          | Bulgarski     |
|                    | `cs`          | Cestina       |
|                    | `da`          | Dansk         |
|                    | `de`          | Deutsch       |
|                    | `et`          | Eesti Keel    |
|                    | `el`          | Greek         |
|                    | `en`          | English       |
|                    | `es`          | Espanol       |
|                    | `fr`          | Francais      |
|                    | `ga`          | Gaeilge       |
|                    | `hr`          | Hrvatski      |
|                    | `it`          | Italiano      |
|                    | `lv`          | Latviesu Valoda |
|                    | `lt`          | Lietuviu Kalba |
|                    | `hu`          | Magyar        |
|                    | `mt`          | Malti         |
|                    | `nl`          | Nederlands    |
|                    | `pl`          | Polski        |
|                    | `pt`          | Portugues     |
|                    | `ro`          | Romana        |
|                    | `sk`          | Slovencina    |
|                    | `sl`          | Slovenscina   |
|                    | `fi`          | Suomi         |
|                    | `sv`          | Svenska       |
|                    | `ot`          | Other         |
| **Formats** | `*`           | All           |
|                    | `htm`         | Web           |
|                    | `doc`         | Word          |
|                    | `xls`         | Excel         |
|                    | `pdf`         | PDF           |
|                    | `ppt`         | Powerpoint    |

## EEA

| Parameter Category | Parameter Key             | Description                        |
| :----------------- | :-------------------------- | :--------------------------------- |
| **Topics** |                             | Agriculture and food               |
|                    |                             | Air pollution                      |
|                    |                             | Bathing water quality              |
|                    |                             | Biodiversity                       |
|                    |                             | Bioeconomy                         |
|                    |                             | Buildings and construction         |
|                    |                             | Chemicals                          |
|                    |                             | Circular economy                   |
|                    |                             | Climate change adaptation          |
|                    |                             | Climate change mitigation          |
|                    |                             | Electric vehicles                  |
|                    |                             | Energy                             |
|                    |                             | Energy efficiency                  |
|                    |                             | Environmental health impacts       |
|                    |                             | Environmental inequalities        |
|                    |                             | Extreme weather                    |
|                    |                             | Fisheries and aquaculture          |
|                    |                             | Forests and forestry               |
|                    |                             | Industry                           |
|                    |                             | Land use                           |
|                    |                             | Nature protection and restoration  |
|                    |                             | Nature-based solutions             |
|                    |                             | Noise                              |
|                    |                             | Plastics                           |
|                    |                             | Pollution                          |
|                    |                             | Production and consumption         |
|                    |                             | Renewable energy                   |
|                    |                             | Resource use and materials         |
|                    |                             | Road transport                     |
|                    |                             | Seas and coasts                    |
|                    |                             | Soil                               |
|                    |                             | Sustainability challenges          |
|                    |                             | Sustainability solutions           |
|                    |                             | Sustainable finance                |
|                    |                             | Textiles                           |
|                    |                             | Transport and mobility             |
|                    |                             | Urban sustainability               |
|                    |                             | Waste and recycling                |
|                    |                             | Water                              |
| **Websites** | `cca`                       | Climate Adaptation Platform        |
|                    | `bise`                      | Biodiversity Information System for Europe |
|                    | `etc`                       | European Environment Information and Observation Network (Eionet) |
|                    | `eea`                       | European Environment Agency        |
| **Time Periods** |                             | All time                           |
|                    |                             | Last week                          |
|                    |                             | Last month                         |
|                    |                             | Last 3 months                      |
|                    |                             | Last year                          |
|                    |                             | Last 2 years                       |
|                    |                             | Last 5 years                       |
| **Countries** |                             | Albania                            |
|                    |                             | Austria                            |
|                    |                             | Belgium                            |
|                    |                             | Bosnia and Herzegovina             |
|                    |                             | Bulgaria                           |
|                    |                             | Croatia                            |
|                    |                             | Cyprus                             |
|                    |                             | Czechia                            |
|                    |                             | Denmark                            |
|                    |                             | Estonia                            |
|                    |                             | Finland                            |
|                    |                             | France                             |
|                    |                             | Germany                            |
|                    |                             | Greece                             |
|                    |                             | Hungary                            |
|                    |                             | Iceland                            |
|                    |                             | Ireland                            |
|                    |                             | Italy                              |
|                    |                             | Kosovo                             |
|                    |                             | Latvia                             |
|                    |                             | Liechtenstein                      |
|                    |                             | Lithuania                          |
|                    |                             | Luxembourg                         |
|                    |                             | Malta                              |
|                    |                             | Montenegro                         |
|                    |                             | Netherlands                        |
|                    |                             | North Macedonia                    |
|                    |                             | Norway                             |
|                    |                             | Poland                             |
|                    |                             | Portugal                           |
|                    |                             | Romania                            |
|                    |                             | Serbia                             |
|                    |                             | Slovakia                           |
|                    |                             | Slovenia                           |
|                    |                             | Spain                              |
|                    |                             | Sweden                             |
|                    |                             | Switzerland                        |
|                    |                             | Türkiye                            |
| **Languages** | `en`                        | English (en)                       |
|                    | `ar`                        | العربية (ar)                       |
|                    | `sr`                        | Српски (sr)                       |
|                    | `sq`                        | Shqip (sq)                         |
|                    | `bg`                        | Български (bg)                     |
|                    | `bs`                        | bosanski (bs)                      |
|                    | `cs`                        | čeština (cs)                       |
|                    | `hr`                        | Hrvatski (hr)                      |
|                    | `da`                        | dansk (da)                         |
|                    | `nl`                        | Nederlands (nl)                    |
|                    | `el`                        | ελληνικά (el)                      |
|                    | `et`                        | eesti (et)                         |
|                    | `fi`                        | Suomi (fi)                         |
|                    | `fr`                        | Français (fr)                      |
|                    | `ga`                        | Gaeilge (ga)                       |
|                    | `de`                        | Deutsch (de)                       |
|                    | `hu`                        | magyar (hu)                        |
|                    | `is`                        | Íslenska (is)                       |
|                    | `it`                        | italiano (it)                      |
|                    | `lv`                        | Latviešu (lv)                      |
|                    | `lt`                        | lietuvių (lt)                      |
|                    | `mk`                        | македонски (mk)                    |
|                    | `mt`                        | Malti (mt)                         |
|                    | `no`                        | Norsk (no)                         |
|                    | `pl`                        | polski (pl)                        |
|                    | `pt`                        | Português (pt)                     |
|                    | `ro`                        | Română (ro)                        |
|                    | `ru`                        | русский (ru)                       |
|                    | `sk`                        | slovenčina (sk)                    |
|                    | `sl`                        | Slovenščina (sl)                   |
|                    | `es`                        | Español (es)                       |
|                    | `sv`                        | Svenska (sv)                       |
|                    | `tr`                        | Türkçe (tr)                        |
| **Content Types** |                             | Adaptation option                  |
|                    |                             | Article                            |
|                    |                             | Briefing                           |
|                    |                             | Case study                         |
|                    |                             | Chart (interactive)                |
|                    |                             | Collection                         |
|                    |                             | Country fact sheet                 |
|                    |                             | Dashboard                          |
|                    |                             | Data set                           |
|                    |                             | Event                              |
|                    |                             | External data reference            |
|                    |                             | FAQ                                |
|                    |                             | Figure (chart/map)                 |
|                    |                             | File                               |
|                    |                             | Funding oportunity                 |
|                    |                             | Glossary term                      |
|                    |                             | Guidance                           |
|                    |                             | Indicator                          |
|                    |                             | Infographic                        |
|                    |                             | Information portal                 |
|                    |                             | Link                               |
|                    |                             | Map (interactive)                  |
|                    |                             | Mission story                      |
|                    |                             | Mission tool                       |
|                    |                             | News                               |
|                    |                             | Organisation                       |
|                    |                             | Publication reference              |
|                    |                             | Report                             |
|                    |                             | Research and knowledge project     |
|                    |                             | Subsite                            |
|                    |                             | Tool                               |
|                    |                             | Topic page                         |
|                    |                             | Video                              |
|                    |                             | Webpage                            |

## Europarl

| Parameter Category    | Parameter Key        | Description        |
| :-------------------- | :--------------------- | :----------------- |
| **Publication Types** | `AT_A_GLANCE`          | At a Glance        |
|                       | `BRIEFING`             | Briefing           |
|                       | `FACT_SHEET`           | EU Fact Sheets     |
|                       | `IN_DEPTH_ANALYSIS`    | In-Depth Analysis  |
|                       | `STUDY`                | Study              |

