# Sales Logger CLI

A terminal-based sales tracking application built in Python for managing handmade product sales, inventory, receipts, and profit tracking.

## Features

- Add and remove item sales
- Track product inventory
- Set and update material costs
- View running totals and profit
- Add, edit, and delete products
- Save sales receipts as:
  - JSON
  - CSV
- Optionally email a receipt to customers
- Color-coded terminal interface for readability

## Products Tracked

By default, the program starts with:

- Bracelet
- Necklace
- Ring
- Earring
- Headband

Products can also be added, edited, or deleted through the product management menu.

---

## Project Structure

```bash
main.py
helpers.py
data_store.py
display.py
sales.py
product_management.py
material_inventory.py
summary.py
email_receipt.py
other.py
```

### File Roles

- **main.py** → main menu and program flow
- **helpers.py** → colors, UI helpers, shared utility functions
- **data_store.py** → shared application data/state
- **display.py** → main menu and totals display
- **sales.py** → add/remove sale logic
- **product_management.py** → add/edit/delete products
- **material_inventory.py** → inventory and material cost tools
- **summary.py** → save receipts as JSON/CSV
- **email_receipt.py** → optional email receipt support
- **other.py** → help screen and extras

---

## How to Run

Make sure you have Python 3 installed.

Then run:

```bash
python main.py
```

Or on Windows if needed:

```bash
py main.py
```

---

## Email Receipt Setup (Optional)

This project supports emailing a receipt to customers using Gmail.

To enable it, open `data_store.py` and update:

```python
EMAIL_ENABLED = True
SENDER_EMAIL = "youremail@gmail.com"
APP_PASSWORD = "your_app_password_here"
```

### Important
If using Gmail, you must use a **Google App Password**, not your normal Gmail password.

---

## Receipt Output

The program can save receipts in two formats:

### JSON
Useful for structured logs and data storage.

### CSV
Useful for spreadsheet viewing and more receipt-style summaries.

Saved receipt files include:

- date and time
- transaction history
- customer info
- item totals
- total sales
- material cost
- total profit

---

## Example Use Cases

This project is useful for small handmade businesses or hobby sellers who want a lightweight way to track:

- sales
- inventory
- customer info
- receipts
- profit

---

## Future Improvements

Possible future upgrades:

- persistent save/load system
- PDF receipt generation
- search sales history
- delete/edit individual transactions by receipt number
- better email validation
- GUI version with Tkinter or PyQt

---

## Author

Built in Python as a modular CLI sales tracker project.