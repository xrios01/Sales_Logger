from helpers import (
    clear_screen,
    print_header,
    print_error,
    color_text,
    pause,
    CYAN,
    BOLD,
    WHITE,
    MAGENTA,
    YELLOW,
    BRIGHT_YELLOW
)


def show_help():
    clear_screen()
    print_header("HELP / HOW TO USE", CYAN)

    print()
    print(color_text("How the program works", BOLD + WHITE))
    print("-" * 40)
    print("• Use product manager to add, edit, or delete products.")
    print("• Type an item number to add that item to the current cart.")
    print("• The first item added will ask for customer info.")
    print("• Inventory goes down automatically when an item is sold.")
    print("• Add as many items as needed for the same customer.")
    print("• Press [" + color_text("f", BRIGHT_YELLOW) + "] to finalize the transaction and send one receipt.")
    print("• Press [" + color_text("x", BRIGHT_YELLOW) + "] to cancel the current transaction.")
    print("• Removing a sale adds 1 back to inventory.")

    print()
    print(color_text("Main Menu Commands", BOLD + WHITE))
    print("-" * 40)
    print(" [" + color_text("item number", BRIGHT_YELLOW) + "]  Add item sale")
    print(" [" + color_text("u", BRIGHT_YELLOW) + "]            Add an extra charge or a discount to a cart depending on the amount sign (+/-)")
    print(" [" + color_text("f", BRIGHT_YELLOW) + "]            Finalize transaction / send one receipt")
    print(" [" + color_text("x", BRIGHT_YELLOW) + "]            Cancel current transaction")
    print(" [" + color_text("i", BRIGHT_YELLOW) + "]            Set or update inventory")
    print(" [" + color_text("m", BRIGHT_YELLOW) + "]            Set material cost by person")
    print(" [" + color_text("p", BRIGHT_YELLOW) + "]            Manage products (add/edit/delete)")
    print(" [" + color_text("r", BRIGHT_YELLOW) + "]            Remove items from sales list")
    print(" [" + color_text("t", BRIGHT_YELLOW) + "]            Show totals / profit / inventory")
    print(" [" + color_text("j", BRIGHT_YELLOW) + "]            Save receipt as JSON")
    print(" [" + color_text("c", BRIGHT_YELLOW) + "]            Save receipt as CSV")
    print(" [" + color_text("e", BRIGHT_YELLOW) + "]            Email settings")
    print(" [" + color_text("h", BRIGHT_YELLOW) + "]            Show this help screen")
    print(" [" + color_text("q", BRIGHT_YELLOW) + "]            Quit the program")

    print()
    print(color_text("User Tip", BOLD + MAGENTA))
    print("-" * 40)
    print("Make sure to set inventory, assign makers to products, and enter each person's material costs for accurate profit tracking.")

    pause()



def show_startup_guide():
    clear_screen()
    print_header("WELCOME", CYAN)

    print()
    print(color_text("This program helps you track:", BOLD + WHITE))
    print("-" * 40)
    print("• Sales")
    print("• Inventory")
    print("• Material costs")
    print("• Profit by person")
    print("• Outgoing reciepts")
    print("• CSV / JSON Sales logs")
    print()

    print(color_text("USER NOTE:", BOLD + WHITE))
    print("-" * 40)
    print("All commands entered into the program must be followed by pressing " + color_text("Enter", BRIGHT_YELLOW) + ".\n")
    print()

    while True:
        choice = input(
            color_text("Press ", YELLOW) + color_text("Enter", BRIGHT_YELLOW) +color_text(" for more information", YELLOW) + color_text(" or type ", YELLOW) + color_text("'s'", BRIGHT_YELLOW) + color_text( " to skip to main menu: ", YELLOW)
        ).strip().lower()

        if choice == "":
            break   # show guide
        elif choice == "s":
            return  # skip guide
        else:
            print_error("Invalid input.")
            print()
        

    clear_screen()
    print_header("STARTUP GUIDE", CYAN)

    print()
    print(color_text("How to begin using the program", BOLD + WHITE))
    print("-" * 45)
    print("1. Set material costs for each person.")
    print("   Use [" + color_text("m", BRIGHT_YELLOW) + "] from the main menu.")
    print()
    print("2. Set product inventory.")
    print("   Use [" + color_text("i", BRIGHT_YELLOW) + "] to enter how many of each item you currently have.")
    print()
    print("3. Add new products or edit existing ones if needed.")
    print("   Use [" + color_text("p", BRIGHT_YELLOW) + "] to manage product names, prices, inventory, and makers.")
    print()
    print("4. Start a transaction by entering an item number.")
    print("   The first item added will ask for customer information.")
    print()
    print("5. Add more items or use [" + color_text("u", BRIGHT_YELLOW) + "] to add a custom charge/add-on.")
    print()
    print("6. Press [" + color_text("f", BRIGHT_YELLOW) + "] to finalize the transaction.")
    print("   This records the sale and can email a receipt if email is provided.")
    print()
    print("7. Use [" + color_text("j", BRIGHT_YELLOW) + "] to save JSON logs or [" + color_text("c", BRIGHT_YELLOW) + "] to save CSV logs.")
    print("   These logs include totals and profit by person.")
    print()
    print(color_text("Recommended startup order:", BOLD + MAGENTA))
    print("-" * 45)
    print(" [" + color_text("m", BRIGHT_YELLOW) + "] Material costs  ->  [" + color_text("i", BRIGHT_YELLOW) + "] Inventory  ->  [" + color_text("p", BRIGHT_YELLOW) + "] Products  ->  [" + color_text("item number", BRIGHT_YELLOW) + "] Sales")
    print()

    pause()





def secret():
    clear_screen()
    print("###                         @@@@@/                        ###")
    print("#########(                  @@@@@/                 ## (#####")
    print("############                @@@@@/               ###########")
    print("   ###########(##           @@@@@/          #( ###########")
    print("   ################         @@@@@/        ################")
    print("          ########### ##(   @@@@@/  ###(###########")
    print("           ###############  @@@@@/ ###############")
    print("                  ##########@@@@@%#########")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@#       #@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@     X    @@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@#       #@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("                 ###########@@@@@%##########")
    print("          ###############   @@@@@/  ##############")
    print("         #/##########(###   @@@@@/   #)#############")
    print("  .###############          @@@@@/         ##############")
    print("  ############(#            @@@@@/          #)#############")
    print("#########(#                 @@@@@/                 #)########")
    print("#####/###                   @@@@@/                    #########")

    pause()
