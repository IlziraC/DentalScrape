#Visits pages with listings, then each individual listing link to pick up data. 
#Removes any duplicate links prior to visiting listing pages.

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import datetime
import re

# CSV file path
csv_file_path = 'pps_listings.csv'

def extract_listing_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links in the HTML
        all_links = soup.find_all('a', href=True)
        
        # Extract links related to listings using a regular expression
        listing_links = [link['href'] for link in all_links if re.search(r'/listings/\d+', link['href'])]
        
        # Remove duplicate links
        unique_listing_links = list(set(listing_links))
        
        return unique_listing_links
    else:
        print(f"Failed to retrieve the webpage {url}. Status code:", response.status_code)
        return []


def extract_listing_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Selectors for the data
        location_selector = '.elementor-element-27755ae .elementor-heading-title'
        patients_selector = '.elementor-element-e7d582f .elementor-heading-title'
        operatories_selector = '.elementor-element-b7fdb3f .elementor-heading-title'
        revenue_selector = '.elementor-element-64ba2d4 .elementor-heading-title'
        reference_selector = '.elementor-element-ded7533 .elementor-heading-title'
        description_selector = '.elementor-element-3b43a65 .elementor-widget-container'

        # Extract data
        location = soup.select_one(location_selector).text.strip() if soup.select_one(location_selector) else ''
        patients = soup.select_one(patients_selector).text.strip() if soup.select_one(patients_selector) else ''
        operatories = soup.select_one(operatories_selector).text.strip() if soup.select_one(operatories_selector) else ''
        revenue = soup.select_one(revenue_selector).text.strip() if soup.select_one(revenue_selector) else ''
        reference = soup.select_one(reference_selector).text.strip() if soup.select_one(reference_selector) else ''
        description = soup.select_one(description_selector).text.strip() if soup.select_one(description_selector) else ''

        return {
            'Location': location,
            'Patients': patients,
            'Operatories': operatories,
            'Revenue': revenue,
            'Reference': reference,
            'Description': description
        }
    else:
        print(f"Failed to retrieve the webpage {url}. Status code:", response.status_code)
        return {}

def scrape_and_save_to_csv():
    # Start with the first page
    current_page = 1

    # Create or load existing CSV file
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Listing URL', 'Location', 'Patients', 'Operatories', 'Revenue', 'Reference', 'Description', 'Scraping Date'])

    while True:
        page_url = f"https://www.ppsales.com/listings/?jsf=epro-posts&pagenum={current_page}"
        page_listing_links = extract_listing_links(page_url)

        if not page_listing_links:
            # No more listings, break out of the loop
            break

        # Extract detailed information for each listing on the current page
        for listing_link in page_listing_links:
            listing_url = f"{listing_link}"
            
            # Check if the listing is already in the DataFrame
            if df['Listing URL'].str.contains(listing_url).any():
                continue

            listing_data = extract_listing_data(listing_url)

            # Add the date of scraping
            listing_data['Scraping Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Concatenate the data to the DataFrame
            df = pd.concat([df, pd.DataFrame([{'Listing URL': listing_url, **listing_data}])], ignore_index=True)

        # Move to the next page
        current_page += 1

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    scrape_and_save_to_csv()
