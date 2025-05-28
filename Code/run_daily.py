
# this script can be used to 

from unittest.mock import patch

from eur_lex import run_eur_lex
from european_commission import run_european_commission
from european_environment_agency import run_EEA
from european_parliament_think_thank import run_europarl

def run_with_inputs(func, inputs):
    inputs_iter = iter(inputs)
    with patch("builtins.input", lambda _: next(inputs_iter)):
        func()

def main():

    """
    Runs the scraping modules for all websites with pre-defined inputs, avoiding user interaction.

    This allows the scraping process to run automatically, for example via `cron` (on Unix-based systems) at regular times without manual intervention.

    An example crontab entry for daily execution at 3 AM would be:
        0 3 * * * /usr/bin/python3 /path/to/this_script.py
    """

    eurlex_inputs = [
        "LEGISLATION",                   # collection(s)
        "sheep wool",                    # search text
        "14042025",                     # start date
        "14052025",                      # end date
        "documents",                     # folder path
        "metadata"                      # metadata path
    ]
    run_with_inputs(run_eur_lex.scrape_docs, eurlex_inputs)

    commission_inputs = [
        "sheep wool",                   # search text
        "-31",                    # time period
        "documents",                   # folder path
        "*"                           # format
    ]
    run_with_inputs(run_european_commission.scrape_docs, commission_inputs)

    eea_inputs = [
        "sheep wool",                  # search text
        "Briefing",                     # content types
        "Last month",                    # time period
        "documents",                    # folder path
        "metadata"                      # metadata path
    ]
    run_with_inputs(run_EEA.scrape_docs, eea_inputs)

    europarl_inputs = [
        "sheep wool",               # search text
        "01042025",                 # start date
        "01052025",                 # end date
        "STUDY",                    # publication types
        "documents",                # folder path
        "metadata"                  # metadata path
    ]
    run_with_inputs(run_europarl.scrape_docs, europarl_inputs)

    
if __name__ == "__main__":
    main()
