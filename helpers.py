import os
import data_store
import re

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def visible_len(text):
    return len(ANSI_ESCAPE_RE.sub("", text))


def pad_ansi(text, width):
    return text + " " * max(0, width - visible_len(text))


##############################
# ANSI Color Codes
##############################
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BOLD = "\033[1m"
BRIGHT_YELLOW = "\033[93m"
ORANGE = "\033[38;2;255;165;0m"


##############################
# Helper Functions
##############################
def color_text(text, color):
    return f"{color}{text}{RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(color_text("\nPress Enter to continue...", YELLOW))


def print_header(title, color=BLUE):
    width = 40
    print(color_text("╔" + "═" * width + "╗", color))
    print(color_text("║" + title.center(width) + "║", BOLD + color))
    print(color_text("╚" + "═" * width + "╝", color))


def print_success(message):
    print("\n" + color_text(f"✓ {message}", GREEN))


def print_error(message):
    print("\n" + color_text(f"✗ {message}", RED))


def print_warning(message):
    print("\n" + color_text(f"! {message}", YELLOW))


def print_info(message):
    print(color_text(message, CYAN))


def get_total_items():
    return sum(data["qty"] for data in data_store.sales.values())


def get_total_revenue():
    return sum(data["revenue"] for data in data_store.sales.values())


def get_total_material_cost():
    return sum(data_store.material_costs.values())


def get_total_profit():
    return get_total_revenue() - get_total_material_cost()

def get_addon_count():
    return sum(1 for sale in data_store.sale_log if sale.get("is_custom", False))


def get_total_line_items():
    return len(data_store.sale_log)


def get_profit_by_maker():
    maker_totals = {}

    for item_name, data in data_store.sales.items():
        maker = data.get("maker", "Unknown")

        if maker not in maker_totals:
            maker_totals[maker] = {
                "items_sold": 0,
                "revenue": 0.0,
                "material_cost": data_store.material_costs.get(maker, 0.0),
                "profit": 0.0,
            }

        maker_totals[maker]["items_sold"] += data["qty"]
        maker_totals[maker]["revenue"] += data["revenue"]

    for maker in maker_totals:
        maker_totals[maker]["profit"] = (
            maker_totals[maker]["revenue"] - maker_totals[maker]["material_cost"]
        )

    return maker_totals