from models import (Base, session, Brands, Product, engine)

import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nWelcome to Lawrence's Inventory Application
            \nHere are your choices:
            \rN) New Product
            \rV) View a Product by ID
            \rA) Product Analysis
            \rB) Backup the Database
            \rQ) Quit the Application
        ''')
        choice = input('\n> ')
        choice = choice.upper()
        if choice in ['N', 'V', 'A', 'B', 'Q']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above (N, V, A, B, or Q)
            \rPress enter to try again.''')


def add_csv_brands():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = row[0]
                new_brand = Brands(brand_name=brand_name)
                session.add(new_brand)
        session.commit()


def add_csv_inventory():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_quantity = row[2]
                product_price = row[1]
                date_updated = row[3]
                brand_id = session.query(Brand).filter_by(brand_name=row['brand_name']).one().brand_id)
                new_product = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
            session.commit()



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    menu()


## UPNEXT: STEP 14