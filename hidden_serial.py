"""
Hidden Serial Number Calculator Module
Calculates the HSN (Twin Code System) for tag verification
"""

def calculate_hidden_serial(tag_number):
    """
    Calculate hidden serial number from visible tag number.
    
    Format: Extract core from tag number (between prefix and object code)
    Convert letters to positions (A=1, B=2, ... Z=26)
    Sum all numbers and letters
    
    Args:
        tag_number (str): The visible tag number (e.g., "EL-3C3X-PH")
    
    Returns:
        str: Hidden serial in format "HSN-XX" (e.g., "HSN-33")
    
    Example:
        calculate_hidden_serial("EL-3C3X-PH")
        # Extract core: 3C3X
        # 3 + C(3) + 3 + X(24) = 3 + 3 + 3 + 24 = 33
        # Returns: "HSN-33"
    """
    try:
        # Remove prefix and object code to get the core
        # Format: PREFIX-CORE-OBJECTCODE
        parts = tag_number.split('-')
        
        if len(parts) != 3:
            raise ValueError(f"Invalid tag format: {tag_number}")
        
        core = parts[1]  # e.g., "3C3X"
        
        # Calculate sum of all characters
        total = 0
        
        for char in core:
            if char.isdigit():
                # If it's a digit, add its numeric value
                total += int(char)
            elif char.isalpha():
                # If it's a letter, convert to position (A=1, Z=26)
                position = ord(char.upper()) - ord('A') + 1
                total += position
            else:
                raise ValueError(f"Invalid character in core: {char}")
        
        return f"HSN-{total}"
    
    except Exception as e:
        raise ValueError(f"Error calculating hidden serial for {tag_number}: {str(e)}")


def verify_sticker(tag_number, provided_serial):
    """
    Verify if the provided hidden serial matches the calculated one.
    
    Args:
        tag_number (str): The visible tag number
        provided_serial (str): The provided serial number to verify
    
    Returns:
        bool: True if they match, False otherwise
    """
    calculated = calculate_hidden_serial(tag_number)
    return calculated == provided_serial


if __name__ == "__main__":
    # Test examples
    test_cases = [
        "NE-1A1Z-ID",      # Should be HSN-29
        "NE-2B2Y-AT",      # Should be HSN-31
        "NE-3C3X-KY",      # Should be HSN-33
        "EL-14N14M-HP",    # Should be HSN-55
        "EL-22V22E-PH",    # Should be HSN-71
    ]
    
    print("Hidden Serial Number Calculation Tests:")
    print("=" * 50)
    for tag in test_cases:
        hsn = calculate_hidden_serial(tag)
        print(f"{tag} → {hsn}")
