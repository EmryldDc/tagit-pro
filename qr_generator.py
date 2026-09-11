"""
QR Code Generator Module
Generates QR codes that link to verification URL
"""

import os
import qrcode
from PIL import Image
from typing import Optional


def generate_qr_code(tag_number, qr_color, output_folder):
    """
    Generate and save a QR code as PNG file.
    
    The QR code links to: https://tagitpro.com/verify/{tag_number}
    
    Args:
        tag_number (str): The tag number to encode (e.g., "EL-3C3X-PH")
        qr_color (str): Hex color code for QR code (e.g., "#000000" for black)
        output_folder (str): Path to save the QR code PNG file
    
    Returns:
        str: Full path to the saved QR code file
    
    Raises:
        ValueError: If parameters are invalid
        IOError: If file cannot be created
    """
    try:
        # Validate inputs
        if not tag_number or not isinstance(tag_number, str):
            raise ValueError("Invalid tag number")
        
        if not qr_color or not isinstance(qr_color, str):
            raise ValueError("Invalid QR color")
        
        # Remove '#' if present in color code
        color = qr_color.lstrip('#')
        
        # Validate hex color
        if not all(c in '0123456789ABCDEFabcdef' for c in color) or len(color) != 6:
            raise ValueError(f"Invalid hex color: {qr_color}")
        
        # Convert hex to RGB tuple
        rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        
        # Create verification URL
        verification_url = f"https://tagitpro.com/verify/{tag_number}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR code
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # Size of each box in pixels
            border=4,  # Border thickness in boxes
        )
        
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Create QR code image with custom color
        img = qr.make_image(
            fill_color=rgb_color,
            back_color=(255, 255, 255)  # White background
        )
        
        # Save the image
        file_path = os.path.join(output_folder, f"{tag_number}.png")
        img.save(file_path)
        
        return file_path
    
    except Exception as e:
        raise IOError(f"Error generating QR code for {tag_number}: {str(e)}")


def generate_qr_codes_batch(tags_data, base_output_folder):
    """
    Generate QR codes for multiple tags in batch.
    
    Args:
        tags_data (list): List of dicts with keys: tag_number, qr_color, category
        base_output_folder (str): Base folder path (will create subfolders per category)
    
    Returns:
        list: List of generated file paths
    
    Example:
        tags = [
            {'tag_number': 'NE-1A1Z-ID', 'qr_color': '#000000', 'category': 'non_electronic'},
            {'tag_number': 'EL-14N14M-HP', 'qr_color': '#2E7D32', 'category': 'standard_electronic'},
        ]
        paths = generate_qr_codes_batch(tags, './stickers')
    """
    generated_files = []
    category_folders = {
        'non_electronic': 'non_electronic',
        'standard_electronic': 'standard_electronic',
        'premium_electronic': 'premium_electronic'
    }
    
    for tag_info in tags_data:
        tag_number = tag_info['tag_number']
        qr_color = tag_info['qr_color']
        category = tag_info.get('category', 'non_electronic')
        
        # Create category-specific folder
        category_folder = category_folders.get(category, 'other')
        output_folder = os.path.join(base_output_folder, category_folder)
        
        try:
            file_path = generate_qr_code(tag_number, qr_color, output_folder)
            generated_files.append({
                'tag_number': tag_number,
                'file_path': file_path,
                'category': category
            })
            print(f"✓ Generated: {tag_number}")
        except Exception as e:
            print(f"✗ Failed: {tag_number} - {str(e)}")
    
    return generated_files


def verify_qr_code_exists(tag_number, output_folder):
    """
    Check if QR code file exists for a tag.
    
    Args:
        tag_number (str): The tag number
        output_folder (str): Path to check
    
    Returns:
        bool: True if file exists, False otherwise
    """
    file_path = os.path.join(output_folder, f"{tag_number}.png")
    return os.path.exists(file_path)


if __name__ == "__main__":
    # Test QR code generation
    print("QR Code Generation Test:")
    print("=" * 60)
    
    test_cases = [
        ("NE-1A1Z-ID", "#000000", "test_output/non_electronic"),
        ("EL-3C3X-PH", "#2E7D32", "test_output/standard_electronic"),
        ("EL-14N14M-HP", "#1A73E8", "test_output/premium_electronic"),
    ]
    
    for tag, color, folder in test_cases:
        try:
            path = generate_qr_code(tag, color, folder)
            print(f"✓ {tag} → {path}")
        except Exception as e:
            print(f"✗ {tag} → Error: {str(e)}")
