from datetime import datetime
import data_store
from email_receipt import send_receipt_email
from helpers import (
    clear_screen,
    print_header,
    print_success,
    print_error,
    print_warning,
    pause,
    color_text,
    get_total_items,
    get_total_revenue,
    GREEN,
    RED,
    YELLOW,
    CYAN,
    BOLD,
    WHITE,
    BRIGHT_YELLOW,
)


def add_sale(item_index):
    clear_screen()
    print_header("ADD ITEM TO CART", GREEN)

    product_names = list(data_store.sales.keys())
    name = product_names[item_index]
    price = data_store.sales[name]["price"]
    maker = data_store.sales[name].get("maker", "Unknown")

    if data_store.sales[name]["inventory"] <= 0:
        print_warning(f"Cannot add {name}; inventory is 0.")
        pause()
        return

    if not data_store.current_cart:
        print()
        sold_to_name = input(color_text("Sold to (customer name): ", YELLOW)).strip()
        sold_to_phone = input(color_text("Customer phone #: ", YELLOW)).strip()
        sold_to_email = input(color_text("Customer email (optional): ", YELLOW)).strip().lower()
        sold_by = input(color_text("Sold by: ", YELLOW)).strip()

        data_store.current_customer["sold_to_name"] = sold_to_name if sold_to_name else "N/A"
        data_store.current_customer["sold_to_phone"] = sold_to_phone if sold_to_phone else "N/A"
        data_store.current_customer["sold_to_email"] = sold_to_email if sold_to_email else "N/A"
        data_store.current_customer["sold_by"] = sold_by if sold_by else "N/A"

    data_store.sales[name]["inventory"] -= 1

    cart_item = {
        "item": name,
        "price": price,
        "maker": maker,
        "is_custom": False,
    }

    data_store.current_cart.append(cart_item)

    print_success(f"Added to cart: {name} (${price:.2f})")
    show_cart_preview()


def add_custom_charge():
    while True:
        clear_screen()
        print_header("ADD CUSTOM CHARGE / ADD-ON", CYAN)

        if not data_store.current_cart:
            print_warning("Start a transaction first by adding at least one item.")
            pause()
            return

        print()
        print(color_text("Add a one-time charge to this transaction.", BOLD + WHITE))
        print("Examples: charm add-on, engraving, gift wrap, rush fee, customization\n")
        print("Type ["+color_text("q", BRIGHT_YELLOW) + "] at any prompt to cancel.")
        print("-" * 60)

        # ----------------------------
        # Description
        # ----------------------------
        while True:
            description = input(color_text("Description of add on: ", YELLOW)).strip()

            if description.lower() == "q":
                print_warning("Custom charge cancelled.")
                pause()
                return

            if not description:
                print_error("Description cannot be empty.")
                pause()
                continue

            break

        # ----------------------------
        # Amount
        # ----------------------------
        while True:
            amount_text = input(color_text("Extra charge amount $", YELLOW)).strip()

            if amount_text.lower() == "q":
                print_warning("Custom charge cancelled.")
                pause()
                return

            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
                break
            except ValueError:
                print_error("Please enter a valid amount greater than 0.")
                pause()

        makers = list(data_store.material_costs.keys())

        if not makers:
            print_error("No makers found. Add a maker first.")
            pause()
            return

        # ----------------------------
        # Choose maker
        # ----------------------------
        while True:
            clear_screen()
            print_header("ADD CUSTOM CHARGE / ADD-ON", CYAN)

            print()
            print(color_text("Review Custom Charge", BOLD + WHITE))
            print("-" * 45)
            print(f" Description : {description}")
            print(f" Amount      : ${amount:.2f}")

            print()
            print(color_text("Who should receive this charge?", BOLD + WHITE))
            print("(This determines who gets the profit)", CYAN)
            print("Type [q] to cancel.")
            print("-" * 45)

            for i, maker in enumerate(makers, start=1):
                print(f" {color_text(str(i) + '.', CYAN):<5} {maker}")

            choice = input(color_text("\nEnter number: ", YELLOW)).strip()

            if choice.lower() == "q":
                print_warning("Custom charge cancelled.")
                pause()
                return

            if not choice.isdigit():
                print_error("Invalid input. Please enter a number.")
                pause()
                continue

            person_num = int(choice)
            if person_num < 1 or person_num > len(makers):
                print_error("Invalid person number.")
                pause()
                continue

            maker = makers[person_num - 1]
            break

        cart_item = {
            "item": f"[ADD-ON] {description}",
            "price": amount,
            "maker": maker,
            "is_custom": True,
        }

        data_store.current_cart.append(cart_item)

        print_success(f"Added: {description} (${amount:.2f}) assigned to {maker}")
        show_cart_preview()
        return


def show_cart_preview():
    print()
    print(color_text("Current Cart", BOLD + WHITE))
    print("-" * 40)
    for i, item in enumerate(data_store.current_cart, start=1):
        print(f" {i}. {item['item']:<15} ${item['price']:.2f}")

    cart_total = sum(item["price"] for item in data_store.current_cart)
    print("-" * 40)
    print(f" Cart total      : ${cart_total:.2f}")

    pause()


def finalize_transaction():
    if not data_store.current_cart:
        clear_screen()
        print_header("FINALIZE TRANSACTION", GREEN)
        print_warning("There are no items in the cart.")
        pause()
        return

    clear_screen()
    print_header("FINALIZE TRANSACTION", GREEN)

    timestamp = datetime.now().strftime("%m-%d-%Y %I:%M:%S %p")

    transaction = {
        "sold_to_name": data_store.current_customer["sold_to_name"],
        "sold_to_phone": data_store.current_customer["sold_to_phone"],
        "sold_to_email": data_store.current_customer["sold_to_email"],
        "sold_by": data_store.current_customer["sold_by"],
        "timestamp": timestamp,
        "items": data_store.current_cart.copy(),
    }

    for item in data_store.current_cart:
        name = item["item"]
        price = item["price"]
        maker = item.get("maker", "Unknown")
        is_custom = item.get("is_custom", False)

        if not is_custom and name in data_store.sales:
            data_store.sales[name]["qty"] += 1
            data_store.sales[name]["revenue"] += price

        data_store.sale_log.append({
            "item": name,
            "price": price,
            "maker": maker,
            "is_custom": is_custom,
            "sold_to_name": transaction["sold_to_name"],
            "sold_to_phone": transaction["sold_to_phone"],
            "sold_to_email": transaction["sold_to_email"],
            "sold_by": transaction["sold_by"],
            "timestamp": timestamp,
        })

    if (
        data_store.EMAIL_ENABLED
        and transaction["sold_to_email"] != "N/A"
        and transaction["sold_to_email"].strip()
        and data_store.SENDER_EMAIL.strip()
        and data_store.APP_PASSWORD.strip()
    ):
        try:
            send_receipt_email(
                customer_email=transaction["sold_to_email"],
                transaction=transaction,
                sender_email=data_store.SENDER_EMAIL,
                app_password=data_store.APP_PASSWORD,
            )
            print_success("Receipt emailed successfully.")
        except Exception as e:
            print_error(f"Could not send email: {e}")

    print_success("Transaction finalized.")

    print()
    print(color_text("Receipt Summary", BOLD + WHITE))
    print("-" * 40)
    for item in transaction["items"]:
        print(f" {item['item']:<15} ${item['price']:.2f}")
    print("-" * 40)
    print(f" Total items      : {len(transaction['items'])}")
    print(f" Total amount     : ${sum(item['price'] for item in transaction['items']):.2f}")
    print(f" Sold to          : {transaction['sold_to_name']}")
    print(f" Time logged      : {timestamp}")

    data_store.current_cart.clear()
    data_store.current_customer = {
        "sold_to_name": "",
        "sold_to_phone": "",
        "sold_to_email": "",
        "sold_by": "",
    }

    pause()


def cancel_transaction():
    if not data_store.current_cart:
        clear_screen()
        print_header("CANCEL TRANSACTION", RED)
        print_warning("There is no active cart to cancel.")
        pause()
        return

    for item in data_store.current_cart:
        if not item.get("is_custom", False) and item["item"] in data_store.sales:
            data_store.sales[item["item"]]["inventory"] += 1

    data_store.current_cart.clear()
    data_store.current_customer = {
        "sold_to_name": "",
        "sold_to_phone": "",
        "sold_to_email": "",
        "sold_by": "",
    }

    clear_screen()
    print_header("CANCEL TRANSACTION", RED)
    print_warning("Current transaction cancelled.")
    pause()


def remove_sale():
    while True:
        clear_screen()
        print_header("REMOVE SAVED SALE", RED)

        print()
        print("Which item would you like to remove from recorded sales?")
        print("-" * 50)

        removable_items = [
            (name, data) for name, data in data_store.sales.items()
        ]

        for i, (name, data) in enumerate(removable_items, start=1):
            sold_qty = data["qty"]
            print(f" {color_text(str(i) + '.', CYAN):<5} {name:<12} sold: {sold_qty}")

        print()
        print(color_text("[q]", CYAN) + " Return to main menu")

        choice = input(color_text("\nEnter item number to remove: ", YELLOW)).strip().lower()

        if choice == "q":
            return

        if not choice.isdigit():
            print_error("Invalid input. Please enter a number.")
            pause()
            continue

        item_num = int(choice)
        if item_num < 1 or item_num > len(removable_items):
            print_error("Invalid item number.")
            pause()
            continue

        name, data = removable_items[item_num - 1]
        price = data["price"]

        if data_store.sales[name]["qty"] <= 0:
            print_warning(f"Cannot remove {name}; none have been sold yet.")
            pause()
            continue

        data_store.sales[name]["qty"] -= 1
        data_store.sales[name]["revenue"] -= price
        data_store.sales[name]["inventory"] += 1

        for i in range(len(data_store.sale_log) - 1, -1, -1):
            if (
                data_store.sale_log[i]["item"] == name
                and data_store.sale_log[i]["price"] == price
            ):
                del data_store.sale_log[i]
                break

        print_success(f"Removed saved sale: {name} (${price:.2f})")

        print()
        print(color_text("Updated Totals", BOLD + WHITE))
        print("-" * 40)
        print(f" {name} sold so far : {data_store.sales[name]['qty']}")
        print(f" Total items sold  : {get_total_items()}")
        print(f" Total revenue     : ${get_total_revenue():.2f}")

        pause()
