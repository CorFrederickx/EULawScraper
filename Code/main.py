
from eur_lex import run_eur_lex
from european_commission import run_european_commission
from european_environment_agency import run_EEA
from european_parliament_think_thank import run_europarl


def main():
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
