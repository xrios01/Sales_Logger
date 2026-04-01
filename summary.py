import csv
import json
from datetime import datetime
import data_store
from paths import DATA_DIR
from helpers import (
    clear_screen,
    print_header,
    print_success,
    pause,
    color_text,
    get_total_items,
    get_addon_count,
    get_total_line_items,
    get_total_revenue,
    get_total_profit,
    get_total_material_cost,
    get_profit_by_maker,
    CYAN,
    BOLD,
    WHITE,
)


def save_summary():
    clear_screen()
    print_header("SAVE JSON RECEIPT", CYAN)

    now = datetime.now()
    filename = DATA_DIR / f"sales_receipt_{now.strftime('%m-%d-%Y_%H-%M-%S')}.json"

    maker_summary = get_profit_by_maker()

    receipt_data = {
        "receipt_info": {
            "date": now.strftime("%m-%d-%Y"),
            "time": now.strftime("%I:%M:%S %p"),
            "total_items_sold": get_total_items(),
            "add_ons_sold": get_addon_count(),
            "line_items": get_total_line_items(),
            "total_revenue": round(get_total_revenue(), 2),
            "overall_material_cost": round(get_total_material_cost(), 2),
            "overall_profit": round(get_total_profit(), 2),
        },
        "line_items": [],
        "item_totals": [],
        "material_cost_by_person": [],
        "profit_by_person": [],
    }

    # Individual sales
    for sale in data_store.sale_log:
        receipt_data["line_items"].append({
            "item": sale["item"],
            "price": round(sale["price"], 2),
            "maker": sale.get("maker", "Unknown"),
            "sold_to_name": sale["sold_to_name"],
            "sold_to_phone": sale["sold_to_phone"],
            "sold_to_email": sale.get("sold_to_email", "N/A"),
            "sold_by": sale["sold_by"],
            "timestamp": sale["timestamp"],
        })

    # Item totals
    for name, data in data_store.sales.items():
        receipt_data["item_totals"].append({
            "item": name,
            "maker": data.get("maker", "Unknown"),
            "price_each": round(data["price"], 2),
            "quantity_sold": data["qty"],
            "total_revenue": round(data["revenue"], 2),
            "inventory_left": data["inventory"],
        })

    # Material cost by person
    for maker, data in maker_summary.items():
        receipt_data["material_cost_by_person"].append({
            "maker": maker,
            "material_cost": round(data["material_cost"], 2),
        })

    # Profit by person
    for maker, data in maker_summary.items():
        receipt_data["profit_by_person"].append({
            "maker": maker,
            "items_sold": data["items_sold"],
            "revenue": round(data["revenue"], 2),
            "profit": round(data["profit"], 2),
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(receipt_data, f, indent=4)
    
    data_store.json_saved_this_session = True

    print_success(f"JSON receipt saved to: {str(filename)}")

    print()
    print(color_text("Saved Data", BOLD + WHITE))
    print("-" * 40)
    print(f" Total items sold : {get_total_items()}")
    print(f" Add-ons sold     : {get_addon_count()}")
    print(f" Line items       : {get_total_line_items()}")
    print(f" Total revenue    : ${get_total_revenue():.2f}")

    

    pause()


def save_summary_csv():
    clear_screen()
    print_header("SAVE CSV RECEIPT", CYAN)

    now = datetime.now()
    filename = DATA_DIR / f"sales_receipt_{now.strftime('%m-%d-%Y_%H-%M-%S')}.csv"

    maker_summary = get_profit_by_maker()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["SALES RECEIPT"])
        writer.writerow(["Date", now.strftime("%m-%d-%Y")])
        writer.writerow(["Time", now.strftime("%I:%M:%S %p")])
        writer.writerow([])

        # Running receipt / individual sales
        writer.writerow(["RUNNING RECEIPT"])
        writer.writerow([
            "Sale #",
            "Item",
            "Maker",
            "Price",
            "Sold To",
            "Phone #",
            "Customer Email",
            "Sold By",
            "Timestamp"
        ])

        if data_store.sale_log:
            for i, sale in enumerate(data_store.sale_log, start=1):
                writer.writerow([
                    i,
                    sale["item"],
                    sale.get("maker", "Unknown"),
                    f"${sale['price']:.2f}",
                    sale["sold_to_name"],
                    sale["sold_to_phone"],
                    sale["sold_to_email"],
                    sale["sold_by"],
                    sale["timestamp"],
                ])
        else:
            writer.writerow(["No sales recorded yet."])

        # Item totals
        writer.writerow([])
        writer.writerow(["ITEM TOTALS"])
        writer.writerow([
            "Item",
            "Maker",
            "Price Each",
            "Quantity Sold",
            "Item Revenue",
            "Inventory Left"
        ])

        for name, data in data_store.sales.items():
            writer.writerow([
                name,
                data.get("maker", "Unknown"),
                f"${data['price']:.2f}",
                data["qty"],
                f"${data['revenue']:.2f}",
                data["inventory"],
            ])

        # Overall summary
        writer.writerow([])
        writer.writerow(["OVERALL SUMMARY"])
        writer.writerow(["Total Items Sold", get_total_items()])
        writer.writerow(["Add-Ons Sold", get_addon_count()])
        writer.writerow(["Line Items", get_total_line_items()])
        writer.writerow(["Total Revenue", f"${get_total_revenue():.2f}"])
        writer.writerow(["Overall Material Cost", f"${get_total_material_cost():.2f}"])
        writer.writerow(["Overall Profit", f"${get_total_profit():.2f}"])

        # Material cost by person
        writer.writerow([])
        writer.writerow(["MATERIAL COST BY PERSON"])
        writer.writerow(["Maker", "Material Cost"])

        if maker_summary:
            for maker, data in maker_summary.items():
                writer.writerow([
                    maker,
                    f"${data['material_cost']:.2f}",
                ])
        else:
            writer.writerow(["No maker data available."])

        # Profit by person
        writer.writerow([])
        writer.writerow(["PROFIT BY PERSON"])
        writer.writerow(["Maker", "Items Sold", "Revenue", "Profit"])

        if maker_summary:
            for maker, data in maker_summary.items():
                writer.writerow([
                    maker,
                    data["items_sold"],
                    f"${data['revenue']:.2f}",
                    f"${data['profit']:.2f}",
                ])
        else:
            writer.writerow(["No maker data available."])
    
    data_store.csv_saved_this_session = True

    print_success(f"CSV receipt saved to: {str(filename)}")

    print()
    print(color_text("Saved Data", BOLD + WHITE))
    print("-" * 40)
    print(f" Total items sold : {get_total_items()}")
    print(f" Add-ons sold     : {get_addon_count()}")
    print(f" Line items       : {get_total_line_items()}")
    print(f" Total revenue    : ${get_total_revenue():.2f}")

   

    pause()