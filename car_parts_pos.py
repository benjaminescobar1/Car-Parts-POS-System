# Cashier Class
class Cashier:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username, password):
        return self.username == username and self.password == password

# Car Parts Class
class CarPart:
    def __init__(self, part_number, name, year, make, model, price, stock):
        self.part_number = part_number
        self.name = name
        self.year = year
        self.make = make
        self.model = model
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.part_number} | {self.name} | {self.year} {self.make} {self.model} | ${self.price:.2f} | Stock: {self.stock}"

# Inventory Class
class Inventory:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def search(self, keyword):
        return [
            part for part in self.parts
            if keyword.lower() in part.name.lower()
            or keyword.lower() in part.part_number.lower()
        ]

    def filter_vehicle(self, year, make, model):
        return [
            part for part in self.parts
            if part.year == year
            and part.make.lower() == make.lower()
            and part.model.lower() == model.lower()
        ]

    def reduce_stock(self, part, quantity):
        if part.stock >= quantity:
            part.stock -= quantity
            return True
        return False

    def restock(self, part, quantity):
        part.stock += quantity

# Cart Item class
class CartItem:
    def __init__(self, part, quantity):
        self.part = part
        self.quantity = quantity

    def total(self):
        return self.part.price * self.quantity

# Shopping Cart Class
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, part, quantity):
        for item in self.items:
            if item.part.part_number == part.part_number:
                item.quantity += quantity
                return
        self.items.append(CartItem(part, quantity))

    def remove_item(self, part_number):
        for item in self.items:
            if item.part.part_number == part_number:
                self.items.remove(item)
                return item
        return None

    def update_quantity(self, part_number, new_quantity):
        for item in self.items:
            if item.part.part_number == part_number:
                old_quantity = item.quantity
                item.quantity = new_quantity
                return old_quantity
        return None

    def subtotal(self):
        return sum(item.total() for item in self.items)

    def show_cart(self):
        print("\n================ CURRENT SALE ================")
        if not self.items:
            print("Cart is empty.")
        else:
            print("Part #     Name              Qty   Price    Total")
            print("-----------------------------------------------")
            for item in self.items:
                print(f"{item.part.part_number:<10} {item.part.name:<17} {item.quantity:<5} ${item.part.price:<7.2f} ${item.total():.2f}")
        print("===============================================")

# Tax Calculator Class
class TaxCalculator:
    TAX_RATE = 0.0488

    def calculate_tax(self, subtotal):
        return subtotal * self.TAX_RATE

# Payment Class
class Payment:
    def __init__(self, amount):
        self.amount = amount

# Cash Payment Class
class CashPayment(Payment):
    def __init__(self, amount, cash_received):
        super().__init__(amount)
        self.cash_received = cash_received

    def approved(self):
        return self.cash_received >= self.amount

    def change(self):
        return self.cash_received - self.amount

# Card Payment Class
class CardPayment(Payment):
    def __init__(self, amount, last_four):
        super().__init__(amount)
        self.last_four = last_four

    def approved(self):
        return len(self.last_four) == 4 and self.last_four.isdigit()

# Sales Transcation Class
class SaleTransaction:
    def __init__(self, transaction_number, cart):
        self.transaction_number = transaction_number
        self.cart = cart
        self.tax_calculator = TaxCalculator()
        self.subtotal = 0
        self.tax = 0
        self.total = 0
        self.payment_type = "Not Paid"

    def calculate_total(self):
        self.subtotal = self.cart.subtotal()
        self.tax = self.tax_calculator.calculate_tax(self.subtotal)
        self.total = self.subtotal + self.tax

    def show_totals(self):
        self.calculate_total()
        print("\n---------------- TOTALS ----------------")
        print(f"Subtotal: ${self.subtotal:.2f}")
        print(f"Tax:      ${self.tax:.2f}")
        print(f"Total:    ${self.total:.2f}")
        print("----------------------------------------")

# Return and Refund Class
class ReturnRefund:
    def process_refund(self, inventory, part, quantity):
        inventory.restock(part, quantity)
        return part.price * quantity

# Receipt Class
class Receipt:
    def __init__(self, sale):
        self.sale = sale

    def print_receipt(self):
        print("\n============== RECEIPT ==============")
        print("Car Parts Store")
        print(f"Transaction #: {self.sale.transaction_number}")
        print("-------------------------------------")
        for item in self.sale.cart.items:
            print(f"{item.part.name} x{item.quantity}: ${item.total():.2f}")
        print("-------------------------------------")
        print(f"Subtotal: ${self.sale.subtotal:.2f}")
        print(f"Tax:      ${self.sale.tax:.2f}")
        print(f"Total:    ${self.sale.total:.2f}")
        print(f"Payment:  {self.sale.payment_type}")
        print("Thank you for your purchase!")
        print("=====================================")

# Function to Creating Database Part Inventory
def create_inventory():
    inventory = Inventory()
    inventory.add_part(CarPart("OF100", "Oil Filter", 2015, "Honda", "Accord", 10.00, 10))
    inventory.add_part(CarPart("AF200", "Air Filter", 2015, "Honda", "Accord", 18.99, 8))
    inventory.add_part(CarPart("BP300", "Brake Pads", 2014, "BMW", "335i", 45.00, 5))
    inventory.add_part(CarPart("SP400", "Spark Plugs", 2011, "Mitsubishi", "Evo X", 7.50, 20))
    inventory.add_part(CarPart("WB500", "Wiper Blades", 2015, "Honda", "Accord", 14.99, 15))
    return inventory

# FUntion to Show Parts
def show_parts(parts):
    if not parts:
        print("No parts found.")
        return

    print("\nSearch Results:")
    for index, part in enumerate(parts, start=1):
        print(f"{index}. {part}")

# Funtion to Select Parts
def select_part(parts):
    if not parts:
        return None

    try:
        choice = int(input("Select item number: "))
        return parts[choice - 1]
    except:
        print("Invalid selection.")
        return None

# Function for Login Screen
def login_screen():
    print("=====================================")
    print("      CAR PARTS POS LOGIN")
    print("=====================================")

    cashier = Cashier("BennyBen", "password123456")

    username = input("Username: ")
    password = input("Password: ")

    if cashier.login(username, password):
        print("\nLogin successful.")
        return True

    print("\nLogin failed.")
    return False

# Function for Checkout Screen
def checkout_screen(sale):
    sale.show_totals()

    print("\nPayment Options")
    print("1. Cash Payment")
    print("2. Card Payment")
    print("3. Cancel Checkout")

    choice = input("Select payment option: ")

    if choice == "1":
        cash = float(input("Enter cash received: $"))
        payment = CashPayment(sale.total, cash)

        if payment.approved():
            sale.payment_type = "Cash"
            print(f"Cash approved. Change due: ${payment.change():.2f}")
            return True
        else:
            print("Not enough cash received.")
            return False

    elif choice == "2":
        last_four = input("Enter last 4 digits of card: ")
        payment = CardPayment(sale.total, last_four)

        if payment.approved():
            sale.payment_type = "Card"
            print("Card approved. Sale complete.")
            return True
        else:
            print("Card declined.")
            return False

    return False

# Function for Return Screen
def return_screen(inventory):
    print("\n=========== RETURN / REFUND ===========")
    receipt_number = input("Enter receipt number: ")

    print("\nAvailable parts for return:")
    show_parts(inventory.parts)

    part = select_part(inventory.parts)

    if part:
        quantity = int(input("Enter return quantity: "))
        refund = ReturnRefund()
        amount = refund.process_refund(inventory, part, quantity)
        print(f"Refund completed for receipt {receipt_number}.")
        print(f"Refund amount: ${amount:.2f}")

# Function for POS screen
def pos_screen():
    inventory = create_inventory()
    cart = ShoppingCart()
    sale = SaleTransaction("TXN1001", cart)

    while True:
        print("\n================ CAR PARTS POS ================")
        print("1. Search part by name or part number")
        print("2. Filter parts by car year, make and model")
        print("3. Add part to cart")
        print("4. Remove part from cart")
        print("5. Update quantity")
        print("6. View current sale")
        print("7. Calculate tax and total")
        print("8. Checkout / Process payment")
        print("9. Print receipt")
        print("10. Process returns or refund")
        print("11. Start new sale")
        print("12. Exit")
        print("================================================")

        choice = input("Select option: ")

        if choice == "1":
            keyword = input("Enter part name or part number: ")
            results = inventory.search(keyword)
            show_parts(results)

        elif choice == "2":
            year = int(input("Enter car year: "))
            make = input("Enter make: ")
            model = input("Enter model: ")
            results = inventory.filter_vehicle(year, make, model)
            show_parts(results)

        elif choice == "3":
            keyword = input("Search part to add: ")
            results = inventory.search(keyword)
            show_parts(results)
            part = select_part(results)

            if part:
                quantity = int(input("Enter quantity: "))

                if inventory.reduce_stock(part, quantity):
                    cart.add_item(part, quantity)
                    print(f"{part.name} x{quantity} added to cart.")
                else:
                    print("Not enough inventory.")

        elif choice == "4":
            cart.show_cart()
            part_number = input("Enter part number to remove: ")
            removed = cart.remove_item(part_number)

            if removed:
                inventory.restock(removed.part, removed.quantity)
                print(f"{removed.part.name} removed from cart.")
            else:
                print("Part not found in cart.")

        elif choice == "5":
            cart.show_cart()
            part_number = input("Enter part number to update: ")
            new_quantity = int(input("Enter new quantity: "))
            old_quantity = cart.update_quantity(part_number, new_quantity)

            if old_quantity is not None:
                print("Quantity updated.")
            else:
                print("Part not found in cart.")

        elif choice == "6":
            cart.show_cart()

        elif choice == "7":
            sale.show_totals()

        elif choice == "8":
            if not cart.items:
                print("Cannot checkout. Cart is empty.")
            else:
                completed = checkout_screen(sale)

                if completed:
                    receipt = Receipt(sale)
                    receipt.print_receipt()

        elif choice == "9":
            sale.calculate_total()
            receipt = Receipt(sale)
            receipt.print_receipt()

        elif choice == "10":
            return_screen(inventory)

        elif choice == "11":
            cart = ShoppingCart()
            sale = SaleTransaction("TXN1001", cart)
            print("New sale started.")

        elif choice == "12":
            print("Exiting POS system.")
            break

        else:
            print("Invalid option.")

# Function to start POS system
def main():
    if login_screen():
        pos_screen()

# Runs the main function when program is executed
if __name__ == "__main__":
    main()