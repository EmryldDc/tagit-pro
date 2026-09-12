"""
TagIt Pro - Main CLI Interface
Complete QR code generation system for campus lost-and-found stickers
"""

import os
import sys
from datetime import datetime
from tag_generator import reset_sequence, OBJECT_CODES
from hidden_serial import calculate_hidden_serial, verify_sticker
from bulk_generator import BulkGenerator
from database import TagItDatabase


class TagItProCLI:
    """Command-line interface for TagIt Pro"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.generator = BulkGenerator('stickers', 'tagit_pro.db')
        self.db = self.generator.db
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.print_header("TagIt Pro - Lost & Found Management System")
        print("""
  1. Generate Bulk Stickers
  2. Assign Sticker to Student
  3. Verify Sticker Authenticity
  4. Search Sticker by Tag Number
  5. List Available Stickers
  6. View Sales Report
  7. Exit
  
""")
    
    def menu_generate_bulk(self):
        """Generate bulk stickers"""
        self.print_header("Generate Bulk Stickers")
        
        # Reset sequence for new batch
        reset_sequence()
        
        try:
            ne_count = int(input("Enter number of Non-Electronic tags (₦200, BLACK): "))
            se_count = int(input("Enter number of Standard Electronic tags (₦500, GREEN): "))
            pe_count = int(input("Enter number of Premium Electronic tags (₦1,000, BLUE): "))
            
            if ne_count < 0 or se_count < 0 or pe_count < 0:
                print("✗ Please enter positive numbers")
                return
            
            if ne_count + se_count + pe_count == 0:
                print("✗ Please enter at least one tag quantity")
                return
            
            confirm = input(f"\nGenerate {ne_count + se_count + pe_count} total tags? (yes/no): ")
            if confirm.lower() != 'yes':
                print("✗ Generation cancelled")
                return
            
            # Generate tags
            stats = self.generator.generate_bulk_tags(ne_count, se_count, pe_count)
            
            print("\n✓ Generation completed successfully!")
            print(f"✓ Manifest file: {self.generator.manifest_file}")
            print("\nPress Enter to continue...")
            input()
        
        except ValueError:
            print("✗ Invalid input. Please enter numbers only.")
            input("Press Enter to continue...")
    
    def menu_assign_sticker(self):
        """Assign sticker to student"""
        self.print_header("Assign Sticker to Student")
        
        tag_number = input("Enter tag number (e.g., NE-1A1Z-ID): ").strip().upper()
        
        # Check if tag exists
        tag = self.db.search_by_tag(tag_number)
        if not tag:
            print(f"✗ Tag {tag_number} not found in database")
            input("Press Enter to continue...")
            return
        
        if tag['status'] not in ['AVAILABLE', 'SOLD']:
            print(f"✗ Tag status is {tag['status']} (not assignable)")
            input("Press Enter to continue...")
            return
        
        print(f"\nTag Details:")
        print(f"  Category: {tag['category']}")
        print(f"  Price: ₦{tag['price']}")
        print(f"  Current Status: {tag['status']}")
        
        # Get student info
        owner_name = input("\nEnter student name: ").strip()
        owner_email = input("Enter student email: ").strip()
        owner_phone = input("Enter student phone: ").strip()
        item_name = input("Enter item name: ").strip()
        
        imei = None
        if tag['category'] in ['standard_electronic', 'premium_electronic']:
            imei = input("Enter IMEI/Serial number (optional): ").strip() or None
        
        # Confirm assignment
        print("\nAssignment Details:")
        print(f"  Student: {owner_name}")
        print(f"  Email: {owner_email}")
        print(f"  Phone: {owner_phone}")
        print(f"  Item: {item_name}")
        if imei:
            print(f"  IMEI: {imei}")
        
        confirm = input("\nConfirm assignment? (yes/no): ")
        if confirm.lower() != 'yes':
            print("✗ Assignment cancelled")
            input("Press Enter to continue...")
            return
        
        # Update database
        if self.db.assign_to_student(tag_number, owner_name, owner_email, owner_phone, item_name, imei):
            print(f"\n✓ Sticker {tag_number} assigned to {owner_name}")
        else:
            print(f"✗ Failed to assign sticker")
        
        input("Press Enter to continue...")
    
    def menu_verify_sticker(self):
        """Verify sticker authenticity"""
        self.print_header("Verify Sticker Authenticity")
        
        tag_number = input("Enter tag number (e.g., NE-1A1Z-ID): ").strip().upper()
        hidden_serial = input("Enter hidden serial (e.g., HSN-29): ").strip().upper()
        
        # Verify in database
        tag = self.db.verify_sticker(tag_number, hidden_serial)
        
        if tag:
            print("\n✓ STICKER VERIFIED - AUTHENTIC")
            print(f"\nTag Information:")
            print(f"  Tag Number: {tag['tag_number']}")
            print(f"  Hidden Serial: {tag['hidden_serial']}")
            print(f"  Category: {tag['category']}")
            print(f"  Object Code: {tag['object_code']}")
            print(f"  Price: ₦{tag['price']}")
            print(f"  Status: {tag['status']}")
            
            if tag['owner_name']:
                print(f"\nOwner Information:")
                print(f"  Name: {tag['owner_name']}")
                print(f"  Email: {tag['owner_email']}")
                print(f"  Phone: {tag['owner_phone']}")
                print(f"  Item: {tag['item_name']}")
        else:
            print("\n✗ VERIFICATION FAILED - NOT AUTHENTIC")
            print("The tag number and hidden serial do not match in the system.")
        
        input("Press Enter to continue...")
    
    def menu_search_sticker(self):
        """Search sticker by tag number"""
        self.print_header("Search Sticker by Tag Number")
        
        tag_number = input("Enter tag number: ").strip().upper()
        
        tag = self.db.search_by_tag(tag_number)
        
        if not tag:
            print(f"\n✗ Tag {tag_number} not found")
        else:
            print(f"\n✓ Tag Found:")
            print(f"\nBasic Information:")
            print(f"  Tag Number: {tag['tag_number']}")
            print(f"  Hidden Serial: {tag['hidden_serial']}")
            print(f"  Category: {tag['category']}")
            print(f"  Object Code: {tag['object_code']}")
            print(f"  Price: ₦{tag['price']}")
            print(f"  Status: {tag['status']}")
            print(f"  Created: {tag['created_at']}")
            
            if tag['owner_name']:
                print(f"\nOwner Information:")
                print(f"  Name: {tag['owner_name']}")
                print(f"  Email: {tag['owner_email']}")
                print(f"  Phone: {tag['owner_phone']}")
                print(f"  Item: {tag['item_name']}")
                if tag['imei']:
                    print(f"  IMEI: {tag['imei']}")
                print(f"  Activated: {tag['activated_at']}")
            
            if tag['qr_file_path']:
                print(f"\nQR Code: {tag['qr_file_path']}")
        
        input("Press Enter to continue...")
    
    def menu_list_available(self):
        """List available stickers"""
        self.print_header("List Available Stickers")
        
        print("\nCategories:")
        print("  1. Non-Electronic (BLACK - ₦200)")
        print("  2. Standard Electronic (GREEN - ₦500)")
        print("  3. Premium Electronic (BLUE - ₦1,000)")
        print("  4. All Categories")
        
        choice = input("\nSelect category (1-4): ").strip()
        
        category_map = {
            '1': 'non_electronic',
            '2': 'standard_electronic',
            '3': 'premium_electronic',
            '4': None
        }
        
        category = category_map.get(choice)
        
        if choice not in category_map:
            print("✗ Invalid choice")
            input("Press Enter to continue...")
            return
        
        available = self.db.list_available_stickers(category)
        
        if not available:
            print("\n✗ No available stickers found")
        else:
            print(f"\n✓ Found {len(available)} available stickers:\n")
            print(f"{'Tag Number':<20} {'Object':<8} {'Category':<20} {'Price':<10}")
            print("-" * 60)
            
            for tag in available:
                print(f"{tag['tag_number']:<20} {tag['object_code']:<8} {tag['category']:<20} ₦{tag['price']:<9}")
        
        input("Press Enter to continue...")
    
    def menu_sales_report(self):
        """Display sales report"""
        self.print_header("Sales Report")
        
        stats = self.db.get_sales_report()
        
        if not stats:
            print("\n✗ No data available")
        else:
            total_revenue = 0
            total_tags = 0
            total_sold = 0
            
            print("\nCategory Breakdown:")
            print("-" * 80)
            print(f"{'Category':<25} {'Total':<10} {'Available':<12} {'Sold/Active':<12} {'Revenue':<15}")
            print("-" * 80)
            
            for row in stats:
                category = row['category'].replace('_', ' ').title()
                total = row['total_tags'] or 0
                available = row['available'] or 0
                sold_active = (row['sold'] or 0) + (row['active'] or 0)
                revenue = row['revenue'] or 0
                
                print(f"{category:<25} {total:<10} {available:<12} {sold_active:<12} ₦{revenue:<14,}")
                
                total_tags += total
                total_sold += sold_active
                total_revenue += revenue
            
            print("-" * 80)
            print(f"{'TOTAL':<25} {total_tags:<10} {total_tags - total_sold:<12} {total_sold:<12} ₦{total_revenue:<14,}")
            
            print(f"\n\nSummary:")
            print(f"  Total Tags Generated: {total_tags}")
            print(f"  Tags Sold/Active: {total_sold}")
            print(f"  Tags Available: {total_tags - total_sold}")
            print(f"  Total Revenue: ₦{total_revenue:,}")
        
        input("Press Enter to continue...")
    
    def run(self):
        """Run the main CLI loop"""
        while True:
            self.print_menu()
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.menu_generate_bulk()
            elif choice == '2':
                self.menu_assign_sticker()
            elif choice == '3':
                self.menu_verify_sticker()
            elif choice == '4':
                self.menu_search_sticker()
            elif choice == '5':
                self.menu_list_available()
            elif choice == '6':
                self.menu_sales_report()
            elif choice == '7':
                print("\n✓ Thank you for using TagIt Pro!")
                print("Exiting...")
                self.generator.close()
                sys.exit(0)
            else:
                print("✗ Invalid choice. Please enter 1-7.")
                input("Press Enter to continue...")


def main():
    """Entry point"""
    try:
        cli = TagItProCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n✗ Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
