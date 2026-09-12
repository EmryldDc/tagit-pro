# Quick Start Guide - TagIt Pro

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Generate Your First Batch
```
Menu Selection: 1
Enter number of Non-Electronic tags: 5
Enter number of Standard Electronic tags: 3
Enter number of Premium Electronic tags: 2
Confirm: yes
```

That's it! You'll get:
- ✅ 10 QR code PNG files in `stickers/` folder
- ✅ All tags registered in `tagit_pro.db`
- ✅ CSV manifest with all details

## 📝 Common Workflows

### Workflow 1: Sell a Sticker to a Student
```
1. Start application: python main.py
2. Select Menu: 2 (Assign Sticker to Student)
3. Enter tag number: NE-1A1Z-ID
4. Fill in student details
5. Confirm assignment
```

### Workflow 2: Verify a Found Sticker
```
1. Start application: python main.py
2. Select Menu: 3 (Verify Sticker Authenticity)
3. Enter tag number: NE-1A1Z-ID
4. Enter hidden serial: HSN-29
5. System returns owner info if authentic
```

### Workflow 3: Check Inventory
```
1. Start application: python main.py
2. Select Menu: 5 (List Available Stickers)
3. Choose category or view all
```

### Workflow 4: Generate Sales Report
```
1. Start application: python main.py
2. Select Menu: 6 (View Sales Report)
3. See revenue, inventory, and stats
```

## 🎯 Expected Output Examples

### After Generating Tags
```
======================================================================
BULK TAG GENERATION
======================================================================

[1/3] Generating 5 Non-Electronic Tags (BLACK - ₦200)...
  [20.0%] NE-1A1Z-ID → HSN-29 ✓
  [40.0%] NE-2B2Y-AT → HSN-31 ✓
  [60.0%] NE-3C3X-KY → HSN-33 ✓
  [80.0%] NE-4D4X-WB → HSN-35 ✓
  [100.0%] NE-5E5W-BK → HSN-37 ✓

[2/3] Generating 3 Standard Electronic Tags (GREEN - ₦500)...
  [33.3%] EL-1A1Z-HP → HSN-29 ✓
  [66.6%] EL-2B2Y-PB → HSN-31 ✓
  [100.0%] EL-3C3X-CB → HSN-33 ✓

[3/3] Generating 2 Premium Electronic Tags (BLUE - ₦1,000)...
  [50.0%] EL-1A1Z-PH → HSN-29 ✓
  [100.0%] EL-2B2Y-LP → HSN-31 ✓

======================================================================
GENERATION COMPLETE
======================================================================
✓ Total tags generated: 10
  - Non-Electronic: 5
  - Standard Electronic: 3
  - Premium Electronic: 2
✓ Manifest saved: stickers/manifest_20260912_003723.csv
```

## 📁 File Structure After First Run

```
tagit-pro/
├── main.py
├── tag_generator.py
├── hidden_serial.py
├── qr_generator.py
├── database.py
├── bulk_generator.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
│
├── tagit_pro.db                    ← Created automatically
├── stickers/                       ← Created automatically
│   ├── non_electronic/
│   │   ├── NE-1A1Z-ID.png
│   │   ├── NE-2B2Y-AT.png
│   │   └── ...
│   ├── standard_electronic/
│   │   ├── EL-1A1Z-HP.png
│   │   └── ...
│   ├── premium_electronic/
│   │   ├── EL-1A1Z-PH.png
│   │   └── ...
│   └── manifest_20260912_003723.csv
```

## 🔍 Sample Tag & HSN Calculations

### Example 1: Non-Electronic
```
Tag: NE-1A1Z-ID
Core: 1A1Z
Calculation: 1 + A(1) + 1 + Z(26) = 29
Result: HSN-29
Price: ₦200
QR Color: BLACK
```

### Example 2: Standard Electronic
```
Tag: EL-14N14M-HP
Core: 14N14M
Calculation: 1 + 4 + N(14) + 1 + 4 + M(13) = 37
Result: HSN-37
Price: ₦500
QR Color: GREEN
```

### Example 3: Premium Electronic
```
Tag: EL-22V22E-PH
Core: 22V22E
Calculation: 2 + 2 + V(22) + 2 + 2 + E(5) = 35
Result: HSN-35
Price: ₦1,000
QR Color: BLUE
```

## 🗂️ Manifest CSV Format

Each batch generates a manifest CSV with this structure:

```csv
tag_number,hidden_serial,object_code,category,price,qr_color,qr_file_path,generated_at
NE-1A1Z-ID,HSN-29,ID,non_electronic,200,BLACK,stickers/non_electronic/NE-1A1Z-ID.png,2026-09-12T00:37:23
NE-2B2Y-AT,HSN-31,AT,non_electronic,200,BLACK,stickers/non_electronic/NE-2B2Y-AT.png,2026-09-12T00:37:23
EL-1A1Z-HP,HSN-29,HP,standard_electronic,500,GREEN,stickers/standard_electronic/EL-1A1Z-HP.png,2026-09-12T00:37:23
EL-1A1Z-PH,HSN-29,PH,premium_electronic,1000,BLUE,stickers/premium_electronic/EL-1A1Z-PH.png,2026-09-12T00:37:23
```

## 📊 Database Status Check

### View Database in Python
```python
from database import TagItDatabase

db = TagItDatabase('tagit_pro.db')
stats = db.get_sales_report()

for row in stats:
    print(f"{row['category']}: {row['total_tags']} total")

db.close()
```

## ⚠️ Troubleshooting

### Issue: ModuleNotFoundError
```
Error: No module named 'qrcode'
Solution: pip install -r requirements.txt
```

### Issue: Database locked
```
Error: database is locked
Solution: Close other instances of the application
```

### Issue: Permission denied for stickers folder
```
Error: Permission denied: 'stickers'
Solution: Check folder permissions or run as administrator
```

### Issue: QR codes not generating
```
Error: PIL/Pillow not found
Solution: pip install Pillow
```

## 🎓 Learning Path

1. **Start Here**: Run `python main.py` and explore the menu
2. **Generate Tags**: Start with 5 of each tier
3. **View Files**: Check `stickers/` folder to see QR codes
4. **Check Database**: Use menu option 4 to search tags
5. **Assign to Student**: Use menu option 2 to practice workflow
6. **Verify**: Use menu option 3 to test verification
7. **Analytics**: Use menu option 6 to view reports

## 💡 Pro Tips

✅ **Batch Generation**: Generate tags in batches of 100+ for efficiency
✅ **Backup Database**: Regularly backup `tagit_pro.db`
✅ **Export Manifests**: Keep CSV manifests for record-keeping
✅ **Test Verification**: Always test HSN verification before selling
✅ **Color Coding**: Use QR color to identify category at a glance

## 🚀 Next Steps

- Print QR codes on stickers (use manifest CSV for batch printing)
- Create student portal for registration
- Integrate with campus email system
- Add photo upload for lost items
- Create mobile app for verification

---

**Questions?** Check the full README.md for detailed documentation.
