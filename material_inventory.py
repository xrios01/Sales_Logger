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
    YELLOW,
    BOLD,
    WHITE,
)


def set_material_cost():
    while True:
        clear_screen()
        print_header("SET MATERIAL COST", CYAN)

        print()
        print(color_text("Current Material Costs", BOLD + WHITE))
        print("-" * 40)

        makers = list(data_store.material_costs.keys())

        for i, maker in enumerate(makers, start=1):
            print(
                f" {color_text(str(i) + '.', CYAN):<5} "
                f"{maker:<12} cost: ${data_store.material_costs[maker]:.2f}"
            )

        print()
        print(color_text("Commands", BOLD + WHITE))
        print("-" * 40)
        print(f" {color_text('[person number]', CYAN):<15} Update that person's material cost")
        print(f" {color_text('[q]', CYAN):<15} Return to main menu")

        choice = input(
            color_text("\nEnter person number to update or q to quit: ", YELLOW)
        ).strip().lower()

        if choice == "q":
            return

        if not choice.isdigit():
            print_error("Invalid input. Please enter a number or q.")
            pause()
            continue

        person_num = int(choice)
        if person_num < 1 or person_num > len(makers):
            print_error("Invalid person number.")
            pause()
            continue

        maker = makers[person_num - 1]

        amount_text = input(
            color_text(f"Enter total material cost for {maker}: $", YELLOW)
        ).strip()

        try:
            amount = float(amount_text)
            if amount < 0:
                raise ValueError
        except ValueError:
            print_error("Please enter a valid non-negative number.")
            pause()
            continue

        data_store.material_costs[maker] = amount
        data_store.material_costs_changed_this_session = True
        print_success(f"Material cost for {maker} set to ${amount:.2f}")
        pause()


def set_inventory():
    while True:
        clear_screen()
        print_header("SET INVENTORY", CYAN)

        print()
        print(color_text("Current Inventory", BOLD + WHITE))
        print("-" * 40)

        for i, (name, data) in enumerate(data_store.sales.items(), start=1):
            print(
                f" {color_text(str(i) + '.', CYAN):<5} "
                f"{name:<12} stock: {data['inventory']}"
            )

        print()
        print(color_text("Commands", BOLD + WHITE))
        print("-" * 40)
        print(f" {color_text('[item number]', CYAN):<15} Update that item's inventory")
        print(f" {color_text('[q]', CYAN):<15} Return to main menu")

        choice = input(
            color_text("\nEnter item number to update or q to quit: ", YELLOW)
        ).strip().lower()

        if choice == "q":
            return

        if not choice.isdigit():
            print_error("Invalid input. Please enter a number or q.")
            pause()
            continue

        item_num = int(choice)
        if item_num < 1 or item_num > len(data_store.sales):
            print_error("Invalid item number.")
            pause()
            continue

        name = list(data_store.sales.keys())[item_num - 1]

        amount_text = input(
            color_text(f"Enter inventory amount for {name}: ", YELLOW)
        ).strip()

        if not amount_text.isdigit():
            print_error("Inventory must be a whole number 0 or greater.")
            pause()
            continue

        data_store.sales[name]["inventory"] = int(amount_text)
        data_store.inventory_changed_this_session = True
        print_success(f"Inventory for {name} set to {data_store.sales[name]['inventory']}")
        pause()