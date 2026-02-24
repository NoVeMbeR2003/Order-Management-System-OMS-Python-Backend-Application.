from customer import customerPanel
from admin import adminPanel
import os
def main_menu():
    while True:
        print('\n'+'='*50)
        print("1. Customer Panel")
        print("2. Admin Panel")
        print("3. Exit")
        print('='*50)
        
        choice = input("Enter choice: ")

        if choice == "1":
            c = customerPanel()
            c.customer_panel()
        elif choice == "2":
            a = adminPanel()
            a.admin_panel()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

main_menu()
os.makedirs('orders', exist_ok=True)