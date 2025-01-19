from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Prompt user for the input CSV file path
# input_csv = input("Enter the path to the input CSV file containing URLs: ").strip()
input_csv = input("Enter the path to the input CSV file containing URLs: ")  # CSV file containing URLs

# Validate the input file
try:
    urls_df = pd.read_csv(input_csv)
    if "URL" not in urls_df.columns:
        raise ValueError("Input CSV must contain a column named 'URL'.")
    print(f"Successfully loaded input CSV: {input_csv}")
except Exception as e:
    print(f"Error loading input CSV: {e}")
    exit()  # Exit the program if the file is invalid

# Generate dynamic output file name with today's date
today_date = datetime.now().strftime("%d-%m-%Y")
output_csv = f"output_products_{today_date}.csv"

# Initialize the Chrome browser
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Open Zepto and prompt for pincode input
driver.get("https://www.zeptonow.com/")
input("Press Enter here in the console after entering the pincode on the website...")
time.sleep(3)

while True:
    # Read the input CSV file containing URLs
    try:
        urls_df = pd.read_csv(input_csv)
        if "URL" not in urls_df.columns:
            raise ValueError("Input CSV must contain a column named 'URL'.")
    except Exception as e:
        print(f"Error reading input CSV or no more URLs to process: {e}")
        break  # Exit the loop if no URLs left or file not found

    # Process up to 20 URLs in the current batch
    batch = urls_df.head(20)
    if batch.empty:
        print("No more URLs to process.")
        break

    # List to store scraped product data for the batch
    products_data = []

    counter = 1

    for index, row in batch.iterrows():
        url = row["URL"]
        try:
            driver.get(url)
            time.sleep(3)  # Allow the page to load

            # Parse the page source using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract product name
            h1_tag = soup.find("h1", class_="text-xl font-semibold leading-[22px] tracking-[-0.36px] text-[#262A33]")
            product_name = h1_tag.get_text(strip=True) if h1_tag else "N/A"

            # Extract quantity and pack
            p_tag_description = soup.find("p", class_="mt-2 text-sm leading-4 text-[#757C8D]")
            net_quantity = "N/A"
            if p_tag_description:
                span_tag = p_tag_description.find("span", class_="font-bold")
                if span_tag:
                    net_quantity = span_tag.get_text(strip=True)

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

            # Extract "Pack of" value
            pack_of_value = "N/A"
            try:
                # Locate the highlights section
                highlights_div = soup.find("div", id="productHighlights")
                if highlights_div:
                    # Find the 'pack of' label within the section
                    pack_of_div = highlights_div.find_all("div", class_="flex items-start gap-3")
                    for div in pack_of_div:
                        label = div.find("h3")
                        if label and "pack of" in label.get_text(strip=True).lower():
                            pack_of_value = div.find("p").get_text(strip=True)
                            break  # Exit the loop once the value is found
            except Exception as e:
                print(f"Error extracting 'Pack of': {e}")
                
             # Extract "weight" value
            weight = "N/A"
            try:
                # Locate the highlights section
                highlights_div = soup.find("div", id="productHighlights")
                if highlights_div:
                    # Find the 'Weight' label within the section
                    pack_of_div = highlights_div.find_all("div", class_="flex items-start gap-3")
                    for div in pack_of_div:
                        label = div.find("h3")
                        if label and "weight" in label.get_text(strip=True).lower():
                            weight = div.find("p").get_text(strip=True)
                            break  # Exit the loop once the value is found
            except Exception as e:
                print(f"Error extracting 'Weight': {e}")

            # Check for out-of-stock status
            out_of_stock_div = soup.find("div", class_="mb-5 flex flex-col items-center justify-center rounded-[10px] bg-[#FDEDED] p-2")
            out_of_stock = "Yes" if out_of_stock_div and "Current selection is out of stock" in out_of_stock_div.get_text() else "No"

            # Append product details to the list
            products_data.append({
                "URL": url,
                "Product Name": product_name,
                "Net Quantity": net_quantity,
                "Selling Price": selling_price,
                "MRP": mrp,
                "Out of Stock": out_of_stock,
                "Pack of": pack_of_value,
                "Weight": weight
                
            })

            print(f"{counter}. Processed URL: {url}")  # Print with counter
            counter += 1  # Increment the counter

        except Exception as e:
            print(f"Error fetching details for URL {url}: {e}")

    # Save the current batch data to the output CSV file
    try:
        batch_df = pd.DataFrame(products_data)
        if not batch_df.empty:
            # Append to the output CSV if it exists, otherwise create it
            with open(output_csv, "a", newline='', encoding="utf-8") as f:
                batch_df.to_csv(f, index=False, header=f.tell() == 0)  # Write header only if the file is empty
            print(f"Batch of {len(batch)} URLs saved to {output_csv}")
    except Exception as e:
        print(f"Error saving batch to output CSV: {e}")

    # Remove the processed URLs from the input CSV
    try:
        urls_df = urls_df.iloc[20:]  # Drop the first 20 rows
        urls_df.to_csv(input_csv, index=False)
        print(f"Removed processed URLs from {input_csv}")
    except Exception as e:
        print(f"Error updating input CSV: {e}")

print("All batches have been processed.")
driver.quit()
