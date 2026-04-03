import json
import os
import data_store
from paths import DATA_DIR
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
    GREEN,
    RED,
    BOLD,
    WHITE,
    BLUE,
)

CONFIG_FILE = DATA_DIR / "config.json"


def get_default_config():
    return {
        "email_enabled": False,
        "sender_email": "",
        "app_password": "",
    }


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def load_config():
    config = get_default_config()

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            if isinstance(loaded, dict):
                config["email_enabled"] = bool(loaded.get("email_enabled", False))
                config["sender_email"] = str(loaded.get("sender_email", "")).strip()
                config["app_password"] = str(loaded.get("app_password", "")).strip()
        except (json.JSONDecodeError, OSError):
            pass

    apply_config_to_data_store(config)
    return config


def apply_config_to_data_store(config):
    data_store.EMAIL_ENABLED = config.get("email_enabled", False)
    data_store.SENDER_EMAIL = config.get("sender_email", "").strip()
    data_store.APP_PASSWORD = config.get("app_password", "").strip()


def config_exists():
    return os.path.exists(CONFIG_FILE)


def first_run_email_setup():
    clear_screen()
    print_header("FIRST-TIME EMAIL SETUP", CYAN)

    print()
    print(color_text("Email receipts are not set up yet.", BOLD + WHITE))
    print("You can set them up now or skip and do it later from the main menu.")
    print()

    while True:
        choice = input(color_text("Set up email receipts now? (y/n): ", YELLOW)).strip().lower()

        if choice == "y":
            run_email_setup_wizard()
            return
        elif choice == "n":
            config = get_default_config()
            save_config(config)
            apply_config_to_data_store(config)
            print_warning("Email setup skipped for now.")
            pause()
            return
        else:
            print_error("Please enter 'y' or 'n'.")


def run_email_setup_wizard():
    clear_screen()
    print_header("EMAIL SETUP", CYAN)

    print()
    print(color_text("Set up email receipts", BOLD + WHITE))
    print("-" * 40)
    print("Use the Gmail address you want receipts sent from.")
    print("For Gmail, use an App Password, not your normal password.")
    print()

    sender_email = input(color_text("Sender email: ", YELLOW)).strip()
    app_password = input(color_text("App password: ", YELLOW)).strip()

    if not sender_email or not app_password:
        print_error("Email and app password cannot be empty.")
        pause()
        return

    config = {
        "email_enabled": True,
        "sender_email": sender_email,
        "app_password": app_password,
    }

    save_config(config)
    apply_config_to_data_store(config)

    print_success("Email settings saved.")
    pause()


def email_settings_menu():
    while True:
        config = load_config()

        clear_screen()
        print_header("EMAIL SETTINGS", BLUE)

        print()
        print(color_text("Current Settings", BOLD + WHITE))
        print("-" * 40)
        print(" " + color_text("Email receipts ", CYAN) + f": {'Enabled' if config['email_enabled'] else 'Disabled'}")
        print(" " + color_text("Sender email   ", CYAN) + f": {config['sender_email'] if config['sender_email'] else 'Not set'}")
        print(" " + color_text("App password   ", CYAN) + f": {'Set' if config['app_password'] else 'Not set'}")

        print()
        print(color_text("Commands", BOLD + WHITE))
        print("-" * 40)
        print(" " + color_text("[1]", CYAN) + " Enable email receipts")
        print(" " + color_text("[2]", CYAN) + " Disable email receipts")
        print(" " + color_text("[3]", CYAN) + " Change sender email")
        print(" " + color_text("[4]", CYAN) + " Change app password")
        print(" " + color_text("[5]", CYAN) + " Run full email setup again")
        print(" " + color_text("[q]", CYAN) + " Return to main menu")

        choice = input(color_text("\nEnter choice: ", YELLOW)).strip().lower()

        if choice == "q":
            return

        elif choice == "1":
            if not config["sender_email"] or not config["app_password"]:
                print_error("You must set both sender email and app password first.")
                pause()
                continue

            config["email_enabled"] = True
            save_config(config)
            apply_config_to_data_store(config)
            print_success("Email receipts enabled.")
            pause()

        elif choice == "2":
            config["email_enabled"] = False
            save_config(config)
            apply_config_to_data_store(config)
            print_success("Email receipts disabled.")
            pause()

        elif choice == "3":
            new_email = input(color_text("Enter new sender email: ", YELLOW)).strip()
            if not new_email:
                print_error("Sender email cannot be empty.")
                pause()
                continue

            config["sender_email"] = new_email
            save_config(config)
            apply_config_to_data_store(config)
            print_success("Sender email updated.")
            pause()

        elif choice == "4":
            new_password = input(color_text("Enter new app password: ", YELLOW)).strip()
            if not new_password:
                print_error("App password cannot be empty.")
                pause()
                continue

            config["app_password"] = new_password
            save_config(config)
            apply_config_to_data_store(config)
            print_success("App password updated.")
            pause()

        elif choice == "5":
            run_email_setup_wizard()

        else:
            print_error("Invalid command.")
            pause()