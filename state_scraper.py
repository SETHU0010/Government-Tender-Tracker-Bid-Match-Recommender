import requests
from bs4 import BeautifulSoup

def fetch_state_tenders(url="https://bidplus.gem.gov.in/all-bids/"): # REPLACE WITH ACTUAL URL
    tenders = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # IDENTIFY THE CORRECT HTML ELEMENTS FOR TENDER LISTINGS ON YOUR STATE PORTAL
        tender_items = soup.find_all('div', {'class': 'tender-item'}) # Example class - ADJUST THIS
        for item in tender_items:
            title_element = item.find('h3', {'class': 'tender-title'}) # ADJUST THIS
            organization_element = item.find('span', {'class': 'org-name'}) # ADJUST THIS
            link_element = item.find('a', {'class': 'tender-link'}) # ADJUST THIS
            deadline_element = item.find('span', {'class': 'deadline'}) # ADJUST THIS

            tender = {
                'title': title_element.text.strip() if title_element else None,
                'organization': organization_element.text.strip() if organization_element else None,
                'view_details_url': url + link_element['href'] if link_element and 'href' in link_element.attrs else None,
                'closing_date': deadline_element.text.strip() if deadline_element else None,
                'source': 'State Portal'
            }
            tenders.append(tender)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state portal data from {url}: {e}")
    return tenders

if __name__ == '__main__':
    # REPLACE WITH AN ACTUAL STATE PORTAL URL FOR TESTING
    state_tenders = fetch_state_tenders("https://bidplus.gem.gov.in/all-bids/")
    for tender in state_tenders:
        print(tender)