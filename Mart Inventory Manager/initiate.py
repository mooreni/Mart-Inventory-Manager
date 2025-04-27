from dbtools import orm
from persistence import *
import sys
import os

def add_branche(splittedline: list[str]):
    # Ensure proper data types by casting
    branch_dto = Branche(
        id=int(splittedline[0]),  # Assuming id should be an integer
        location=splittedline[1],  # Location is a string
        number_of_employees=int(splittedline[2])  # Assuming this should be an integer
    )
    
    # Create the DAO for the Branch DTO
    branch_dao = Dao(Branche, repo._conn)
    
    # Insert the branch DTO into the database
    branch_dao.insert(branch_dto)


def add_supplier(splittedline: list[str]):
    # Ensure proper data types by casting
    supplier_dto = Supplier(
        id=int(splittedline[0]),  # Assuming id is an integer
        name=splittedline[1],  # Name is a string
        contact_information=splittedline[2]  # Assuming contact info is a string, could be empty
    )

    # Create the DAO for the Supplier DTO
    supplier_dao = Dao(Supplier, repo._conn)

    # Insert the supplier DTO into the database
    supplier_dao.insert(supplier_dto)

def add_product(splittedline: list[str]):
    # Ensure proper data types by casting
    product_dto = Product(
        id=int(splittedline[0]),  # Assuming id is an integer
        description=splittedline[1],  # Description is a string
        price=float(splittedline[2]),  # Price is a real number (float)
        quantity=int(splittedline[3])  # Quantity is an integer
    )

    # Create the DAO for the Product DTO
    product_dao = Dao(Product, repo._conn)

    # Insert the product DTO into the database
    product_dao.insert(product_dto)

def add_employee(splittedline: list[str]):
    # Ensure proper data types by casting
    employee_dto = Employee(
        id=int(splittedline[0]),  # Assuming id is an integer
        name=splittedline[1],  # Name is a string
        salary=float(splittedline[2]),  # Salary is a real number (float)
        branche=int(splittedline[3])  # Branche id is an integer (foreign key reference)
    )

    # Create the DAO for the Employee DTO
    employee_dao = Dao(Employee, repo._conn)

    # Insert the employee DTO into the database
    employee_dao.insert(employee_dto)


adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    # uncomment if needed
    if os.path.isfile("bgumart.db"):
         os.remove("bgumart.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)