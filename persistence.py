import json
import os
import data_store
from paths import DATA_DIR

DATA_FILE = DATA_DIR / "products.json"


def save_products():
    saved_sales = {}

    for name, data in data_store.sales.items():
        saved_sales[name] = {
            "price": data["price"],
            "maker": data.get("maker", "Unknown"),
            "inventory": data.get("inventory", 0),
        }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(saved_sales, f, indent=4)


def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded_sales = json.load(f)

            if isinstance(loaded_sales, dict) and loaded_sales:
                data_store.sales = {}

                for name, saved in loaded_sales.items():
                    data_store.sales[name] = {
                        "price": saved.get("price", 0.0),
                        "qty": 0,
                        "revenue": 0.0,
                        "inventory": saved.get("inventory", 0),
                        "maker": saved.get("maker", "Unknown"),
                    }
        except (json.JSONDecodeError, OSError):
            pass

    reset_daily_data()


def reset_daily_data():
    for item in data_store.sales.values():
        item["qty"] = 0
        item["revenue"] = 0.0
        # DO NOT reset inventory here

    makers = set()

    for item in data_store.sales.values():
        makers.add(item.get("maker", "Unknown"))

    data_store.material_costs = {maker: 0.0 for maker in makers}

    data_store.sale_log = []
    data_store.current_cart = []
    data_store.current_customer = {
        "sold_to_name": "",
        "sold_to_phone": "",
        "sold_to_email": "",
        "sold_by": "",
    }

    data_store.json_saved_this_session = False
    data_store.csv_saved_this_session = False
    data_store.inventory_changed_this_session = False
    data_store.material_costs_changed_this_session = False
    data_store.products_changed_this_session = False
