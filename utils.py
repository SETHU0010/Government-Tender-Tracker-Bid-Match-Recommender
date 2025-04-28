import requests
import pdfplumber
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_url):
    text = ""
    try:
        response = requests.get(pdf_url, stream=True, timeout=10) # Added timeout
        response.raise_for_status()
        with pdfplumber.open(response.content) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
    return text

def extract_scope_from_url(url):
    scope = ""
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # ADJUST THESE SELECTORS BASED ON THE STRUCTURE OF THE TENDER DETAIL PAGES
        scope_elements = soup.find_all('div', {'class': 'tender-details'}) # Example
        for element in scope_elements:
            scope += element.get_text(separator='\n').strip() + "\n"
        if not scope:
            # Try other common elements if 'tender-details' is not found
            scope_elements = soup.find_all('div', {'class': 'description'})
            for element in scope_elements:
                scope += element.get_text(separator='\n').strip() + "\n"
            if not scope:
                scope_elements = soup.find_all('p')
                for element in scope_elements:
                    scope += element.get_text().strip() + "\n"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    return scope