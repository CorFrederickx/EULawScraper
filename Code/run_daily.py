
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

# instead of a user making choices, every module is run with fixed parameters
# because it does not require user interaction it can be scheduled to run on a server at set times
# scheduling can be done by adding a cron job to your crontab file (when working on a Unix based system)
# For example, after using 'crontab -e' to edit your crontab file, you can enter the command: '0 3 * * * /usr/bin/python3 /path/to/your/run_daily.py' to run your file daily at 3AM. 

def main():

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
