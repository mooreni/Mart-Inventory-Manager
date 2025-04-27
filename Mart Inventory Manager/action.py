from persistence import *  # Assuming this imports your Repository, DTOs, and DAO helpers
import sys

def update_product_quantity(product_id: int, quantity: int):
    # Retrieve the current product
    product_dao = Dao(Product, repo._conn)
    product_list = product_dao.find(id=product_id)
    
    if not product_list:
        return  # Product does not exist, so do nothing
    
    product = product_list[0]
    current_quantity = product.quantity  # Assuming the product is returned as a list
    
    # If it's a sale, check if enough stock is available
    if quantity < 0:
        if current_quantity < abs(quantity):  # Not enough stock to sell
            return  # Ignore this sale
    
    new_quantity = current_quantity + quantity


    # Update the product's quantity
    product.quantity = new_quantity
    product_dao.update(product)  # Save back to the database

def add_activity(splittedline: list[str]):
    product_id = int(splittedline[0])  # Product ID
    quantity = int(splittedline[1])  # Quantity (positive for supply, negative for sale)
    activator_id = int(splittedline[2])  # Supplier or employee ID (depending on activity type)
    date = splittedline[3]  # Date in format YYYYMMDD

    # Update product quantity based on the activity type
    update_product_quantity(product_id, quantity)
    
    # Record the activity
    activity_dto = Activitie(product_id=product_id, quantity=quantity, activator_id=activator_id, date=date)
    activity_dao = Dao(Activitie, repo._conn)
    activity_dao.insert(activity_dto)

def main(args: list[str]):
    inputfilename: str = args[1]  # Input file containing activity data
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(", ")  # Split line by comma and space
            add_activity(splittedline)  # Process the activity based on the splitted data

if __name__ == '__main__':
    main(sys.argv)
