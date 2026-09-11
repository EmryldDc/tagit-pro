"""
Tag Number Generator Module
Generates unique tag numbers with format: PREFIX-NUMBERLETTERNUMBERLETTER-OBJECTCODE
"""

import random
from typing import Tuple

# Object Code Definitions with Categories and Pricing
OBJECT_CODES = {
    # Non-Electronic (NE) - Price ₦200 - BLACK
    'non_electronic': {
        'codes': ['ID', 'AT', 'KY', 'WB', 'BK', 'WL', 'UN', 'BP', 'SH', 'EG', 'FL', 'HC', 'JW'],
        'price': 200,
        'color': '#000000',  # Black
        'color_name': 'BLACK'
    },
    # Standard Electronic (EL) - Price ₦500 - GREEN
    'standard_electronic': {
        'codes': ['HP', 'PB', 'CB', 'SP', 'CL', 'ER', 'PD', 'GB'],
        'price': 500,
        'color': '#2E7D32',  # Green
        'color_name': 'GREEN'
    },
    # Premium Electronic (EL) - Price ₦1,000 - BLUE
    'premium_electronic': {
        'codes': ['PH', 'LP', 'DR', 'CR', 'SW'],
        'price': 1000,
        'color': '#1A73E8',  # Blue
        'color_name': 'BLUE'
    }
}

# Prefix mapping
CATEGORY_PREFIX = {
    'non_electronic': 'NE',
    'standard_electronic': 'EL',
    'premium_electronic': 'EL'
}

# State tracking for sequence generation
class TagSequence:
    """Tracks the sequence state for tag generation"""
    
    def __init__(self):
        self.number_counter = 0  # Ascending: 1, 2, 3, ...
        self.letter_counter = 25  # Descending: Z(25), Y(24), X(23), ... cycles after 26
    
    def get_next_number(self):
        """Get next ascending number and increment counter"""
        self.number_counter += 1
        return self.number_counter
    
    def get_next_letter(self):
        """Get next descending letter and cycle counter"""
        letter = chr(ord('A') + self.letter_counter)
        self.letter_counter = (self.letter_counter - 1) % 26
        return letter
    
    def reset(self):
        """Reset counters"""
        self.number_counter = 0
        self.letter_counter = 25

# Global sequence tracker
_tag_sequence = TagSequence()


def get_category_for_object_code(object_code):
    """
    Determine which category an object code belongs to.
    
    Args:
        object_code (str): Two-letter object code
    
    Returns:
        str: Category name or None if not found
    """
    for category, details in OBJECT_CODES.items():
        if object_code in details['codes']:
            return category
    return None


def validate_object_code(object_code):
    """
    Validate if object code exists.
    
    Args:
        object_code (str): Two-letter object code
    
    Returns:
        bool: True if valid, False otherwise
    """
    return get_category_for_object_code(object_code) is not None


def get_object_code_details(object_code):
    """
    Get details for an object code (price, color, category).
    
    Args:
        object_code (str): Two-letter object code
    
    Returns:
        dict: Contains category, price, color, color_name
    """
    category = get_category_for_object_code(object_code)
    if not category:
        raise ValueError(f"Invalid object code: {object_code}")
    
    details = OBJECT_CODES[category].copy()
    details['category'] = category
    return details


def generate_tag_number(object_code):
    """
    Generate a unique tag number.
    
    Format: PREFIX-NUMBERLETTERNUMBERLETTER-OBJECTCODE
    Example: NE-1A1Z-ID
    
    Args:
        object_code (str): Two-letter object code (e.g., 'ID', 'HP', 'PH')
    
    Returns:
        str: Generated tag number
    
    Raises:
        ValueError: If object code is invalid
    """
    if not validate_object_code(object_code):
        raise ValueError(f"Invalid object code: {object_code}")
    
    # Get category and prefix
    category = get_category_for_object_code(object_code)
    prefix = CATEGORY_PREFIX[category]
    
    # Get sequential components
    number = _tag_sequence.get_next_number()
    random_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    middle_number = number  # Same as the ascending number
    descending_letter = _tag_sequence.get_next_letter()
    
    # Construct tag number
    tag_number = f"{prefix}-{number}{random_letter}{middle_number}{descending_letter}-{object_code}"
    
    return tag_number


def generate_tags_for_category(category, count):
    """
    Generate multiple tags for a specific category.
    
    Args:
        category (str): Category name (non_electronic, standard_electronic, premium_electronic)
        count (int): Number of tags to generate
    
    Returns:
        list: List of generated tag numbers
    """
    if category not in OBJECT_CODES:
        raise ValueError(f"Invalid category: {category}")
    
    available_codes = OBJECT_CODES[category]['codes']
    tags = []
    
    for i in range(count):
        object_code = available_codes[i % len(available_codes)]
        tag = generate_tag_number(object_code)
        tags.append(tag)
    
    return tags


def reset_sequence():
    """Reset the tag sequence counter (for testing or new batch)"""
    _tag_sequence.reset()


def get_all_object_codes():
    """Get all available object codes organized by category"""
    return OBJECT_CODES


if __name__ == "__main__":
    # Test tag generation
    print("Tag Number Generation Tests:")
    print("=" * 60)
    
    # Test Non-Electronic
    print("\nNon-Electronic Tags (NE - BLACK - ₦200):")
    print("-" * 60)
    reset_sequence()
    ne_tags = generate_tags_for_category('non_electronic', 5)
    for tag in ne_tags:
        details = get_object_code_details(tag.split('-')[2])
        print(f"{tag} | Price: ₦{details['price']} | Color: {details['color_name']}")
    
    # Test Standard Electronic
    print("\nStandard Electronic Tags (EL - GREEN - ₦500):")
    print("-" * 60)
    reset_sequence()
    se_tags = generate_tags_for_category('standard_electronic', 5)
    for tag in se_tags:
        details = get_object_code_details(tag.split('-')[2])
        print(f"{tag} | Price: ₦{details['price']} | Color: {details['color_name']}")
    
    # Test Premium Electronic
    print("\nPremium Electronic Tags (EL - BLUE - ₦1,000):")
    print("-" * 60)
    reset_sequence()
    pe_tags = generate_tags_for_category('premium_electronic', 5)
    for tag in pe_tags:
        details = get_object_code_details(tag.split('-')[2])
        print(f"{tag} | Price: ₦{details['price']} | Color: {details['color_name']}")
