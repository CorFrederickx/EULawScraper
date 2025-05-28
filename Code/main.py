"""main function to execute a selected module"""

from eur_lex import run_eur_lex
from european_commission import run_european_commission
from european_environment_agency import run_EEA
from european_parliament_think_thank import run_europarl


def main():

    """
    Presents the user with a list of available websites from which documents can be scraped.
    Based on the user's input, it runs the appropriate run_x.py file.
    If the user's input is invalid, it notifies the user of the error. 
    """

    choices = {
        "eurlex": run_eur_lex.scrape_docs,
        "commission": run_european_commission.scrape_docs,
        "eea": run_EEA.scrape_docs,
        "europarl": run_europarl.scrape_docs
    }

    print("Available modules:")
    for key in choices:
        print(f"- {key}")

    selected = input("Enter the module to run: ").strip().lower()

    if selected in choices:
        choices[selected]()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
