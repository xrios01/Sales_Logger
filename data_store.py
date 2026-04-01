# Shared application data/state


##############################
# Email Settings
##############################
EMAIL_ENABLED = FALSE  # set to true to turn on email functiality only after you included the source email and app password
SENDER_EMAIL = "youremail@email.com"
APP_PASSWORD = "yourapppassword"

##############################
# Current transaction/cart
##############################
current_cart = []
current_customer = {
    "sold_to_name": "",
    "sold_to_phone": "",
    "sold_to_email": "",
    "sold_by": "",
}

##############################
# Inventory / Products
##############################
sales = {
    "Bracelet": {
        "price": 1.50,
        "qty": 0,
        "revenue": 0.0,
        "inventory": 0,
        "maker": "Denise",
    },
    "Necklace": {
        "price": 2.00,
        "qty": 0,
        "revenue": 0.0,
        "inventory": 0,
        "maker": "Deborah",
    },
    "Ring": {
        "price": 1.25,
        "qty": 0,
        "revenue": 0.0,
        "inventory": 0,
        "maker": "Denise",
    },
    "Earring": {
        "price": 1.00,
        "qty": 0,
        "revenue": 0.0,
        "inventory": 0,
        "maker": "Roseanne",
    },
    "Headband": {
        "price": 0.75,
        "qty": 0,
        "revenue": 0.0,
        "inventory": 0,
        "maker": "Deborah",
    },
}

##############################
# Material cost by maker
##############################
material_costs = {
    "Denise": 0.0,
    "Deborah": 0.0,
    "Roseanne": 0.0,
}

##############################
# Individual sale log
##############################
sale_log = []


##############################
# Session save/change flags
##############################
json_saved_this_session = False
csv_saved_this_session = False
inventory_changed_this_session = False
material_costs_changed_this_session = False
products_changed_this_session = False