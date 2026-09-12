# How to Run TagIt Pro - Complete Instructions

## 🚀 Step-by-Step Setup

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

**Check your Python version:**
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

---

### Step 2: Clone or Download the Repository

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/EmryldDc/tagit-pro.git
cd tagit-pro
```

**Option B: Download as ZIP**
1. Go to https://github.com/EmryldDc/tagit-pro
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in that folder

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `qrcode[pil]==7.4.2` - QR code generation
- `Pillow==10.0.0` - Image processing

**If you encounter errors:**
```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install dependencies
pip install -r requirements.txt
```

---

### Step 4: Run the Application

```bash
python main.py
```

You should see this menu:

```
======================================================================
  TagIt Pro - Lost & Found Management System
======================================================================

  1. Generate Bulk Stickers
  2. Assign Sticker to Student
  3. Verify Sticker Authenticity
  4. Search Sticker by Tag Number
  5. List Available Stickers
  6. View Sales Report
  7. Exit

Enter your choice (1-7): 
```

---

## 📋 Your First Run - Complete Walkthrough

### Generate Your First Tags

```
Step 1: Select menu option 1
Enter your choice (1-7): 1

Step 2: Enter quantities
Enter number of Non-Electronic tags (₦200, BLACK): 3
Enter number of Standard Electronic tags (₦500, GREEN): 2
Enter number of Premium Electronic tags (₦1,000, BLUE): 1

Step 3: Confirm
Generate 6 total tags? (yes/no): yes

Step 4: Watch the generation
✓ Total tags generated: 6
  - Non-Electronic: 3
  - Standard Electronic: 2
  - Premium Electronic: 1
✓ Manifest saved: stickers/manifest_20260912_003723.csv

Step 5: Check the output
- QR codes saved in: stickers/ folder
- Database updated: tagit_pro.db
- Manifest created: CSV file with all details
```

---

## 🎯 Common Commands

### Open Terminal/Command Prompt

**Windows:**
1. Press `Windows Key + R`
2. Type `cmd`
3. Press Enter

**Mac:**
1. Press `Cmd + Space`
2. Type `terminal`
3. Press Enter

**Linux:**
1. Right-click desktop
2. Select "Open Terminal Here"

---

### Navigate to Project Folder

```bash
# Example: If tagit-pro is on Desktop
cd Desktop/tagit-pro

# Or the full path
cd /Users/YourName/Desktop/tagit-pro
```

---

### Run the App

```bash
python main.py
```

---

## 🔧 Troubleshooting

### Problem: "python: command not found"
**Solution:** Python may not be in your PATH
```bash
# Try with python3
python3 main.py

# Or use full path
/usr/bin/python3 main.py
```

---

### Problem: "ModuleNotFoundError: No module named 'qrcode'"
**Solution:** Dependencies not installed
```bash
# Reinstall dependencies
pip install -r requirements.txt

# If still fails, try
pip install qrcode[pil] Pillow
```

---

### Problem: "Permission denied"
**Solution:** Run with appropriate permissions
```bash
# On Mac/Linux, try
sudo python main.py

# Or check folder permissions
chmod 755 tagit-pro
```

---

### Problem: "Database is locked"
**Solution:** Close other instances of the app and delete lock files
```bash
# Remove lock files
rm *.db-journal
rm *.db-wal

# Then run again
python main.py
```

---

## 📁 What Gets Created

After running for the first time, these folders/files appear:

```
tagit-pro/
├── tagit_pro.db              ← Database (auto-created)
└── stickers/                 ← QR codes folder (auto-created)
    ├── non_electronic/       ← BLACK QR codes
    │   ├── NE-1A1Z-ID.png
    │   ├── NE-2B2Y-AT.png
    │   └── NE-3C3X-KY.png
    ├── standard_electronic/  ← GREEN QR codes
    │   ├── EL-1A1Z-HP.png
    │   └── EL-2B2Y-PB.png
    ├── premium_electronic/   ← BLUE QR codes
    │   └── EL-1A1Z-PH.png
    └── manifest_20260912_003723.csv  ← Tag list
```

---

## ✅ Verify Installation

Run this test to confirm everything works:

```bash
python tag_generator.py
```

You should see test output showing sample tags and HSN calculations.

---

## 🎬 Quick Start Sequence

1. **Open Terminal**
   ```bash
   cd Desktop/tagit-pro
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run App**
   ```bash
   python main.py
   ```

4. **Select Option 1** (Generate Bulk Stickers)

5. **Enter quantities** (e.g., 5, 3, 2)

6. **Confirm** (type `yes`)

7. **Done!** Check `stickers/` folder for QR codes

---

## 💡 Pro Tips

✅ Always run from the project root directory
✅ Keep terminal open while using the app
✅ Use Option 6 to check your inventory anytime
✅ Export manifests for record-keeping
✅ Check `stickers/` folder to see generated QR codes

---

## 🆘 Need More Help?

1. Check **README.md** for detailed documentation
2. Check **QUICKSTART.md** for common workflows
3. Read error messages carefully (they indicate what went wrong)
4. Try running individual modules for testing:
   ```bash
   python tag_generator.py
   python hidden_serial.py
   python qr_generator.py
   ```

---

## 🎓 Menu Options Explained

```
1. Generate Bulk Stickers
   → Creates multiple tags with QR codes
   → Stores in database
   → Creates manifest CSV

2. Assign Sticker to Student
   → Link tag to student info
   → Record item details
   → Mark as SOLD/ACTIVE

3. Verify Sticker Authenticity
   → Check if tag + HSN match
   → Display owner info
   → Prevent counterfeits

4. Search Sticker by Tag Number
   → Look up any tag
   → View full details
   → See history

5. List Available Stickers
   → Browse unsold inventory
   → Filter by category
   → Check pricing

6. View Sales Report
   → Revenue statistics
   → Inventory status
   → Category breakdown

7. Exit
   → Safely close the application
```

---

**You're all set! Start generating your first batch of QR codes now!** 🎉
