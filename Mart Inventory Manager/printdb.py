from persistence import *

def print_table(cursor, table_name):
    print(table_name)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def print_employees_report(conn):
    print("Employee Report")
    employee_dao = Dao(Employee, conn)
    employees = employee_dao.find_all()
    
    # Sort employees by name
    employees.sort(key=lambda e: e.name)

    # For each employee, calculate their total sales income
    for employee in employees:
        employee_name = employee.name
        # Query to calculate total sales income for this employee
        sales_income_query = """
            SELECT SUM(p.price * ABS(a.quantity)) 
            FROM activities a
            JOIN products p ON a.product_id = p.id
            WHERE a.activator_id = ? AND a.quantity < 0
        """
        cursor = conn.cursor()
        cursor.execute(sales_income_query, (employee.id,))
        sales_income = cursor.fetchone()[0] or 0  # Default to 0 if no sales found
        
        # Query to get the branch location
        cursor.execute("SELECT location FROM branches WHERE id = ?", (employee.branche,))
        branch_location = cursor.fetchone()[0]
        
        # Print the employee report in the correct format
        print(f"{employee.name} {employee.salary} {branch_location} {sales_income}")


def print_activities_report(conn):
    print("Activities Report")
    activity_dao = Dao(Activitie, conn)
    activities = activity_dao.find_all()

    for activity in activities:
        # Get product description
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM products WHERE id = ?", (activity.product_id,))
        product_description = cursor.fetchone()[0]

        # Get seller and supplier names
        if activity.quantity < 0:
            # Sale, get the employee's name and supplier as 'None'
            cursor.execute("SELECT name FROM employees WHERE id = ?", (activity.activator_id,))
            seller_name = cursor.fetchone()[0]
            supplier_name = "None"
        else:
            # Supply, get supplier's name and seller as 'None'
            cursor.execute("SELECT name FROM suppliers WHERE id = ?", (activity.activator_id,))
            supplier_name = cursor.fetchone()[0]
            seller_name = "None"

        # Print the activity in tuple format
        print(f"('{activity.date}', '{product_description}', {activity.quantity}, '{seller_name}', '{supplier_name}')")

def main():
    # Connect to the database
    conn = repo._conn
    cursor = conn.cursor()

    # Print Activities table
    cursor.execute("SELECT * FROM activities ORDER BY date")
    print_table(cursor, "Activities")

    # Print Branches table
    cursor.execute("SELECT * FROM branches ORDER BY id")
    print_table(cursor, "Branches")

    # Print Employees table
    cursor.execute("SELECT * FROM employees ORDER BY id")
    print_table(cursor, "Employees")

    # Print Products table
    cursor.execute("SELECT * FROM products ORDER BY id")
    print_table(cursor, "Products")

    # Print Suppliers table
    cursor.execute("SELECT * FROM suppliers ORDER BY id")
    print_table(cursor, "Suppliers")

    # Print the employee report
    print()
    print_employees_report(conn)

    # Print the activities report
    print()
    print_activities_report(conn)

if __name__ == '__main__':
    main()