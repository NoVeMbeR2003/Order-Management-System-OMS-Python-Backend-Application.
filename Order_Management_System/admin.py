import os
import json
from datetime import datetime
from customer import customerPanel
class adminPanel:
    
    def admin_login(self):
        """Authenticate admin user"""
        print("\n" + "="*50)
        print("ADMIN LOGIN".center(50))
        print("="*50)

        """username :- admin
           password :- admin123"""
        
        username = input("Username: ").upper().strip()
        password = input("Password: ").strip()
        
        if username == "ADMIN" and password == "ADMIN123":
            print(f"✅ Welcome, {username}!")
            return username
        else:
            print("❌ Invalid credentials!")
            return None







    def view_all_orders(self):
        """View all orders in the system"""
        print("\n" + "="*50)
        print("ALL ORDERS".center(50))
        print("="*50)
        
        try:
            orders = []
            for filename in os.listdir('orders'):
                with open(f"orders/{filename}", "r") as file:
                    order = json.load(file)
                    orders.append(order)
            
            # Sort by date (newest first)
            orders.sort(key=lambda x: x['order_date'], reverse=True)
            
            if not orders:
                print("❌ No orders found.")
                return
            
            print(f"Total Orders: {len(orders)}")
            print("-" * 50)
            
            for i, order in enumerate(orders, 1):
                print(f"\n{i}. Order ID: {order['order_id']}")
                print(f"   Customer: {order['user_name']}")
                print(f"   Date: {order['order_date']}")
                print(f"   Product: {order['product_name']} (x{order['quantity']})")
                print(f"   Status: {order['order_status']}")
                print(f"   Payment: {order['payment_status']}")
                
        except FileNotFoundError:
            print("❌ No orders directory found.")
    
    
    
    
    
    
    
    
    
    
    
    
    def search_orders(self):
        """Search orders by various criteria"""
        print("\n" + "="*50)
        print("SEARCH ORDERS".center(50))
        print("="*50)
        
        print("Search by:")
        print("1. Order ID")
        print("2. Customer Name")
        print("3. Product Category")
        print("4. Date Range")
        print("5. Order Status")
        
        choice = input("\nEnter your choice: ")
        
        try:
            orders = []
            for filename in os.listdir('orders'):
                with open(f"orders/{filename}", "r") as file:
                    orders.append(json.load(file))
            
            results = []
            
            if choice == '1':
                order_id = input("Enter Order ID: ").strip()
                results = [o for o in orders if order_id in o['order_id']]
            
            elif choice == '2':
                customer = input("Enter Customer Name: ").upper().strip()
                results = [o for o in orders if customer in o['user_name']]
            
            elif choice == '3':
                category = input("Enter Product Category: ").strip()
                results = [o for o in orders if category.lower() in o['product_category'].lower()]
            
            elif choice == '4':
                print("Enter date range (YYYY-MM-DD):")
                start = input("Start date: ").strip()
                end = input("End date: ").strip()
                results = [o for o in orders if start <= o['order_date'][:10] <= end]
            
            elif choice == '5':
                status = input("Enter Status (Confirmed/Cancelled/Updated): ").strip()
                results = [o for o in orders if o['order_status'].lower() == status.lower()]
            
            else:
                print("❌ Invalid choice")
                return
            
            # Display results
            if results:
                print(f"\n✅ Found {len(results)} order(s):")
                for order in results:
                    print(f"\n📦 Order ID: {order['order_id']}")
                    print(f"   Customer: {order['user_name']}")
                    print(f"   Product: {order['product_name']}")
                    print(f"   Status: {order['order_status']}")
            else:
                print("❌ No orders found.")
                
        except FileNotFoundError:
            print("❌ No orders directory found.")
    
    
    
    
    
    def update_order_status(self):
        """Update order status (admin only)"""
        print("\n" + "="*50)
        print("UPDATE ORDER STATUS".center(50))
        print("="*50)
        
        order_id = input("Enter Order ID: ").strip()
       
        c = customerPanel()
        order = c.load_order(order_id)
        if not order:
            print("❌ Order not found.")
            return
        
        print(f"\nCurrent Order Details:")
        print(f"Customer: {order['user_name']}")
        print(f"Product: {order['product_name']}")
        print(f"Current Status: {order['order_status']}")
        print(f"Payment Status: {order['payment_status']}")
        
        print("\nNew Status:")
        print("1. Confirmed")
        print("2. Processing")
        print("3. Shipped")
        print("4. Delivered")
        print("5. Cancelled")
        
        choice = input("Select status: ")
        status_map = {
            '1': 'Confirmed',
            '2': 'Processing',
            '3': 'Shipped', 
            '4': 'Delivered',
            '5': 'Cancelled'
        }
        
        if choice in status_map:
            order['order_status'] = status_map[choice]
            order['status_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.save_order(order['user_name'], order)
            print(f"✅ Order status updated to: {status_map[choice]}")
        else:
            print("❌ Invalid choice.")
    
    def update_payment_status(self):
        """Update payment status"""
        print("\n" + "="*50)
        print("UPDATE PAYMENT STATUS".center(50))
        print("="*50)
        
        order_id = input("Enter Order ID: ").strip()
        c = customerPanel()
        order = c.load_order(order_id)
        if not order:
            print("❌ Order not found.")
            return
        
        print(f"\nCurrent Payment Status: {order['payment_status']}")
        
        print("\nNew Payment Status:")
        print("1. Pending")
        print("2. Paid")
        print("3. Failed")
        print("4. Refunded")
        
        choice = input("Select status: ")
        status_map = {
            '1': 'Pending',
            '2': 'Paid',
            '3': 'Failed',
            '4': 'Refunded'
        }
        
        if choice in status_map:
            order['payment_status'] = status_map[choice]
            order['payment_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.save_order(order['user_name'], order)
            print(f"✅ Payment status updated to: {status_map[choice]}")
        else:
            print("❌ Invalid choice.")
    
    
    def admin_panel(self):
        """Main admin panel"""
        # Authenticate admin
        admin_user = self.admin_login()
        if not admin_user:
            return
        
        while True:
            print("\n" + "="*50)
            print(f"ADMIN PANEL - Welcome {admin_user}".center(50))
            print("="*50)
            
            print("1. 👁️ View All Orders")
            print("2. 🔍 Search Orders")
            print("3. 📊 Update Order Status")
            print("4. 💰 Update Payment Status")
            print("5. 🚪 Logout")
            print("-"*50)
            
            try:
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    self.view_all_orders()
                
                elif choice == '2':
                    self.search_orders()
                
                elif choice == '3':
                    self.update_order_status()
                
                elif choice == '4':
                    self.update_payment_status()
               
                
                elif choice == '5':
                    print("\n👋 Logging out...")
                    break
                
                else:
                    print("❌ Invalid choice.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")


# s1=adminPanel()
# s1.admin_panel()
