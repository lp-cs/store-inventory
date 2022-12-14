from models import (Base, session, Brands, Product, engine)

from collections import Counter

import datetime
import csv
import time

from statistics import median, mean, mode


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
            \rPlease choose one of the options (N, V, A, B, or Q)
            \rPress enter to try again.''')


def submenu():
    while True:
        print('''
            E) Edit Product
            D) Delete Product
            Q) Return to Main Menu''')
        choice = input('\nWhat would you like to do? ')
        if choice.upper() in ['E', 'D', 'Q']:
            return choice.upper()
        else:
            input('''
                \rPlease choose one of the options (E,D, or Q)
                \rPress enter to try again.''')



def add_csv():
    add_csv_brands()
    add_csv_products()


def add_csv_brands():
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


def add_csv_products():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)  ## This is the Header
        for row in data:
            product_name = row[0]
            product_quantity = clean_quantity(row[2])
            product_price = clean_product_price(row[1])
            date_updated = clean_date(row[3])
            brand_id = session.query(Brands).filter(Brands.brand_name == row[4]).one().brand_id
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                new_product = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
            elif product_in_db.date_updated < date_updated:
                product_in_db.product_quantity = product_quantity
                product_in_db.product_price = product_price
                product_in_db.date_updated = date_updated
                brand_in_db = session.query(Brands).filter(Brands.brand_name == row[4]).one_or_none()
                if brand_in_db == None:
                    new_brand = Brands(brand_name=row[4])
                    session.add(new_brand)
                product_in_db.brand_id = find_brand_id(row[4])
        session.commit()


def clean_product_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        print('Invalid Entry. The ID should be a number.')
        return
    else:
        if product_id in options:
            return product_id
        else:
            print(f'Invalid Entry. Options: {options}')
            return


def clean_brand_id(id_str, options):
    try:
        brand_id = int(id_str)
    except ValueError:
        print('Invalid entry. Please Try Again!')
        return
    else:
        if brand_id in options:
            return brand_id
        else:
            print('Invalid entry. Please Try Again!')
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
        return_date = datetime.date(year, month, day)
    except ValueError:
        print('Invalid date format. Please Try Again!')
        return
    else:
        return return_date


def find_brand_name(brand_id):
    brand = session.query(Brands).filter(Brands.brand_id == brand_id).first()
    return (brand.brand_name)


def find_brand_id(brand_name):
    brand = session.query(Brands).filter(Brands.brand_name == brand_name).first()
    return (brand.brand_id)


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        print('Invalid entry. The price should be a number without a currency symbol (Ex. 8.99). Please Try Again!')
    else:
        return int(price_float * 100)


def clean_quantity(quantity):
    try:
        quantity = int(quantity)
    except ValueError:
        print('Invalid Entry. The quantity should be a whole positive number (Ex. 4). Please Try Again!')
    else:
        return(quantity)


def add_new_brand(brand_name):
    new_brand = Brands(brand_name=brand_name)
    session.add(new_brand)
    session.commit()
    print(f'{brand_name} has been added')
    return new_brand


def add_new_product(product_name, product_price, product_quantity, date_updated, brand_id):
    new_product = Product(product_name=product_name,
                          product_price=product_price,
                          product_quantity=product_quantity,
                          date_updated=date_updated,
                          brand_id=brand_id)
    session.add(new_product)
    session.commit()
    print(f'{product_name} has been added')
    return


def edit_check(column_name, current_value):
    if column_name ==  column_name == 'product_price' or 'product_quantity':
        while True:
            if column_name == 'product_price':
                changes = input(f'The price is currently {current_value/100:.2f}. Please enter the new price: ')
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
            elif column_name == 'product_quantity':
                changes = input(f'\rThe quantity is currently {current_value}. Please enter the new quantity: ')
                changes = clean_quantity(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to?')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'N':
            product_name = input('What is the name of the product? ')
            product_in_db = session.query(Product).filter(Product.product_name == product_name).one_or_none()
            if product_in_db != None:
                print(f'\n{product_in_db.product_name} Exist. Updating {product_in_db.product_name}')
                product_in_db.product_price = edit_check('product_price', product_in_db.product_price)
                product_in_db.product_quantity = edit_check('product_quantity', product_in_db.product_quantity)
                product_in_db.date_updated = datetime.now()
                session.commit()
                print(f'{product_in_db.product_name} has been updated')
                time.sleep(1)
            else:
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

                    if type(brand_id_choice) == int:
                        add_new_product(product_name, product_price, product_quantity, date_updated, brand_id_choice)
                        brand_id_error = False

                    elif brand_id_choice == 'X':
                        brand_in_db_error = True
                        while brand_in_db_error:
                            new_brand = input("What is the name of the brand? ")
                            brand_in_db = session.query(Brands).filter(Brands.brand_name == new_brand).one_or_none()
                            if brand_in_db == None:
                                new_brand = add_new_brand(new_brand)
                                add_new_product(product_name, product_price, product_quantity, date_updated, new_brand.brand_id)
                                brand_in_db_error = False
                                brand_id_error = False
                            else:
                                print(f'{new_brand} already exist. Please try again!')

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
            sub_choice = submenu()
            if sub_choice == 'E':
                print(f'\nEditing {the_product.product_name}')
                the_product.product_price = edit_check('product_price', the_product.product_price)
                the_product.product_quantity = edit_check('product_quantity', the_product.product_quantity)
                the_product.date_updated = datetime.now()
                session.commit()
                print(f'{the_product.product_name} has been updated')
                time.sleep(1)
            elif sub_choice == 'D':
                session.delete(the_product)
                session.commit()
                print('Product deleted!')
                time.sleep(1)
            elif sub_choice == 'Q':
                pass

        elif choice == 'A':
            print("Analyzing Database...")
            # What is the most expensive item in the database?
            most_expensive = session.query(Product).order_by(Product.product_price.desc()).first()
            print(f'\nThe most expensive product is: {most_expensive.product_name} \nThe price is: ${most_expensive.product_price/100:.2f}')

            # What is the least expensive item?
            least_expensive = session.query(Product).order_by(Product.product_price).first()
            print(f'\nThe least expensive product is: {least_expensive.product_name} \nThe price is: ${least_expensive.product_price/100:.2f}')

            # Which brand has the most products in the database?
            # concept from https://bobbyhadz.com/blog/python-find-most-common-element-in-list
            brand_id_in_products = []
            for product in session.query(Product):
                brand_id_in_products.append(product.brand_id)
            most_common = find_brand_name(Counter(brand_id_in_products).most_common(1)[0][0])
            print(f'\nThe most common brand is: {most_common}')

            # Which brand has the least products in the database?
            # concept from https://bobbyhadz.com/blog/python-get-least-common-element-in-list
            brand_id_in_products = []
            for product in session.query(Product):
                brand_id_in_products.append(product.brand_id)
            least_common = find_brand_name(Counter(brand_id_in_products).most_common()[-1][0])
            print(f'\nThe least common brand is: {least_common}')

            # Total number of products
            total_products = session.query(Product).count()
            print(f'\nThere are {total_products} number of products')

            inventory_prices = []
            for product in session.query(Product):
                inventory_prices.append(product.product_price)

            # Min
            min_price = min(inventory_prices)
            print(f'\nThe minimum price is ${min_price/100:.2f}')

            # Max
            max_price = max(inventory_prices)
            print(f'\nThe maximum price is ${max_price/100:.2f}')

            # Median
            median_price = median(inventory_prices)
            print(f'\nThe median price is ${median_price/100:.2f}')

            # Mean
            mean_price = mean(inventory_prices)
            print(f'\nThe average price is ${mean_price/100:.2f}')

            # Multimode
            price_mode = mode(inventory_prices)
            print(f"\nThe most often price is: ${price_mode/100:.2f}")

        elif choice == 'B':
            # https://docs.python.org/3/library/csv.html
            print("Backing up data...")

            with open('inventory_backup.csv', 'w', newline='') as csvfile:
                productwriter = csv.writer(csvfile)
                productwriter.writerow(['product_name', 'product_price', 'product_quantity', 'date_updated', 'brand_name'])
                for product in session.query(Product).order_by(Product.product_id):
                    # Product Price Convert from Cents to $
                    formatted_price = f"${product.product_price/100:.2f}"
                    # Format date from YYYY-MM-DD to MM/DD/YYYY
                    formatted_date = product.date_updated.strftime("%m/%d/%Y").replace('/0', '/').strip("0")
                    # Search brand_name from brand_id
                    brand_name_from_id = find_brand_name(product.brand_id)
                    productwriter.writerow([product.product_name, formatted_price, product.product_quantity, formatted_date, brand_name_from_id])


            with open('brands_backup.csv', 'w', newline='') as csvfile:
                brandswriter = csv.writer(csvfile)
                brandswriter.writerow(['brand_name'])
                for brand in session.query(Brands).order_by(Brands.brand_id):
                    brandswriter.writerow([brand.brand_name])

            print("Your database has been backed up!")

        else:
            print('Closing App. Goodbye!')
            app_running = False

        input("\nPress enter to return to the main menu")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()