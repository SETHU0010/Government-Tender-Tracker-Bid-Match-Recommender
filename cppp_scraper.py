import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_cppp_tenders():
    tenders = []
    url = "https://eprocure.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page" # Example
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        tender_table = soup.find('table', {'class': 'list_work'})
        if tender_table:
            rows = tender_table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 7:
                    tender = {
                        'title': columns[2].text.strip(),
                        'organization': columns[1].text.strip(),
                        'reference_no': columns[3].text.strip(),
                        'publish_date': columns[4].text.strip(),
                        'closing_date': columns[5].text.strip(),
                        'view_details_url': 'https://eprocure.gov.in/' + columns[2].find('a')['href'] if columns[2].find('a') else None,
                        'source': 'CPPP'
                    }
                    tenders.append(tender)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CPPP data: {e}")
    return tenders

if __name__ == '__main__':
    tenders = fetch_cppp_tenders()
    for tender in tenders:
        print(tender)