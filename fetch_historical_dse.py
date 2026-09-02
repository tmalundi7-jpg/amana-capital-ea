import requests
from bs4 import BeautifulSoup
import os
import urllib3
import re
from scrape_dse import extract_text_from_pdf_url

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DSE_URL = "https://dse.co.tz/"
OUTPUT_DIR = "output"

def fetch_available_reports():
    """Scrapes the DSE homepage to find all available daily market reports."""
    print(f"Fetching available reports from {DSE_URL}...")
    try:
        response = requests.get(DSE_URL, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching DSE website: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    daily_reports_div = soup.find('div', id='daily-reports')
    
    if not daily_reports_div:
        print("Could not find the 'daily-reports' section on the page.")
        return []

    reports = []
    
    # Check for the card structure first
    cards = daily_reports_div.find_all('div', class_='card')
    if cards:
        for card in cards:
            date_text = 'Unknown'
            p = card.find('p', class_='card-text')
            if p:
                date_text = ' '.join(p.get_text().replace('Date:', '').split())
                date_text = re.sub(r'\b(\d+)(?:st|nd|rd|th)\b', r'\1', date_text) # Clean up suffixes from numbers only (e.g. 13th -> 13)
            a = card.find('a', href=re.compile('/get/daily/report'))
            if a:
                pdf_url = DSE_URL.rstrip('/') + a['href'] if a['href'].startswith('/') else a['href']
                reports.append({"date_text": date_text.strip(), "url": pdf_url})
    else:
        # Fallback to the old table structure just in case
        for a in daily_reports_div.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            if '/get/daily/report' in href.lower():
                pdf_url = DSE_URL.rstrip('/') + href if href.startswith('/') else href
                reports.append({"date_text": text, "url": pdf_url})
                
    return reports

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    reports = fetch_available_reports()
    
    if not reports:
        print("No historical reports found.")
        return

    print("\n--- Available Historical Reports ---")
    for i, report in enumerate(reports):
        print(f"[{i+1}] {report['date_text']}")
        
    while True:
        print("\n------------------------------------")
        user_input = input("Enter the number of the report or a date (e.g. '10 August') to fetch (or type 'q' to quit): ").strip()
        
        if user_input.lower() == 'q':
            print("Exiting...")
            break
            
        selected = None
        
        # Check if user wants today's report
        if user_input.lower() == 'today':
            if reports:
                selected = reports[0]
            else:
                print("No reports available.")
                continue
        # Try treating input as a number
        elif user_input.isdigit():
            choice = int(user_input) - 1
            if 0 <= choice < len(reports):
                selected = reports[choice]
            else:
                print("Invalid selection. Number out of range.")
                continue
        else:
            # Treat input as a date string search
            matches = [r for r in reports if user_input.lower() in r['date_text'].lower()]
            if not matches:
                print(f"No reports found matching '{user_input}'. Please try again.")
                continue
            elif len(matches) > 1:
                print(f"Multiple reports match '{user_input}'. Please be more specific (e.g., add the year).")
                for m in matches:
                    print(f" - {m['date_text']}")
                continue
            else:
                selected = matches[0]
                
        if selected:
            print(f"\nFetching data for: {selected['date_text']}")
            raw_text = extract_text_from_pdf_url(selected['url'])
            
            if raw_text:
                safe_date = selected['date_text'].replace(' ', '_').replace(',', '')
                filename = f"Raw_Market_Data_{safe_date}.txt"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(raw_text)
                    
                print(f"SUCCESS! Raw data saved to {filepath}")
                import subprocess
                subprocess.Popen(['notepad.exe', filepath])
            else:
                print("Failed to extract text from the report.")

if __name__ == "__main__":
    main()
