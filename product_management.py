import data_store
from helpers import (
    clear_screen,
    print_header,
    print_success,
    print_error,
    print_warning,
    pause,
    color_text,
    CYAN,
    GREEN,
    RED,
    YELLOW,
    BOLD,
    WHITE,
)
from persistence import save_products


def manage_products():
    while True:
        clear_screen()
        print_header("MANAGE PRODUCTS", CYAN)

        print()
        print(color_text("Current Products", BOLD + WHITE))
        print("-" * 70)

        if data_store.sales:
            for i, (name, data) in enumerate(data_store.sales.items(), start=1):
                print(
                    f" {color_text(str(i) + '.', CYAN):<5} "
                    f"{name:<15} price: ${data['price']:.2f}   stock: {data['inventory']}   maker: {data.get('maker', 'Unknown')}"
                )
        else:
            print_warning("No products available yet.")

        print()
        print(color_text("Commands", BOLD + WHITE))
        print("-" * 50)
        print(f" {color_text('[a]', CYAN):<10} Add new product")
        print(f" {color_text('[e]', CYAN):<10} Edit a product")
        print(f" {color_text('[d]', CYAN):<10} Delete a product")
        print(f" {color_text('[q]', CYAN):<10} Return to main menu")

        choice = input(color_text("\nEnter choice: ", YELLOW)).strip().lower()

        if choice == "q":
            return
        elif choice == "a":
            add_product()
        elif choice == "e":
            edit_product()
        elif choice == "d":
            delete_product()
        else:
            print_error("Invalid command.")
            pause()


def add_product():
    clear_screen()
    print_header("ADD PRODUCT", GREEN)

    name = input(color_text("Enter product name: ", YELLOW)).strip()
    if not name:
        print_error("Product name cannot be empty.")
        pause()
        return

    if name in data_store.sales:
        print_error("That product already exists.")
        pause()
        return

    price_text = input(color_text("Enter product price: $", YELLOW)).strip()
    inventory_text = input(color_text("Enter starting inventory: ", YELLOW)).strip()
    maker = input(color_text("Enter maker/owner name: ", YELLOW)).strip()

    if not maker:
        print_error("Maker name cannot be empty.")
        pause()
        return

    try:
        price = float(price_text)
        if price < 0:
            raise ValueError
    except ValueError:
        print_error("Price must be a valid non-negative number.")
        pause()
        return

    if not inventory_text.isdigit():
        print_error("Inventory must be a whole number 0 or greater.")
        pause()
        return

    data_store.sales[name] = {
        "price": price,
        "qty": 0,
        "revenue": 0.0,
        "inventory": int(inventory_text),
        "maker": maker,
    }

    if maker not in data_store.material_costs:
        data_store.material_costs[maker] = 0.0

    save_products()
    data_store.products_changed_this_session = True

    print_success(f"Added product: {name}")
    pause()


def choose_product(prompt_text):
    if not data_store.sales:
        print_warning("No products available.")
        pause()
        return None

    print()
    print(color_text("Products", BOLD + WHITE))
    print("-" * 60)

    product_names = list(data_store.sales.keys())

    for i, name in enumerate(product_names, start=1):
        data = data_store.sales[name]
        print(
            f" {color_text(str(i) + '.', CYAN):<5} "
            f"{name:<15} ${data['price']:.2f} stock: {data['inventory']} maker: {data.get('maker', 'Unknown')}"
        )

    choice = input(color_text(f"\n{prompt_text}", YELLOW)).strip()

    if not choice.isdigit():
        print_error("Invalid input. Please enter a number.")
        pause()
        return None

    item_num = int(choice)
    if item_num < 1 or item_num > len(product_names):
        print_error("Invalid item number.")
        pause()
        return None

    return product_names[item_num - 1]


def edit_product():
    clear_screen()
    print_header("EDIT PRODUCT", YELLOW)

    name = choose_product("Enter product number to edit: ")
    if name is None:
        return

    data = data_store.sales[name]

    print()
    print(f"Current name      : {name}")
    print(f"Current price     : ${data['price']:.2f}")
    print(f"Current inventory : {data['inventory']}")
    print(f"Current maker     : {data.get('maker', 'Unknown')}")
    print()

    new_name = input(color_text("New name (leave blank to keep same): ", YELLOW)).strip()
    new_price_text = input(color_text("New price (leave blank to keep same): $", YELLOW)).strip()
    new_inventory_text = input(color_text("New inventory (leave blank to keep same): ", YELLOW)).strip()
    new_maker = input(color_text("New maker (leave blank to keep same): ", YELLOW)).strip()

    final_name = name
    if new_name:
        if new_name != name and new_name in data_store.sales:
            print_error("Another product already has that name.")
            pause()
            return
        final_name = new_name

    final_price = data["price"]
    if new_price_text:
        try:
            final_price = float(new_price_text)
            if final_price < 0:
                raise ValueError
        except ValueError:
            print_error("Price must be a valid non-negative number.")
            pause()
            return

    final_inventory = data["inventory"]
    if new_inventory_text:
        if not new_inventory_text.isdigit():
            print_error("Inventory must be a whole number 0 or greater.")
            pause()
            return
        final_inventory = int(new_inventory_text)

    final_maker = data.get("maker", "Unknown")
    if new_maker:
        final_maker = new_maker
        if final_maker not in data_store.material_costs:
            data_store.material_costs[final_maker] = 0.0

    updated = {
        "price": final_price,
        "qty": data["qty"],
        "revenue": data["revenue"],
        "inventory": final_inventory,
        "maker": final_maker,
    }

    if final_name != name:
        data_store.sales.pop(name)
        data_store.sales[final_name] = updated

        for sale in data_store.sale_log:
            if sale["item"] == name:
                sale["item"] = final_name
                sale["maker"] = final_maker
    else:
        data_store.sales[name] = updated

        for sale in data_store.sale_log:
            if sale["item"] == name:
                sale["maker"] = final_maker

    save_products()
    data_store.products_changed_this_session = True

    print_success(f"Updated product: {final_name}")
    pause()


def delete_product():
    clear_screen()
    print_header("DELETE PRODUCT", RED)

    name = choose_product("Enter product number to delete: ")
    if name is None:
        return

    if data_store.sales[name]["qty"] > 0:
        print_warning("Cannot delete a product that already has recorded sales.")
        pause()
        return

    confirm = input(color_text(f"Type 'yes' to delete {name}: ", YELLOW)).strip().lower()

    if confirm != "yes":
        print_warning("Delete cancelled.")
        pause()
        return

    del data_store.sales[name]
    save_products()
    data_store.products_changed_this_session = True

    print_success(f"Deleted product: {name}")
    pause()
