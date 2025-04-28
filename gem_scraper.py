import requests
import json
from config import GEM_API_BASE_URL

def fetch_gem_tenders(search_term="government tenders", page_number=1, page_size=10):
    tenders = []
    api_url = f"{GEM_API_BASE_URL}listings"  # Trying a different endpoint

    params = {
        "q": search_term,
        "page": page_number,
        "size": page_size
    }

    headers = {
        'Content-Type': 'application/json'
        # Add any potential API keys or authentication headers here if required
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and isinstance(data['data'], list): # Assuming the data is a list of listings
            for listing in data['data']:
                tender = {
                    'title': listing.get('title'),
                    'organization': listing.get('seller_name'),
                    'reference_no': listing.get('order_no'),
                    'publish_date': listing.get('published_on'),
                    'closing_date': listing.get('bid_end_date'),
                    'view_details_url': f"https://mkp.gem.gov.in/tender/{listing.get('id')}",
                    'source': 'GeM'
                }
                tenders.append(tender)
        if 'total_pages' in data and page_number < data['total_pages']: # Assuming pagination info is like this
            tenders.extend(fetch_gem_tenders(search_term, page_number + 1, page_size))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GeM data: {e}")
        if e.response is not None:
            print(f"GeM Response Status Code: {e.response.status_code}")
            print(f"GeM Response Content: {e.response.text}")
    except json.JSONDecodeError:
        print("Error decoding GeM JSON response.")
    return tenders

if __name__ == '__main__':
    tenders = fetch_gem_tenders()
    for tender in tenders:
        print(tender)