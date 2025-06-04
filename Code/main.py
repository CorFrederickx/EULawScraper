"""main function to execute a selected module"""

import logging

from eur_lex import run_eur_lex
from european_commission import run_european_commission
from european_environment_agency import run_EEA
from european_parliament_think_thank import run_europarl

def setup_logging(verbose: bool):

    """
    Configures logging. 
    If `verbose` is True, basic logging is set up to display all log messages,
    otherwise, logging remains disabled.
    """
     
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )


def main(log=False):

    """
    Displays a list of available scraper modules and prompts the user to choose one.
    Optionally enables verbose logging, which is useful for debugging or monitoring progress.
    If the user provides an invalid input, an error message is displayed.

    :param log: If True, enables verbose logging. When run from the command line, this is set via the '--log' flag.
    """

    setup_logging(log)

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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", action="store_true", help="Enable logging output")
    args = parser.parse_args()
    main(log=args.log)
