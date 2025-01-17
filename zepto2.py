import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Input and output file paths
input_csv = "inputfile/Sarthak Rough Book - Sheet397.csv"  # CSV file containing SKUs
output_csv = "outputfile/output_products.csv"

# Base URL with SKU placeholder
base_url = "https://www.zeptonow.com/pn/lays-american-cream-onion-potato-chips/pvid/{sku}"

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Read the input CSV file containing SKUs
try:
    skus_df = pd.read_csv(input_csv)
    if "SKU" not in skus_df.columns:
        raise ValueError("Input CSV must contain a column named 'SKU'.")
except Exception as e:
    print(f"Error reading input CSV: {e}")
    exit()

# List to store scraped product data
products_data = []

# Crawl each SKU
for index, row in skus_df.iterrows():
    sku = row["SKU"]
    url = base_url.format(sku=sku)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract product name
        h1_tag = soup.find("h1", class_="text-xl font-semibold leading-[22px] tracking-[-0.36px] text-[#262A33]")
        product_name = h1_tag.get_text(strip=True) if h1_tag else "N/A"

        # Extract quantity and pack
        p_tag_description = soup.find("p", class_="mt-2 text-sm leading-4 text-[#757C8D]")
        quantity, pack = "N/A", "1"
        if p_tag_description:
            span_tag = p_tag_description.find("span", class_="font-bold")
            if span_tag:
                quantity_text = span_tag.get_text(strip=True)
                match = re.search(r'X\s*(\d+)', quantity_text)
                if match:
                    pack = match.group(1)
                    quantity = re.sub(r'\s*X\s*\d+', '', quantity_text).strip()
                else:
                    quantity = quantity_text.strip()

        # Extract selling price
        p_tag_price = soup.find("p", class_="flex items-center justify-center gap-2")
        selling_price = p_tag_price.get_text(strip=True) if p_tag_price else "N/A"

        # Extract MRP
        p_tag_mrp = soup.find("p", class_="text-[14px] font-[450] leading-[21.6px] tracking-[-0.24px] text-[#757C8D]")
        mrp = "N/A"
        if p_tag_mrp:
            span_mrp = p_tag_mrp.find("span", class_="line-through font-bold")
            if span_mrp:
                mrp = span_mrp.get_text(strip=True)

        # Append product details to the list
        products_data.append({
            "SKU": sku,
            "Product Name": product_name,
            "Quantity": quantity,
            "Pack": pack,
            "Selling Price": selling_price,
            "MRP": mrp
        })
    except Exception as e:
        print(f"Error fetching details for SKU {sku}: {e}")

# Save the data to an output CSV file
try:
    products_df = pd.DataFrame(products_data)
    products_df.to_csv(output_csv, index=False)
    print(f"Product data has been saved to {output_csv}")
except Exception as e:
    print(f"Error saving output CSV: {e}")
