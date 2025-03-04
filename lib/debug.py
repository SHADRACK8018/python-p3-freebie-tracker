#!/usr/bin/env python3

from models import Company, Dev, Freebie, session

def fetch_dev_by_name(name):
    
    dev = session.query(Dev).filter_by(name=name).first()
    if dev is None:
        print(f"No developer found with the name: {name}")
    return dev


def fetch_freebie():
    
    freebie = session.query(Freebie).first()
    if freebie is None:
        print("No freebies found in the database.")
    return freebie


def fetch_oldest_company():
    
    oldest_company = Company.oldest_company()
    if oldest_company is None:
        print("No companies found in the database.")
    return oldest_company


def main():
    
    # interactive debugger session
    import ipdb; ipdb.set_trace()

    # Fetching Developer (Alice)
    dev = fetch_dev_by_name('Alice')
    if dev:
        print(f"Developer: {dev.name}")
        print("Freebies associated with Alice:")
        for freebie in dev.freebies:
            print(freebie.print_details())

    # Fetching Freebie and print its details
    freebie = fetch_freebie()
    if freebie:
        print(f"Freebie details: {freebie.print_details()}")

    # Finding the oldest company and print its details
    oldest_company = fetch_oldest_company()
    if oldest_company:
        print(f"Oldest company: {oldest_company.name}, Founded in {oldest_company.founding_year}")

    # Closes the session after all operations
    session.close()


if __name__ == "__main__":
    main()
