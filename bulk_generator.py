"""
Bulk Generator Module
Handles bulk generation of tags with QR codes and database storage
"""

import os
import csv
from datetime import datetime
from tag_generator import generate_tags_for_category, get_object_code_details, OBJECT_CODES
from hidden_serial import calculate_hidden_serial
from qr_generator import generate_qr_code
from database import TagItDatabase


class BulkGenerator:
    """Manages bulk tag generation, QR code creation, and database storage"""
    
    def __init__(self, base_output_folder='stickers', db_path='tagit_pro.db'):
        """
        Initialize bulk generator.
        
        Args:
            base_output_folder (str): Base folder for storing QR codes
            db_path (str): Path to SQLite database
        """
        self.base_output_folder = base_output_folder
        self.db = TagItDatabase(db_path)
        self.generated_tags = []
        self.manifest_file = None
    
    def generate_bulk_tags(self, ne_count=0, se_count=0, pe_count=0):
        """
        Generate tags for all categories in bulk.
        
        Args:
            ne_count (int): Number of non-electronic tags to generate
            se_count (int): Number of standard electronic tags to generate
            pe_count (int): Number of premium electronic tags to generate
        
        Returns:
            dict: Statistics about generated tags
        """
        stats = {
            'total': 0,
            'non_electronic': 0,
            'standard_electronic': 0,
            'premium_electronic': 0,
            'failed': 0
        }
        
        self.generated_tags = []
        
        print("\n" + "=" * 70)
        print("BULK TAG GENERATION")
        print("=" * 70)
        
        # Generate Non-Electronic tags
        if ne_count > 0:
            print(f"\n[1/3] Generating {ne_count} Non-Electronic Tags (BLACK - ₦200)...")
            stats['non_electronic'] = self._generate_category_tags(
                'non_electronic', ne_count
            )
            stats['total'] += stats['non_electronic']
        
        # Generate Standard Electronic tags
        if se_count > 0:
            print(f"\n[2/3] Generating {se_count} Standard Electronic Tags (GREEN - ₦500)...")
            stats['standard_electronic'] = self._generate_category_tags(
                'standard_electronic', se_count
            )
            stats['total'] += stats['standard_electronic']
        
        # Generate Premium Electronic tags
        if pe_count > 0:
            print(f"\n[3/3] Generating {pe_count} Premium Electronic Tags (BLUE - ₦1,000)...")
            stats['premium_electronic'] = self._generate_category_tags(
                'premium_electronic', pe_count
            )
            stats['total'] += stats['premium_electronic']
        
        # Generate manifest
        if self.generated_tags:
            self.manifest_file = self._generate_manifest()
        
        print("\n" + "=" * 70)
        print("GENERATION COMPLETE")
        print("=" * 70)
        print(f"✓ Total tags generated: {stats['total']}")
        print(f"  - Non-Electronic: {stats['non_electronic']}")
        print(f"  - Standard Electronic: {stats['standard_electronic']}")
        print(f"  - Premium Electronic: {stats['premium_electronic']}")
        if self.manifest_file:
            print(f"✓ Manifest saved: {self.manifest_file}")
        
        return stats
    
    def _generate_category_tags(self, category, count):
        """
        Generate tags for a specific category.
        
        Args:
            category (str): Category name
            count (int): Number of tags to generate
        
        Returns:
            int: Number of successfully generated tags
        """
        success_count = 0
        available_codes = OBJECT_CODES[category]['codes']
        
        for i in range(count):
            try:
                # Get object code for this tag
                object_code = available_codes[i % len(available_codes)]
                
                # Generate tag number
                from tag_generator import _tag_sequence
                number = _tag_sequence.get_next_number()
                import random
                random_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                middle_number = number
                descending_letter = _tag_sequence.get_next_letter()
                
                prefix = 'NE' if category == 'non_electronic' else 'EL'
                tag_number = f"{prefix}-{number}{random_letter}{middle_number}{descending_letter}-{object_code}"
                
                # Calculate hidden serial
                hidden_serial = calculate_hidden_serial(tag_number)
                
                # Get category details
                details = get_object_code_details(object_code)
                
                # Create QR code
                category_folder = category
                output_folder = os.path.join(self.base_output_folder, category_folder)
                qr_file_path = generate_qr_code(tag_number, details['color'], output_folder)
                
                # Add to database
                tag_id = self.db.add_tag(
                    tag_number=tag_number,
                    hidden_serial=hidden_serial,
                    object_code=object_code,
                    category=category,
                    price=details['price'],
                    qr_color=details['color'],
                    qr_file_path=qr_file_path
                )
                
                if tag_id:
                    self.generated_tags.append({
                        'tag_number': tag_number,
                        'hidden_serial': hidden_serial,
                        'object_code': object_code,
                        'category': category,
                        'price': details['price'],
                        'qr_color': details['color_name'],
                        'qr_file_path': qr_file_path
                    })
                    success_count += 1
                    
                    # Print progress
                    progress = (i + 1) / count * 100
                    print(f"  [{progress:5.1f}%] {tag_number} → {hidden_serial} ✓")
            
            except Exception as e:
                print(f"  ✗ Failed at index {i}: {str(e)}")
        
        return success_count
    
    def _generate_manifest(self):
        """
        Generate manifest CSV file with all generated tags.
        
        Returns:
            str: Path to manifest file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        manifest_filename = f"manifest_{timestamp}.csv"
        manifest_path = os.path.join(self.base_output_folder, manifest_filename)
        
        # Create base folder if needed
        os.makedirs(self.base_output_folder, exist_ok=True)
        
        try:
            with open(manifest_path, 'w', newline='') as csvfile:
                fieldnames = ['tag_number', 'hidden_serial', 'object_code', 'category', 
                            'price', 'qr_color', 'qr_file_path', 'generated_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for tag in self.generated_tags:
                    tag['generated_at'] = datetime.now().isoformat()
                    writer.writerow(tag)
            
            return manifest_path
        
        except Exception as e:
            print(f"✗ Error creating manifest: {str(e)}")
            return None
    
    def get_statistics(self):
        """
        Get current generation statistics from database.
        
        Returns:
            dict: Statistics about all tags
        """
        return self.db.get_sales_report()
    
    def close(self):
        """Close database connection"""
        self.db.close()


def test_bulk_generation():
    """Test bulk generation with sample data"""
    generator = BulkGenerator('test_stickers', 'test_tagit.db')
    
    print("\nTest Bulk Generation:")
    print("-" * 70)
    
    # Generate sample tags
    stats = generator.generate_bulk_tags(
        ne_count=5,      # 5 Non-Electronic
        se_count=3,      # 3 Standard Electronic
        pe_count=2       # 2 Premium Electronic
    )
    
    # Show statistics
    print("\nGeneration Statistics:")
    print("-" * 70)
    for category_stats in generator.get_statistics():
        print(f"\n{category_stats['category'].upper()}:")
        print(f"  Total: {category_stats['total_tags']}")
        print(f"  Available: {category_stats['available']}")
        print(f"  Sold/Active: {category_stats['sold'] + category_stats['active']}")
        print(f"  Revenue: ₦{category_stats['revenue']:,}")
    
    generator.close()


if __name__ == "__main__":
    test_bulk_generation()
