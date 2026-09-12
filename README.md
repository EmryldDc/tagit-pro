# TagIt Pro - QR Code Lost & Found Management System

A complete Python-based QR code generation system for campus lost-and-found management. Generate unique stickers with embedded verification codes, manage student assignments, and track lost items.

## 🎯 Features

✅ **Unique Tag Generation**
- Automatic sequential tag numbering with random characters
- Format: `PREFIX-NUMBERLETTERNUMBERLETTER-OBJECTCODE`
- Examples: `NE-1A1Z-ID`, `EL-14N14M-HP`, `EL-22V22E-PH`

✅ **Three Pricing Tiers**
- **Non-Electronic** (BLACK QR) - ₦200 (ID, ATM Card, Keys, Wallet, etc.)
- **Standard Electronic** (GREEN QR) - ₦500 (Headphones, Power Bank, Cable, etc.)
- **Premium Electronic** (BLUE QR) - ₦1,000 (Phone, Laptop, Drone, Camera, etc.)

✅ **Twin Code Verification System**
- Hidden Serial Number (HSN) calculated mathematically from visible tag
- Anti-theft verification: `HSN-XX` format
- Example: `NE-1A1Z-ID` → `HSN-29`

✅ **QR Code Generation**
- Links to: `https://tagitpro.com/verify/{tag_number}`
- Color-coded by category
- High-quality PNG output

✅ **Database Management**
- SQLite database for persistent storage
- Track tag status: AVAILABLE, SOLD, ACTIVE, LOST
- Store student assignments and item details
- IMEI tracking for electronics

✅ **Bulk Operations**
- Generate hundreds of tags at once
- Automatic QR code creation
- CSV manifest generation
- Progress tracking

✅ **Sales & Analytics**
- Revenue tracking per category
- Inventory management
- Detailed reporting

## 📋 Project Structure

```
tagit-pro/
├── main.py                 # CLI entry point
├── tag_generator.py        # Tag number generation logic
├── hidden_serial.py        # HSN calculation
├── qr_generator.py         # QR code creation
├── database.py             # SQLite database operations
├── bulk_generator.py       # Bulk generation orchestration
├── requirements.txt        # Python dependencies
├── stickers/               # Generated QR code storage
│   ├── non_electronic/     # BLACK QR codes
│   ├── standard_electronic/# GREEN QR codes
│   └── premium_electronic/ # BLUE QR codes
├── tagit_pro.db            # SQLite database
└── manifest_*.csv          # Tag manifest files
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/EmryldDc/tagit-pro.git
cd tagit-pro
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

## 📖 Usage

### Main Menu Options

```
1. Generate Bulk Stickers
   - Create multiple tags at once
   - Specify quantities per tier
   - Auto-generates QR codes and database records

2. Assign Sticker to Student
   - Link tag to student information
   - Record item details and IMEI
   - Mark as SOLD/ACTIVE status

3. Verify Sticker Authenticity
   - Check if tag + hidden serial match
   - Prevent counterfeits
   - Display full tag information

4. Search Sticker by Tag Number
   - Look up any generated tag
   - View complete history
   - See owner information

5. List Available Stickers
   - Browse unsold inventory
   - Filter by category
   - Check pricing

6. View Sales Report
   - Revenue by category
   - Inventory status
   - Sales statistics

7. Exit
```

## 🏷️ Tag Number System

### Format
`PREFIX-NUMBERLETTERNUMBERLETTER-OBJECTCODE`

### Components
- **PREFIX**: 
  - `NE` = Non-Electronic
  - `EL` = Electronic

- **NUMBER**: Ascending sequence (1, 2, 3, ...)

- **RANDOM LETTER**: Random A-Z (changes each tag)

- **MIDDLE NUMBER**: Same as ascending number

- **LETTER**: Descending sequence (Z, Y, X, W, ... cycles after 26)

- **OBJECT CODE**: 2-letter code from predefined list

### Examples
```
NE-1A1Z-ID   (Non-Electronic: Student ID Card)
NE-2B2Y-AT   (Non-Electronic: ATM Card)
NE-3C3X-KY   (Non-Electronic: Keys)
EL-14N14M-HP (Electronic: Headphones)
EL-22V22E-PH (Premium: Phone)
EL-30F30U-LP (Premium: Laptop)
```

## 🔐 Hidden Serial Number (HSN) System

### Calculation Method
1. Extract core from tag: `PREFIX-[CORE]-OBJECTCODE`
2. Convert each character:
   - Digits: Use numeric value
   - Letters: Use alphabet position (A=1, Z=26)
3. Sum all values
4. Format as: `HSN-{SUM}`

### Examples
```
NE-1A1Z-ID
Core: 1A1Z
1 + 1(A) + 1 + 26(Z) = 29
Result: HSN-29

EL-14N14M-HP
Core: 14N14M
1 + 4 + 14(N) + 1 + 4 + 13(M) = 37
Result: HSN-37

EL-22V22E-PH
Core: 22V22E
2 + 2 + 22(V) + 2 + 2 + 5(E) = 35
Result: HSN-35
```

## 📊 Object Codes

### Non-Electronic (₦200 - BLACK)
```
ID - Student ID Card
AT - ATM Card
KY - Keys
WB - Water Bottle
BK - Books
WL - Wallet
UN - Umbrella
BP - Backpack
SH - Shoes
EG - Eyeglasses
FL - Food Flask
HC - Hat/Cap
JW - Jewelry
```

### Standard Electronic (₦500 - GREEN)
```
HP - Headphones
PB - Power Bank
CB - Charging Cable
SP - Speaker
CL - Calculator
ER - E-Reader
PD - Pen Drive
GB - Gaming Console
```

### Premium Electronic (₦1,000 - BLUE)
```
PH - Phone
LP - Laptop
DR - Drone
CR - Camera
SW - Smartwatch
```

## 💾 Database Schema

### Tags Table
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    tag_number TEXT UNIQUE NOT NULL,
    hidden_serial TEXT NOT NULL,
    object_code TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    qr_color TEXT NOT NULL,
    qr_file_path TEXT,
    status TEXT,                    -- AVAILABLE, SOLD, ACTIVE, LOST
    owner_name TEXT,
    owner_email TEXT,
    owner_phone TEXT,
    item_name TEXT,
    imei TEXT,
    created_at TIMESTAMP,
    sold_at TIMESTAMP,
    activated_at TIMESTAMP
)
```

## 🧪 Testing

### Run Module Tests
```bash
# Test tag generation
python tag_generator.py

# Test hidden serial calculation
python hidden_serial.py

# Test QR code generation
python qr_generator.py

# Test database operations
python database.py

# Test bulk generation
python bulk_generator.py
```

### Sample Data
The system includes test cases for the expected outputs:
- `NE-1A1Z-ID` → `HSN-29`
- `NE-2B2Y-AT` → `HSN-31`
- `NE-3C3X-KY` → `HSN-33`
- `EL-14N14M-HP` → `HSN-55`
- `EL-22V22E-PH` → `HSN-71`

## 📈 Performance

- Generate 1,000+ tags in seconds
- Efficient database indexing
- Batch QR code creation
- CSV manifest export

## 🔒 Security Features

- Twin Code verification prevents counterfeiting
- Database stores both visible and hidden codes
- Tag status tracking prevents duplicates
- Timestamp logging for auditing

## 🎓 Use Cases

1. **Campus Lost & Found**
   - Pre-register stickers
   - Sell to students
   - Track lost items

2. **Event Management**
   - Generate ID badges
   - Verify authenticity
   - Track attendance

3. **Asset Management**
   - Inventory tracking
   - Equipment checkout
   - Loss prevention

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License - feel free to use this project for any purpose

## 📧 Support

For issues, questions, or suggestions, please open a GitHub issue.

## 🙏 Acknowledgments

Built with:
- Python 3
- qrcode library
- Pillow (PIL)
- SQLite3

---

**Made with ❤️ for campus communities**
