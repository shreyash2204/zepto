# Zepto Product Scraper

Automate product data extraction from **Zepto's website** using this Python script. It scrapes product details like Product Name, Quantity, Pack Size, Selling Price, and MRP based on SKUs provided in a CSV file.

---

## 📦 Features

- 🔍 Automated extraction of product details.
- 📄 Saves results in a structured CSV format.
- 🖥️ Utilizes Selenium and BeautifulSoup for dynamic scraping.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/zepto-product-scraper.git
cd zepto-product-scraper
```

### 2. Install Required Libraries
```bash
pip install -r requirements.txt
```

**Required Libraries:**
- `selenium`
- `webdriver-manager`
- `beautifulsoup4`
- `pandas`

### 3. Set Up the Input CSV
Prepare your input CSV (`inputfile/Sample_SKUs.csv`) with the following format:

```csv
SKU,NAME
6d9206b1-2963-4dc3-b8c8-a2afdb61311f,Vs Mani & Co. Filter Coffee Powder - 100 g
6d98d319-2b82-47ae-80a9-86405c29625e,Shadow Securitronics Tom Cat No Entry Rat Repellent Car Spray Highly Effective Easy To Spray - 200 ml
6d9d6337-d86f-4e73-8d4f-5cd271818985,Satvik Diya Pack Of 4 - 1 piece
6d9e21bd-7d2d-478b-be91-c0441b4d15ed,Chrome Black Binder Clip - 1 Piece (19 mm)
```

### 4. Run the Script
```bash
python zepto_scraper.py
```

**Note:** The script will open a browser window. Enter your **pincode** on Zepto's homepage and press **Enter** in the console to continue.

---

## 📊 Output
The script generates an output CSV (`outputfile/output_products.csv`) with the following columns:

- `SKU`
- `Product Name`
- `Quantity`
- `Pack`
- `Selling Price`
- `MRP`

### 📂 Example Output:
```csv
SKU,Product Name,Quantity,Pack,Selling Price,MRP
6d9206b1-2963-4dc3-b8c8-a2afdb61311f,Vs Mani & Co. Filter Coffee Powder - 100 g,100 g,1,₹150,₹180
6d98d319-2b82-47ae-80a9-86405c29625e,Shadow Securitronics Tom Cat No Entry Rat Repellent Car Spray - 200 ml,200 ml,1,₹499,₹599
```

---

## ⚠️ Important Notes
- Ensure **Chrome** is installed.
- Update ChromeDriver using `webdriver-manager` if needed.
- Scraping is for educational purposes. Respect website terms of service.

---

## 🤝 Contributing
Feel free to submit issues or pull requests to improve this script!

---

## 📞 Contact
For queries, contact [Your Name](mailto:your.email@example.com).

---

**Happy Scraping!** 🚀

