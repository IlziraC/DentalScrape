# Scraping Data on Dental Practice Listings

## Overview

This project involves scraping data on dental practice listings from two popular broker firms - Heaps & Doyle and PPS. The collected data is then processed and analyzed to gain insights into the dental practice market.

## Data Sources

The primary sources of data are the websites of two broker firms - Heaps & Doyle and PPS.

## Methodology

I utilized different scraping methodologies for each source:

### PPS
For PPS, I employed BeautifulSoup and Pandas in the script. The script `ppslistings.py` first visits the page(s) with listings, collects links to each individual listing, and then visits each link to extract relevant data.

### Heaps & Doyle
For Heaps & Doyle, I used httpx and selectolax to directly extract information about listings from the main page where listings are published. The script is named `heapsanddoyle.py`.

### -------------
Both scripts extract data into CSV files, while recording the date and time of the scrape. To avoid overwriting existing data, the scripts are designed to only load new listings, bypassing duplicate entries.

## Data Collection Automation

I have set up a task in my Task Scheduler to run both scripts daily, ensuring continuous collection of data over time.

## Power BI Integration

To analyze and visualize the collected data, I created a Power BI file named `Dental Practices.pbix`. In this file, I uploaded, cleaned, and sorted the data. I established custom columns such as Province, Source of Data, etc. Additionally, calculated measures were defined, and a dashboard with visuals was built to highlight key takeaways from the dental practice listings:

![](https://github.com/IlziraC/DentalScrape/blob/edb77f239e6b74c9f8192f3aa15bfe25a82a9bdd/Power%20BI%20Dashboard%20-%20Web%20Scraping.png)

## Repository Structure

- `ppslistings.py`: Python script for scraping data from PPS website.
- `heapsanddoyle.py`: Python script for scraping data from Heaps & Doyle website.
- `Dental Practices.pbix`: Power BI file containing the data model and dashboard.

## Usage

1. Run `ppslistings.py` to scrape data from the PPS website.
2. Run `heapsanddoyle.py` to scrape data from the Heaps & Doyle website.
3. Use `Dental Practices.pbix` for data analysis and visualization in Power BI.
4. If you want to keep collecting data, set up tasks in your Task Scheduler to automate this activity.

