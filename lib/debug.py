#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Creating sample data
    company1 = Company(name="Company A", founding_year=1990)
    company2 = Company(name="Company B", founding_year=2000)
    dev1 = Dev(name="Dev X")
    dev2 = Dev(name="Dev Y")

    # Add companies and devs to the session
    session.add_all([company1, company2, dev1, dev2])
    session.commit()

    # Test the give_freebie method
    freebie1 = company1.give_freebie(dev1, "T-shirt", 10)
    freebie2 = company2.give_freebie(dev2, "Sticker", 5)

    # Test the print_details method
    print(freebie1.print_details())  # Should print: Dev X owns a T-shirt from Company A

    # Test the oldest_company method
    oldest = Company.oldest_company(session)
    print(f"The oldest company is: {oldest.name}")  # Should print: The oldest company is: Company A

    # Test the received_one method
    print(dev1.received_one("T-shirt"))  # Should print: True
    print(dev2.received_one("T-shirt"))  # Should print: False

    # Test the give_away method
    dev1.give_away(dev2, freebie1)
    print(freebie1.dev.name)  # Should print: Dev Y
