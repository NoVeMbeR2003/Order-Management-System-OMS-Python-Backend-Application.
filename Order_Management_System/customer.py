import json
import random
from datetime import datetime
import os



class customerPanel:
    def __init__(self):
        self.orders = {}
        """ list of the products """
        self.products = {
            'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
            'Clothing': ['Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
            'Books': ['Fiction', 'Non-Fiction', 'Textbook', 'Comic', 'Magazine'],
            'Home Appliances': ['Refrigerator', 'Microwave', 'Washing Machine', 'Fan', 'Iron'],
            'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Car'],
            'Sports Equipment': ['Football', 'Basketball', 'Tennis Racket', 'Yoga Mat', 'Dumbbells'],
            'Beauty Products': ['Shampoo', 'Perfume', 'Makeup Kit', 'Cream', 'Soap'],
            'Groceries': ['Rice', 'Wheat', 'Sugar', 'Oil', 'Spices'],
            'Automotive Parts': ['Tire', 'Battery', 'Oil Filter', 'Brake Pad', 'Headlight'],
            'Health Supplements': ['Vitamins', 'Protein Powder', 'Omega-3', 'Calcium', 'Multivitamin']
        }



    """ Generate a new Order id """
    def generate_order_id(self):
        return f"ORD{random.randint(10000, 99999)}"
    


    """Save order to a JSON file"""
    def save_order(self, user_name, order_data):
       
        filename=f"orders/{user_name}_{order_data['order_id']}.json"
        
        os.makedirs('orders', exist_ok=True)
        with open(filename,'w') as file :
            json.dump(order_data,file,indent=4)
        return filename

        pass


    """Validate product quantity"""
    def validate_quantity(self):
        
        while True:
            try:
                quantity = int(input("Enter quantity (min 1, max 100): "))
                if quantity <= 1:
                    print(" Quantity must be at least 1.")
                elif quantity > 100:
                    print(" Maximum quantity is 100.")
                else:
                    return quantity
            except Exception as e :
                print(f" Please enter a valid number.{e}")
    
    
    
    
    
    
    """Validate user age"""
    def validate_age(self):
       while True:
        try:
            age=int(input("Please enter your age :- "))
            if age<=18:
                print("You must be at least 18 years old to place an order.")
                return None
            elif age>=100:
                print('Please enter a valid age ')
                continue
            return age 
        except Exception as e:
            print(f"Please enter the right thing{e}")
        
        
    
    
    """Place a new order"""
    def place_order(self,user_name):
       
        print("\n" + "="*50)
        print("PLACE ORDER".center(50))
        print("="*50)
        
        # Validate age
        age = self.validate_age()
        if age is None:
            return
        
        # Get location
        location = input("Enter your delivery location: ").upper().strip()
        if not location:
            print(" Location cannot be empty.")
            return
        
        # Display products and get selection
        self.display_products()
        
        try:
            # Select category
            category_num = int(input("\nSelect product category (number): "))
            if category_num < 1 or category_num > len(self.products):
                print(" Invalid category selection.")
                return
            
            category = list(self.products.keys())[category_num - 1]
            
            # Select product
            print(f"\nAvailable in {category}:")
            for i, item in enumerate(self.products[category], 1):
                print(f"{i}. {item}")
            
            product_num = int(input("Select product (number): "))
            if product_num < 1 or product_num > len(self.products[category]):
                print("Invalid product selection.")
                return
            
            product = self.products[category][product_num - 1]
            
            # Get quantity
            quantity = self.validate_quantity()
            if quantity is None:
                return
            
            # Generate order ID
            order_id = self.generate_order_id()
            
            # Create order data
            order_data = {
                "order_id": order_id,
                "user_name": user_name,
                "user_age": age,
                "user_location": location,
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_category": category,
                "product_name": product,
                "quantity": quantity,
                "order_status": "Confirmed",
                "payment_statusF"  : "Pending"
            }
            
            # Save order
            filename = self.save_order(user_name, order_data)
            print(f"\n✅ Order placed successfully!")
            print(f"📦 Order ID: {order_id}")
            print(f"📁 Saved to: {filename}")
            
        except ValueError:
            print("Invalid input. Please enter numbers only.")
    


    
    
    
    """Display available product categories and items"""
    def display_products(self):
        
        print("\n" + "="*50)
        print("AVAILABLE PRODUCTS".center(50))
        print("="*50)
        
        for i, (category, items) in enumerate(self.products.items(), 1):
            print(f"\n{i}. {category}:")
            for j, item in enumerate(items, 1):
                print(f"   {j}. {item}")
        print("\n" + "="*50)
     


      
    
    """Delete order file"""
    def delete_order(self, filename):
        
        try:
            os.remove(f"orders/{filename}")
            return True
        except FileNotFoundError:
            return False
    



    """Load order from JSON file"""
    def load_order(self, order_id, user_name=None):
       
        try:
            if user_name:
                
                for filename in os.listdir('orders'):
                    if filename.startswith(user_name) and order_id in filename:
                        with open(f"orders/{filename}", "r") as file:
                            return json.load(file)
            else:
              
                for filename in os.listdir('orders'):
                    if order_id in filename:
                        with open(f"orders/{filename}", "r") as file:
                            return json.load(file)
            return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    



    def update_order(self, user_name):
        """Update an existing order"""
        print("\n" + "="*50)
        print("UPDATE ORDER".center(50))
        print("="*50)
        
        order_id = input("Enter order ID to update: ").strip()
        
        try:
            order = self.load_order(order_id, user_name)
            if order:
                print(f"\nCurrent Order Details:")
                print(f"Product: {order['product_name']}")
                print(f"Quantity: {order['quantity']}")
                print(f"Location: {order['user_location']}")
                print(f"Status: {order['order_status']}")
                
                if order['order_status'] != 'Confirmed':
                    print("Only confirmed orders can be updated.")
                    return
                
                print("\nWhat would you like to update?")
                print("1. Quantity")
                print("2. Delivery Location")
                print("3. Cancel")
                
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    new_quantity = self.validate_quantity()
                    if new_quantity:
                        order['quantity'] = new_quantity
                        print(f"✅ Quantity updated to {new_quantity}")
                        
                elif choice == '2':
                    new_location = input("Enter new delivery location: ").upper().strip()
                    if new_location:
                        order['user_location'] = new_location
                        print(f"✅ Location updated to {new_location}")
                        
                elif choice == '3':
                    print("Update cancelled.")
                    return
                else:
                    print(" Invalid choice.")
                    return
                
                # Save updated order
                order['order_status'] = 'Updated'
                filename = self.save_order(user_name, order)
                print(f"✅ Order updated successfully!")
                print(f"📁 Updated file: {filename}")
                
            else:
                print("Order not found.")
        except Exception as e:
            print(f" Error: {e}")
    

   
    def cancel_order(self, user_name):
        """Cancel an existing order"""
        print("\n" + "="*50)
        print("CANCEL ORDER".center(50))
        print("="*50)
        
        order_id = input("Enter order ID to cancel: ").strip()
        
        try:
            order = self.load_order(order_id, user_name)
            if order:
                print(f"\nOrder Details:")
                print(f"Product: {order['product_name']}")
                print(f"Quantity: {order['quantity']}")
                print(f"Date: {order['order_date']}")
                print(f"Current Status: {order['order_status']}")
                
                confirm = input("\nAre you sure you want to cancel this order? (yes/no): ").lower()
                if confirm == 'yes':
                    # Find and delete the file
                    for filename in os.listdir('orders'):
                        if order_id in filename:
                            if self.delete_order(filename):
                                print(f"✅ Order {order_id} cancelled successfully.")
                            else:
                                print(" Failed to cancel order.")
                            return
                else:
                    print("Cancellation aborted.")
            else:
                print(" Order not found.")
        except Exception as e:
            print(f"Error: {e}")
   
   
    def customer_panel(self):
      while True:
          print("\n"+"="*50)
          print("CUSTOMER PANEL".center(50))
          print("="*50)



          user_name=input("Please enter your name :- ").upper().strip()
          if not user_name:
              print("Name cannot be empty. ")
              continue

    
          while True:
                print("\n" + "-"*50)
                print("Please select your option:")
                print("1. 📦 Place Order")
                print("2. 👁️ View Orders")
                print("3. ❌ Cancel Order")
                print("4. ✏️ Update Order")
                print("5. 📋 View Products")
                print("6. 🔄 Switch User")
                print("7. 🚪 Exit")
                print("-"*50)
                
                try:
                    user_choice = int(input("Enter your choice Number : "))
                    
                    if user_choice == 1:
                        self.place_order(user_name)
                    
                    elif user_choice == 2:
                        self.view_order(user_name)
                    
                    elif user_choice == 3:
                        self.cancel_order(user_name)
                    
                    elif user_choice == 4:
                        self.update_order(user_name)
                    
                    elif user_choice == 5:
                        self.display_products()
                    
                    elif user_choice == 6:
                        print("Switching user...")
                        break
                    
                    elif user_choice == 7:
                        print("\n👋 Thank you for using our Order Management System!")
                        return
                    
                    else:
                        print(" Invalid choice. Please try again.")
                        
                except ValueError:
                    print("Please enter a valid number.")




