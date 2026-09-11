"""
Database Module
Handles SQLite database operations for TagIt Pro
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict


class TagItDatabase:
    """SQLite database manager for TagIt Pro"""
    
    def __init__(self, db_path='tagit_pro.db'):
        """
        Initialize database connection.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            
            # Create tags table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_number TEXT UNIQUE NOT NULL,
                    hidden_serial TEXT NOT NULL,
                    object_code TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    qr_color TEXT NOT NULL,
                    qr_file_path TEXT,
                    status TEXT DEFAULT 'AVAILABLE',
                    owner_name TEXT,
                    owner_email TEXT,
                    owner_phone TEXT,
                    item_name TEXT,
                    imei TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sold_at TIMESTAMP,
                    activated_at TIMESTAMP
                )
            ''')
            
            # Create index for faster searches
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tag_number ON tags(tag_number)
            ''')
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_status ON tags(status)
            ''')
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_category ON tags(category)
            ''')
            
            self.conn.commit()
            print(f"✓ Database initialized: {self.db_path}")
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            raise
    
    def add_tag(self, tag_number, hidden_serial, object_code, category, price, qr_color, qr_file_path=None):
        """
        Add a new tag to the database.
        
        Args:
            tag_number (str): The tag number (e.g., "NE-1A1Z-ID")
            hidden_serial (str): The hidden serial (e.g., "HSN-29")
            object_code (str): Object code (e.g., "ID")
            category (str): Category (non_electronic, standard_electronic, premium_electronic)
            price (int): Price in Naira
            qr_color (str): QR code color hex
            qr_file_path (str): Path to QR code PNG file
        
        Returns:
            int: ID of inserted tag, or None if failed
        """
        try:
            self.cursor.execute('''
                INSERT INTO tags 
                (tag_number, hidden_serial, object_code, category, price, qr_color, qr_file_path, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'AVAILABLE')
            ''', (tag_number, hidden_serial, object_code, category, price, qr_color, qr_file_path))
            
            self.conn.commit()
            return self.cursor.lastrowid
        
        except sqlite3.IntegrityError:
            print(f"✗ Tag {tag_number} already exists in database")
            return None
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return None
    
    def assign_to_student(self, tag_number, owner_name, owner_email, owner_phone, item_name, imei=None):
        """
        Assign a tag to a student.
        
        Args:
            tag_number (str): The tag number
            owner_name (str): Student's name
            owner_email (str): Student's email
            owner_phone (str): Student's phone
            item_name (str): Name of the item
            imei (str): IMEI number (for electronics)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute('''
                UPDATE tags SET 
                owner_name = ?, owner_email = ?, owner_phone = ?, 
                item_name = ?, imei = ?, status = 'ACTIVE', 
                activated_at = CURRENT_TIMESTAMP, sold_at = CURRENT_TIMESTAMP
                WHERE tag_number = ? AND status IN ('AVAILABLE', 'SOLD')
            ''', (owner_name, owner_email, owner_phone, item_name, imei, tag_number))
            
            self.conn.commit()
            return self.cursor.rowcount > 0
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return False
    
    def verify_sticker(self, tag_number, hidden_serial):
        """
        Verify sticker authenticity.
        
        Args:
            tag_number (str): The visible tag number
            hidden_serial (str): The provided hidden serial
        
        Returns:
            dict: Tag info if verified, None if not found or incorrect
        """
        try:
            self.cursor.execute('''
                SELECT * FROM tags WHERE tag_number = ? AND hidden_serial = ?
            ''', (tag_number, hidden_serial))
            
            result = self.cursor.fetchone()
            return dict(result) if result else None
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return None
    
    def search_by_tag(self, tag_number):
        """
        Search for a tag by tag number.
        
        Args:
            tag_number (str): The tag number to search
        
        Returns:
            dict: Tag info if found, None otherwise
        """
        try:
            self.cursor.execute('SELECT * FROM tags WHERE tag_number = ?', (tag_number,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return None
    
    def list_available_stickers(self, category=None):
        """
        List available stickers.
        
        Args:
            category (str): Filter by category (optional)
        
        Returns:
            list: List of available tags
        """
        try:
            if category:
                self.cursor.execute('''
                    SELECT * FROM tags WHERE status = 'AVAILABLE' AND category = ?
                    ORDER BY created_at DESC
                ''', (category,))
            else:
                self.cursor.execute('''
                    SELECT * FROM tags WHERE status = 'AVAILABLE'
                    ORDER BY created_at DESC
                ''')
            
            return [dict(row) for row in self.cursor.fetchall()]
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return []
    
    def get_sales_report(self):
        """
        Get sales report with statistics.
        
        Returns:
            dict: Sales statistics
        """
        try:
            self.cursor.execute('''
                SELECT 
                    category,
                    COUNT(*) as total_tags,
                    SUM(CASE WHEN status = 'SOLD' THEN 1 ELSE 0 END) as sold,
                    SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) as available,
                    SUM(CASE WHEN status = 'LOST' THEN 1 ELSE 0 END) as lost,
                    SUM(CASE WHEN status IN ('SOLD', 'ACTIVE') THEN price ELSE 0 END) as revenue
                FROM tags
                GROUP BY category
            ''')
            
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return []
    
    def count_by_status(self, status):
        """
        Count tags by status.
        
        Args:
            status (str): Status to count (AVAILABLE, SOLD, ACTIVE, LOST)
        
        Returns:
            int: Count of tags with that status
        """
        try:
            self.cursor.execute('SELECT COUNT(*) FROM tags WHERE status = ?', (status,))
            return self.cursor.fetchone()[0]
        
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    # Test database operations
    db = TagItDatabase('test_tagit.db')
    
    print("\nTesting database operations:")
    print("=" * 50)
    
    # Add a test tag
    tag_id = db.add_tag("NE-1A1Z-ID", "HSN-29", "ID", "non_electronic", 200, "#000000")
    print(f"Added tag with ID: {tag_id}")
    
    # Search for tag
    tag = db.search_by_tag("NE-1A1Z-ID")
    if tag:
        print(f"Found tag: {tag['tag_number']} - {tag['hidden_serial']}")
    
    # List available
    available = db.list_available_stickers()
    print(f"Available stickers: {len(available)}")
    
    db.close()
