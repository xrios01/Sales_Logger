import data_store
from helpers import (
    clear_screen,
    print_header,
    print_success,
    print_error,
    print_warning,
    pause,
    color_text,
    ORANGE,
    YELLOW,
    CYAN,
)
from display import display_items, show_totals
from material_inventory import set_inventory, set_material_cost
from product_management import manage_products
from sales import add_sale, finalize_transaction, cancel_transaction, remove_sale, add_custom_charge
from summary import save_summary, save_summary_csv
from other import show_help, secret, show_startup_guide
from persistence import load_products
from config_manager import load_config, config_exists, first_run_email_setup, email_settings_menu


def get_yes_no(prompt):
    while True:
        choice = input(color_text(prompt, YELLOW)).strip().lower()
        if choice in ("y", "n"):
            return choice
        print_error("Please enter 'y' or 'n'.")
        pause()


def main():
    load_products()
    load_config()

    if not config_exists():
        first_run_email_setup()
        load_config()

    show_startup_guide()

    while True:
        display_items()
        choice = input(color_text("\nEnter choice: ", YELLOW)).strip().lower()

        if choice == "q":
            has_unsaved_json = not data_store.json_saved_this_session
            has_unsaved_csv = not data_store.csv_saved_this_session

            has_sales_activity = len(data_store.sale_log) > 0
            has_setup_changes = (
                data_store.inventory_changed_this_session
                or data_store.material_costs_changed_this_session
                or data_store.products_changed_this_session
            )

            clear_screen()
            print_header("QUIT PROGRAM", ORANGE)

            # Strong warning: sales happened, but files not saved
            if has_sales_activity and (has_unsaved_json or has_unsaved_csv):
                print_warning("You have unsaved end-of-day files for this session.")
                print()

                if has_unsaved_json:
                    print(" JSON receipt has not been saved yet.")
                if has_unsaved_csv:
                    print(" CSV receipt has not been saved yet.")

                print()
                print(" " + color_text("[j]", CYAN) + " Save JSON now")
                print(" " + color_text("[c]", CYAN) + " Save CSV now")
                print(" " + color_text("[q]", CYAN) + " Quit anyway")
                print(" " + color_text("[x]", CYAN) + " Cancel and return")

                quit_choice = input(color_text("\nEnter choice: ", YELLOW)).strip().lower()

                if quit_choice == "j":
                    save_summary()
                    continue
                elif quit_choice == "c":
                    save_summary_csv()
                    continue
                elif quit_choice == "q":
                    clear_screen()
                    print_header("GOODBYE", ORANGE)
                    print_success("Exiting program.\n")
                    break
                else:
                    continue

            # Softer confirmation: setup changed, but no sales happened
            elif has_setup_changes:
                print_warning("You made setup changes this session.")
                print(" Inventory, material costs, or products were changed.")
                print()

                confirm = get_yes_no("\nAre you sure you want to quit? (y/n): ")

                if confirm == "y":
                    clear_screen()
                    print_header("GOODBYE", ORANGE)
                    print_success("Exiting program.\n")
                    break
                else:
                    continue

            # Normal quit confirmation: nothing meaningful happened
            else:
                confirm = get_yes_no("\nAre you sure you want to quit? (y/n): ")

                if confirm == "y":
                    clear_screen()
                    print_header("GOODBYE", ORANGE)
                    print_success("Exiting program.\n")
                    break
                else:
                    continue

        elif choice == "t":
            show_totals()

        elif choice == "i":
            set_inventory()

        elif choice == "m":
            set_material_cost()

        elif choice == "p":
            manage_products()

        elif choice == "r":
            remove_sale()

        elif choice == "f":
            finalize_transaction()

        elif choice == "x":
            cancel_transaction()

        elif choice == "j":
            save_summary()

        elif choice == "c":
            save_summary_csv()

        elif choice == "h":
            show_help()

        elif choice == "xr":
            secret()

        elif choice == "u":
            add_custom_charge()

        elif choice == "e":
            email_settings_menu()

        elif choice.isdigit():
            item_num = int(choice)

            if 1 <= item_num <= len(data_store.sales):
                add_sale(item_num - 1)
            else:
                print_error("Invalid item number.")
                pause()

        else:
            print_error("Invalid command.")
            pause()


if __name__ == "__main__":
    main()
