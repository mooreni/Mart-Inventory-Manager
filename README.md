# Mart Inventory Manager

A Python + SQLite tool to manage multi-branch supermarket inventory, track sales/deliveries, and generate automated reports.

## 🚀 Features
- **Database Initialization:** Builds `bgumart.db` schema for employees, suppliers, products, branches, and activities from a config file.  
- **Atomic Transactions:** Processes delivery (stock-in) and sale (stock-out) actions with built-in quantity validation.  
- **Reporting:**  
  - Prints raw tables in key-ordered order  
  - Employee income summaries (by name)  
  - Chronological activity logs (sales vs. deliveries)

## 🛠 Tech Stack
- **Language:** Python 3.9+  
- **Database:** SQLite3  
- **Modules:** `initiate.py`, `action.py`, `printdb.py`
