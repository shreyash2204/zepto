import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage to crawl
url = "https://www.zeptonow.com/pn/lays-american-cream-onion-potato-chips/pvid/c93f510e-0ae9-4912-b4df-41603bef01da"

# Set up headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the `h1` tag with the specified class
    h1_tag = soup.find("h1", class_="text-xl font-semibold leading-[22px] tracking-[-0.36px] text-[#262A33]")
    if h1_tag:
        print("H1 Tag Text:", h1_tag.get_text(strip=True))
    else:
        print("H1 tag with the specified class was not found.")

    # Find the description `p` tag
    p_tag_description = soup.find("p", class_="mt-2 text-sm leading-4 text-[#757C8D]")
    if p_tag_description:
        # Extract raw text and clean it
        span_tag = p_tag_description.find("span", class_="font-bold")
        if span_tag:
            quantity_text = span_tag.get_text(strip=True)
            
            # Check for a multiplier (e.g., "X 3") using regex
            match = re.search(r'X\s*(\d+)', quantity_text)
            if match:
                pack_count = match.group(1)  # Extract the pack count (e.g., '3')
                # Remove "X 3" from the quantity
                quantity_text = re.sub(r'\s*X\s*\d+', '', quantity_text)
                print("Quantity:", quantity_text.strip())  # Cleaned quantity (e.g., '150gms')
                print("Pack:", pack_count)  # Pack count (e.g., '3')
            else:
                print("Quantity:", quantity_text.strip())  # If no multiplier, print as is
                print("Pack: 1")  # If no pack count, default to 1
        else:
            print("Span with the specified class was not found inside the P tag.")
    else:
        print("P tag with the specified class was not found.")

    # Find the selling price
    p_tag_price = soup.find("p", class_="flex items-center justify-center gap-2")
    if p_tag_price:
        print("Selling Price:", p_tag_price.get_text(strip=True))
    else:
        print("P tag for the selling price with the specified class was not found.")

    # Find the MRP
    p_tag_mrp = soup.find("p", class_="text-[14px] font-[450] leading-[21.6px] tracking-[-0.24px] text-[#757C8D]")
    if p_tag_mrp:
        # Find the `span` with the `line-through font-bold` class inside this `p` tag
        span_mrp = p_tag_mrp.find("span", class_="line-through font-bold")
        if span_mrp:
            print("MRP:", span_mrp.get_text(strip=True))
        else:
            print("Span with the specified MRP class was not found inside the P tag.")
    else:
        print("P tag for the MRP with the specified class was not found.")

except requests.exceptions.RequestException as e:
    print("Error fetching the URL:", e)
