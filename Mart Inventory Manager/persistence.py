import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, branche):
        self.id = id            # Unique identifier for the employee
        self.name = name        # Employee's name
        self.salary = salary    # Employee's salary
        self.branche = branche  # Foreign key to the Branch table

    def __repr__(self):
        return f"Employee(id={self.id}, name={self.name}, salary={self.salary}, branche_id={self.branche_id})"

 
class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id                        # Unique identifier for the supplier
        self.name = name                    # Supplier's name
        self.contact_information = contact_information  # Supplier's contact details (e.g., email, phone number)

    def __repr__(self):
        return f"Supplier(id={self.id}, name={self.name}, contact_information={self.contact_information})"


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id            # Unique identifier for the product
        self.description = description  # Product description
        self.price = price      # Product price
        self.quantity = quantity  # Quantity of the product available

    def __repr__(self):
        return f"Product(id={self.id}, description={self.description}, price={self.price}, quantity={self.quantity})"


class Branche(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id                    # Unique identifier for the branch
        self.location = location        # Location of the branch (city, country, etc.)
        self.number_of_employees = number_of_employees  # Number of employees in the branch

    def __repr__(self):
        return f"Branch(id={self.id}, location={self.location}, number_of_employees={self.number_of_employees})"

class Activitie(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id      # Foreign key to Product
        self.quantity = quantity          # Quantity of the product involved in the activity
        self.activator_id = activator_id  # ID of the employee who initiated the activity (could be linked to Employee)
        self.date = date                  # Date when the activity took place

    def __repr__(self):
        return f"Activity(product_id={self.product_id}, quantity={self.quantity}, activator_id={self.activator_id}, date={self.date})"

 
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.cursor = self._conn.cursor()
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    
 
# singleton
repo = Repository()
atexit.register(repo._close)