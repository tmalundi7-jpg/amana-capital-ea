import requests
from bs4 import BeautifulSoup
import pdfplumber
import os
import io

DSE_URL = "https://dse.co.tz/"

def find_latest_market_report_pdf():
    """
    Scrapes the DSE homepage (and potentially other pages) to find the 
    link to the latest daily market report PDF.
    """
    print(f"Scraping {DSE_URL} for market reports...")
    try:
        response = requests.get(DSE_URL, verify=False) # verify=False just in case of SSL issues
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching DSE website: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the daily-reports tab
    daily_reports_div = soup.find('div', id='daily-reports')
    
    if not daily_reports_div:
        print("Could not find the 'daily-reports' section on the page.")
        return None
        
    # Find the first PDF link inside the daily-reports section
    target_pdf_url = None
    import re
    cards = daily_reports_div.find_all('div', class_='card')
    if cards:
        a = cards[0].find('a', href=re.compile('/get/daily/report'))
        if a:
            href = a['href']
            target_pdf_url = DSE_URL.rstrip('/') + href if href.startswith('/') else href
    else:
        for a in daily_reports_div.find_all('a', href=True):
            href = a['href']
            # The DSE daily market report links look like: https://dse.co.tz/get/daily/report/...
            if '/get/daily/report' in href.lower():
                if href.startswith('/'):
                    target_pdf_url = DSE_URL.rstrip('/') + href
                else:
                    target_pdf_url = href
                break
            
    if target_pdf_url:
        print(f"Found Daily Market Report PDF: {target_pdf_url}")
    else:
        print("No PDF links found in the daily-reports section.")
        
    return target_pdf_url

def extract_text_from_pdf_url(pdf_url):
    print(f"Downloading PDF from {pdf_url}...")
    response = requests.get(pdf_url, verify=False, stream=True)
    
    if response.status_code != 200:
        print(f"Failed to download PDF. HTTP Status: {response.status_code}")
        return None
        
    print("Extracting text from PDF...")
    pdf_content = io.BytesIO(response.content)
    
    text = ""
    try:
        with pdfplumber.open(pdf_content) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        # The DSE website actually serves an HTML viewer (pdf2htmlEX) instead of a raw PDF sometimes!
        # Fallback to parsing the text directly from the HTML viewer
        print("Attempting to extract text from HTML viewer fallback...")
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_lines = []
            for el in soup.find_all('div', class_='t'):
                text_lines.append(el.get_text(strip=True))
            
            if text_lines:
                text = "\n".join(text_lines)
                print(f"Successfully extracted {len(text_lines)} lines of text from the HTML viewer!")
            else:
                # Absolute fallback if no 'div.t' found
                text = soup.get_text(separator=' ', strip=True)
                print("Fallback to raw text extraction.")
        except Exception as html_err:
            print(f"Fallback extraction failed: {html_err}")
            return None
            
    return text.strip()

def get_dse_market_data():
    """
    The main public function to be called by generate_daily_wrap.py
    """
    pdf_url = find_latest_market_report_pdf()
    if not pdf_url:
        return None
        
    raw_text = extract_text_from_pdf_url(pdf_url)
    
    # We will pass the raw extracted text as the market summary to DeepSeek.
    # DeepSeek is smart enough to extract the Equity and Bond data from the raw PDF text!
    import datetime
    return {
        "date": datetime.date.today().strftime("%d %B %Y"),
        "text": raw_text
    }

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    data = get_dse_market_data()
    if data:
        print("\n--- Extracted Data Sample ---")
        print(f"Date: {data['date']}")
        print(f"Text Snippet: {data['text'][:500]}...")
