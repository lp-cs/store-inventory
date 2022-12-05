from models import (Base, session, Brands, Product, engine)

from datetime import datetime
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


def add_csv():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data) ## This is the Header
        for row in data:
            brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = row[0]
                new_brand = Brands(brand_name=brand_name)
                session.add(new_brand)
        session.commit()

    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)  ## This is the Header
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_quantity = clean_quantity(row[2])
                product_price = clean_product_price(row[1])
                date_updated = clean_date(row[3])
                brand_id = session.query(Brands).filter(Brands.brand_name == row[4]).one().brand_id
                new_product = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
            session.commit()


def clean_product_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
                \n***** ID ERROR ********
                \rThe ID should be a number.
                \rPress enter to try again
                \r***********************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
                \n***** ID ERROR ********
                \rOptions: {options}
                \rPress enter to try again
                \r***********************''')
            return


def clean_brand_id(id_str, options):
    try:
        brand_id = int(id_str)
    except ValueError:
        input('''
                \n***** ID ERROR ********
                \rThe ID should be a number.
                \rPress enter to try again
                \r***********************''')
        return
    else:
        if brand_id in options:
            return brand_id
        else:
            print(f'''
                \n***** ID ERROR ********
                \rPress enter to try again
                ''')
            next(session.query(Brands).order_by(Brands.brand_id))  ## This is the Header
            for brand in session.query(Brands).order_by(Brands.brand_id):
                print(f'{brand.brand_id}) {brand.brand_name}')
            print('\r***********************')
            return


def clean_product_price(price_str):
    stripped_price = price_str.strip("$")
    price_float = float(stripped_price)
    return int(price_float * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime(year, month, day)
    except ValueError:
        input('''
            \n***** DATE ERROR *****
            \rPress enter to try again
            \r**********************''')
        return
    else:
        return return_date


def find_brand_name(brand_id):
    brand = session.query(Brands).filter(Brands.brand_id == brand_id).first()
    return(brand.brand_name)


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
                    \n***** PRICE ERROR *****
                    \rThe price should be a number without a currency symbol.
                    \r Ex: 10.99
                    \rPress enter to try again
                    \r***********************''')
    else:
        return int(price_float * 100)


def clean_quantity(quantity):
    try:
        quantity = int(quantity)
    except ValueError:
        input('''
            \n********* QUANTITY ERROR *******
            \rThe quantity should be a whole positive number (Ex. 4).
            \rPress enter to try again.
            \r********************************''')
    else:
        return(quantity)


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'N':
            product_name = input('What is the name of the product? ')
            price_error = True
            while price_error:
                product_price = input('How much us the product? ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                product_quantity = input('How many products are available? ')
                product_quantity = clean_quantity(product_quantity)
                if type(product_quantity) == int:
                    quantity_error = False
            date_updated = datetime.now()
            print('Please select a brand from the following: ')
            brand_id_options = ['X']
            for brand in session.query(Brands).order_by(Brands.brand_id):
                print(f'{brand.brand_id}) {brand.brand_name}')
                brand_id_options.append(brand.brand_id)
            brand_id_error = True

            while brand_id_error:
                brand_id_choice = input("Please choose the number for the corresponding brand or press 'X' if the brand is not listed. ")
                if brand_id_choice.upper() == 'X':
                    brand_id_choice = brand_id_choice.upper()
                else:
                    brand_id_choice = clean_brand_id(brand_id_choice, brand_id_options)
                brand_id_error = False

                brand_choice_error = True
                while brand_choice_error:
                    if type(brand_id_choice) == int:
                        new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id_choice)

                    elif brand_id_choice == 'X':
                        brand_in_db_error = True
                        while brand_in_db_error:
                            new_brand = input("What is the name of the brand? ")
                            brand_in_db = session.query(Brands).filter(Brands.brand_name == new_brand).one_or_none()
                            if brand_in_db == None:
                                new_brand = Brands(brand_name=new_brand)
                                session.add(new_brand)
                                session.commit()
                                new_product = Product(product_name=product_name, product_price=product_price,
                                                      product_quantity=product_quantity, date_updated=date_updated,
                                                      brand_id=new_brand.brand_id)
                                print(f'{new_brand} has been added')
                                time.sleep(1.5)
                                brand_in_db_error = False
                            else:
                                print(f'{new_brand} already exist. Please try again!')
                    else:
                        break

                    session.add(new_product)
                    session.commit()
                    print(f'{product_name} has been added')
                    time.sleep(1.5)
                    brand_choice_error = False


        elif choice == 'V':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                                \nID Options: {id_options}
                                \rEnter a product's ID number: ''')
                id_choice = clean_product_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id == id_choice).first()
            print(f'''
            \n*** {the_product.product_name} ***
                \rPrice: ${the_product.product_price/100:.2f}
                \rQuantity: {the_product.product_quantity}
                \rBrand: {find_brand_name(the_product.brand_id)}
                \rDate Updated: {the_product.date_updated}''')

        elif choice == 'A':
            pass
        elif choice == 'B':
            pass
        else:
            print('Closing App. Goodbye!')
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()


## UPNEXT: STEP 15