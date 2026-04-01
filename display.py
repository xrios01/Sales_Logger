import data_store
from helpers import (
    clear_screen,
    print_header,
    color_text,
    print_warning,
    pause,
    get_total_items,
    get_addon_count,
    get_total_line_items,
    get_total_revenue,
    get_total_profit,
    get_profit_by_maker,
    get_total_material_cost,
    pad_ansi,
    visible_len,
    BLUE,
    BOLD,
    WHITE,
    CYAN,
    BRIGHT_YELLOW,
    MAGENTA,
    GREEN,
    RED,
    YELLOW,
    ORANGE,
)


def display_items():
    clear_screen()
    print_header("MAIN SALES MENU", BLUE)

    print()

    LEFT_WIDTH = 36
    RIGHT_WIDTH = 32
    GAP = "   "

    left_header = "Available Items"
    right_header = "Commands"

    print(
        color_text(left_header.ljust(LEFT_WIDTH), BOLD + WHITE)
        + GAP
        + color_text(right_header.ljust(RIGHT_WIDTH), BOLD + WHITE)
    )
    print("-" * LEFT_WIDTH + GAP + "-" * RIGHT_WIDTH)

    item_names = list(data_store.sales.keys())
    item_lines = []

    for i, name in enumerate(item_names, start=1):
        data = data_store.sales[name]
        plain_line = f"{i}. {name:<10} ${data['price']:<6.2f} stock: {data['inventory']}"
        item_lines.append(plain_line.ljust(LEFT_WIDTH))

    command_lines = [
    "[" + color_text("item number", BRIGHT_YELLOW) + "]".ljust(5) + " Add item to cart",
    "[" + color_text("u", BRIGHT_YELLOW) + "]".ljust(15) + " Add custom charge",
    "[" + color_text("f", BRIGHT_YELLOW) + "]".ljust(15) + " Finalize transaction",
    "[" + color_text("x", BRIGHT_YELLOW) + "]".ljust(15) + " Cancel current transaction",
    "[" + color_text("i", BRIGHT_YELLOW) + "]".ljust(15) + " Add/update inventory",
    "[" + color_text("m", BRIGHT_YELLOW) + "]".ljust(15) + " Set material costs per person",
    "[" + color_text("p", BRIGHT_YELLOW) + "]".ljust(15) + " Manage products list",
    "[" + color_text("r", BRIGHT_YELLOW) + "]".ljust(15) + " Remove saved sale",
    "[" + color_text("t", BRIGHT_YELLOW) + "]".ljust(15) + " Show totals",
    "[" + color_text("j", BRIGHT_YELLOW) + "]".ljust(15) + " Save receipt as JSON",
    "[" + color_text("c", BRIGHT_YELLOW) + "]".ljust(15) + " Save receipt as CSV",
    "[" + color_text("h", BRIGHT_YELLOW) + "]".ljust(15) + " Help / how to use",
    "[" + color_text("q", BRIGHT_YELLOW) + "]".ljust(15) + " Quit program",
    ]

    max_lines = max(len(item_lines), len(command_lines)) if data_store.sales else len(command_lines)

    for i in range(max_lines):
        left_plain = item_lines[i] if i < len(item_lines) else " " * LEFT_WIDTH
        right_plain = command_lines[i] if i < len(command_lines) else ""

        left_colored = color_text(left_plain, CYAN) if i < len(item_lines) else left_plain
        print(left_colored + GAP + right_plain)

    print()
    print(
        color_text("Overall Running Totals".ljust(LEFT_WIDTH), BOLD + MAGENTA)
        + GAP
        + color_text("Current Cart".ljust(RIGHT_WIDTH), BOLD + WHITE)
    )
    print("-" * LEFT_WIDTH + GAP + "-" * RIGHT_WIDTH)

    profit = get_total_profit()

    profit_text = f"${profit:.2f}"
    if profit < 0:
        profit_text = color_text(profit_text, RED)
    elif profit == 0:
        profit_text = color_text(profit_text, YELLOW)
    else:
        profit_text = color_text(profit_text, GREEN)

    totals_lines = [
        f"Items sold     : {color_text(str(get_total_items()), CYAN)}",
        f"Add-ons        : {color_text(str(get_addon_count()), ORANGE)}",
        f"Line items     : {color_text(str(get_total_line_items()), MAGENTA)}",
        f"Revenue        : {color_text(f'${get_total_revenue():.2f}', GREEN)}",
        f"Material cost  : {color_text(f'${get_total_material_cost():.2f}', ORANGE)}",
        f"Profit         : {profit_text}",
    ]

    cart_lines = []
    if data_store.current_cart:
        for item in data_store.current_cart:
            cart_lines.append(f"{item['item']:<15} ${item['price']:.2f}")
        cart_lines.append("-" * 24)
        cart_lines.append(
            f"Cart total: ${sum(item['price'] for item in data_store.current_cart):.2f}"
        )
    else:
        cart_lines = [
            "No current transaction.",
            "",
        ]

    max_bottom = max(len(totals_lines), len(cart_lines))

    for i in range(max_bottom):
        left = totals_lines[i] if i < len(totals_lines) else ""
        right = cart_lines[i] if i < len(cart_lines) else ""

        left_padding = LEFT_WIDTH - visible_len(left)
        if left_padding < 0:
            left_padding = 0

        print(left + (" " * left_padding) + GAP + right)


def show_totals():
    clear_screen()
    print_header("SALES TOTALS", GREEN)

    print()
    print(color_text("Items Sold", BOLD + WHITE))
    print("-" * 40)

    total_items = 0
    total_revenue = 0.0

    for name, data in data_store.sales.items():
        print(
            f" {color_text(name, CYAN):<12}: qty: {data['qty']:<3}, "
            f"revenue: ${data['revenue']:.2f}, stock left: {data['inventory']}"
        )
        total_items += data["qty"]
        total_revenue += data["revenue"]

    if not data_store.sales:
        print_warning("No products have been added yet.")

    maker_summary = get_profit_by_maker()

    print()
    print(color_text("Overall Summary", BOLD + ORANGE))
    print("-" * 40)

    overall_profit = get_total_profit()

    overall_profit_text = f"${overall_profit:.2f}"
    if overall_profit < 0:
        overall_profit_text = color_text(overall_profit_text, RED)
    elif overall_profit == 0:
        overall_profit_text = color_text(overall_profit_text, YELLOW)
    else:
        overall_profit_text = color_text(overall_profit_text, GREEN)

    print(f" Total items sold : {color_text(str(total_items), CYAN)}")
    print(f" Add-ons sold     : {color_text(str(get_addon_count()), ORANGE)}")
    print(f" Line items       : {color_text(str(get_total_line_items()), MAGENTA)}")
    print(f" Total revenue    : {color_text(f'${total_revenue:.2f}', GREEN)}")
    print(f" Material cost    : {color_text(f'${get_total_material_cost():.2f}', ORANGE)}")
    print(f" Total profit     : {overall_profit_text}")

    print()
    print(color_text("Material Cost by Person", BOLD + BLUE))
    print("-" * 40)

    if maker_summary:
        for maker, data in maker_summary.items():
            print(
                f" {color_text(maker, CYAN):<12}: "
                f"materials: ${data['material_cost']:.2f}"
            )
    else:
        print_warning("No maker data available.")

    print()
    print(color_text("Profit by Person", BOLD + MAGENTA))
    print("-" * 65)

    if maker_summary:
        for maker, data in maker_summary.items():
            profit = data["profit"]
            profit_text = f"${profit:.2f}"

            if profit < 0:
                profit_text = color_text(profit_text, RED)
            elif profit == 0:
                profit_text = color_text(profit_text, YELLOW)
            else:
                profit_text = color_text(profit_text, GREEN)

            print(
                f" {color_text(maker, CYAN):<12}: "
                f"items: {data['items_sold']:<3}, "
                f"revenue: ${data['revenue']:.2f}, "
                f"profit: {profit_text}"
            )
    else:
        print_warning("No maker data available.")

    pause()