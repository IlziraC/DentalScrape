#Extracts listings from H&D website, removes duplicates based on listing_id

import httpx
from selectolax.parser import HTMLParser
import csv
import time
import os
from datetime import datetime

def clean_data(value):
    chars_to_remove = ["$", '"']
    for char in chars_to_remove:
        if char in value:
            value = value.replace(char, "")
    return value.strip()

def get_html(baseurl, page):
    headers = {
        "User-Agent": "ENTER YOUR USER AGENT"
    }
    resp = httpx.get(baseurl + str(page), headers=headers, follow_redirects=True)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        return False
    html = HTMLParser(resp.text)
    return html

def extract_text(html, sel):
    try:
        return clean_data(html.css_first(sel).text())
    except AttributeError:
        return None

def load_existing_data(csv_filename):
    existing_data = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_data.add(row["listing_id"])
    return existing_data

def save_data(csv_filename, data):
    data["date_scraped"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["location", "price", "status", "listing_id", "practice_type", "gross", "practice_description", "date_scraped"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:  # If the file is empty, write the header
            writer.writeheader()
        writer.writerow(data)

def main():
    baseurl = "https://listings.heapsanddoyle.com/?submit=1&city&status&practice&revenue#results"
    csv_filename = "hd_listings.csv"

    existing_data = load_existing_data(csv_filename)

    for x in range(1, 2):
        html = get_html(baseurl, x)
        if html is False:
            break
        listings = html.css("div.list")
        for listing in listings:
            item = {
                "location": extract_text(listing, "h3"),
                "price": extract_text(listing, ".content-left-side p:nth-child(1) span:nth-child(2)"),
                "status": extract_text(listing, ".content-left-side p:nth-child(2) span:nth-child(2)"),
                "listing_id": extract_text(listing, ".content-right-side p:nth-child(1) span:nth-child(2)"),
                "practice_type": extract_text(listing, ".content-right-side p:nth-child(2) span:nth-child(2)"),
                "gross": extract_text(listing, ".content-stuts p:nth-child(3) span:nth-child(2)"),
                "practice_description": extract_text(listing, ".content-list p")
            }

            if item["listing_id"] not in existing_data:
                save_data(csv_filename, item)
                existing_data.add(item["listing_id"])

            # Print the item details
            print(item)

        time.sleep(1)

    print(f"Results written to {csv_filename}")

if __name__ == "__main__":
    main()
