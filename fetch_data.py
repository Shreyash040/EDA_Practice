#!/usr/bin/env python3
"""
Script to fetch data from transilience.ai website
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys

def fetch_website_data(url):
    """Fetch and parse data from the website"""
    print(f"Fetching data from {url}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for CSV links
        csv_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.csv') or 'csv' in href.lower():
                csv_links.append(href)
        
        if csv_links:
            print(f"\nFound {len(csv_links)} CSV link(s):")
            for i, link in enumerate(csv_links, 1):
                print(f"  {i}. {link}")
            return csv_links
        else:
            print("\n⚠ No CSV files found on the page")
            
            # Try to find data tables
            tables = soup.find_all('table')
            if tables:
                print(f"\nFound {len(tables)} HTML table(s) on the page")
                print("Attempting to extract first table...")
                
                df = pd.read_html(str(tables[0]))[0]
                output_file = 'extracted_data.csv'
                df.to_csv(output_file, index=False)
                print(f"✓ Extracted table saved as '{output_file}'")
                return [output_file]
            else:
                print("⚠ No tables found on the page either")
                
                # Save page content for inspection
                with open('page_content.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print("✓ Page content saved as 'page_content.html' for inspection")
                
        return []
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return []


def download_csv(url, output_file='downloaded_data.csv'):
    """Download CSV file from URL"""
    try:
        print(f"\nDownloading CSV from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ CSV downloaded as '{output_file}'")
        return output_file
    except Exception as e:
        print(f"✗ Error downloading CSV: {e}")
        return None


def main():
    """Main function"""
    url = 'https://www.transilience.ai/'
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    print("="*80)
    print("TRANSILIENCE.AI DATA FETCHER")
    print("="*80 + "\n")
    
    csv_links = fetch_website_data(url)
    
    if csv_links:
        # If CSV links found, download the first one
        if csv_links[0].startswith('http'):
            download_csv(csv_links[0])
        else:
            print(f"\nRelative URL found: {csv_links[0]}")
            print("Please provide the full URL to download")
    else:
        print("\n" + "="*80)
        print("ALTERNATIVE: Using Sample Data")
        print("="*80)
        print("\nSince no CSV data was found on the website,")
        print("you can use the SampleSuperstore.csv file in the current directory")
        print("or provide your own CSV file for analysis.")


if __name__ == "__main__":
    main()
