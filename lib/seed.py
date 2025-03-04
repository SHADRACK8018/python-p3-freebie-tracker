from models import Company, Dev, Freebie, session, initialize_db

def create_companies():
   
    companies = [
        Company(name="TechCorp", founding_year=1999),
        Company(name="DevGoods", founding_year=2005),
        Company(name="WebSolutions", founding_year=2010)
    ]
    return companies


def create_devs():
    
    devs = [
        Dev(name="Alice"),
        Dev(name="Bob"),
        Dev(name="Charlie")
    ]
    return devs


def seed_freebies(companies, devs):
    
    # Company1 gives freebies to Alice and Bob
    companies[0].give_freebie(devs[0], "T-Shirt", 10)
    companies[0].give_freebie(devs[1], "Mug", 5)

    # Company2 gives freebies to Alice and Charlie
    companies[1].give_freebie(devs[0], "Laptop Bag", 25)
    companies[1].give_freebie(devs[2], "T-Shirt", 10)

    # Company3 gives freebies to Bob and Charlie
    companies[2].give_freebie(devs[1], "Notebook", 15)
    companies[2].give_freebie(devs[2], "Laptop", 100)


def seed():
    
    # Initializing database (create tables if they don't exist already)
    initialize_db()

    # Creating and add companies and developers
    companies = create_companies()
    devs = create_devs()

    # Adding companies and devs to session
    session.add_all(companies + devs)
    session.commit()

    # Assigning freebies
    seed_freebies(companies, devs)

    # Commiting session to save changes to the database
    session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
