import requests
from bs4 import BeautifulSoup
import re
import time
import random
import datetime
from property import Property

class PropertyScraper:
    """Class for obtaining rental properties from SS.com (Rīga only)"""

    def __init__(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
        ]
        self.headers = {
            'User-Agent': random.choice(user_agents),
            'Accept-Language': 'en,lv;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/'
        }

    def scrape_ss_com(self, max_price=1500):
        properties = []
        url = "https://www.ss.com/en/real-estate/flats/riga/all/hand_over/"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            ads = soup.select('tr[id^=tr_]')

            for ad in ads:
                try:
                    link_tag = ad.select_one('a')
                    if not link_tag or not link_tag.get('href'):
                        continue

                    link = link_tag['href']
                    if not link.startswith('http'):
                        link = "https://www.ss.com" + link

                    title = link_tag.text.strip()
                    price_cell = ad.select_one('td:nth-last-child(1)')
                    if not price_cell:
                        continue

                    price_text = price_cell.text.strip().replace(' ', '')
                    price_match = re.search(r'(\d+)', price_text)
                    if not price_match:
                        continue

                    price = float(price_match.group(1))
                    if price > max_price:
                        continue

                    property_details = self._get_ss_property_details(link)
                    if not property_details:
                        continue

                    property_obj = Property(
                        id=link.split('/')[-2] if '/' in link else f"ss_{random.randint(1000, 9999)}",
                        title=title,
                        price=price,
                        address=property_details.get('address', 'Riga'),
                        size=property_details.get('size', 50),
                        rooms=property_details.get('rooms', 1),
                        floor=property_details.get('floor', None),
                        has_furniture=property_details.get('has_furniture', None),
                        kitchen_equipment=property_details.get('kitchen_equipment', []),
                        bathroom=property_details.get('bathroom', None),
                        utilities_included=property_details.get('utilities_included', None),
                        source_url=link,
                        portal="ss.com",
                        published_date=property_details.get('published_date', None),
                        has_parking=property_details.get('has_parking', None),
                        pets_allowed=property_details.get('pets_allowed', None),
                        min_rent_term=property_details.get('min_rent_term', None)
                    )

                    properties.append(property_obj)
                except Exception:
                    continue

                time.sleep(random.uniform(0.3, 0.5))

        except Exception:
            return []

        return properties

    def _get_ss_property_details(self, url):
        details = {}
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return details

            soup = BeautifulSoup(response.content, 'html.parser')

            address_row = soup.find('td', string=re.compile('Address:|District:|Region:'))
            if address_row and address_row.find_next('td'):
                details['address'] = address_row.find_next('td').text.strip()
            else:
                details['address'] = "Riga"

            size_row = soup.find('td', string=re.compile('Area:'))
            if size_row and size_row.find_next('td'):
                size_text = size_row.find_next('td').text.strip()
                size_match = re.search(r'(\d+(?:\.\d+)?)', size_text)
                details['size'] = float(size_match.group(1)) if size_match else 50
            else:
                details['size'] = 50

            rooms_row = soup.find('td', string=re.compile('Rooms:'))
            if rooms_row and rooms_row.find_next('td'):
                rooms_text = rooms_row.find_next('td').text.strip()
                rooms_match = re.search(r'(\d+)', rooms_text)
                details['rooms'] = int(rooms_match.group(1)) if rooms_match else 1
            else:
                details['rooms'] = 1

            floor_row = soup.find('td', string=re.compile('Floor:'))
            if floor_row and floor_row.find_next('td'):
                floor_text = floor_row.find_next('td').text.strip()
                floor_match = re.search(r'(\d+)', floor_text)
                details['floor'] = int(floor_match.group(1)) if floor_match else None
            else:
                details['floor'] = None

            description = soup.find('div', id='msg_div_msg') or soup.find('div', class_='ads_opt')
            if description:
                desc_text = description.text.lower()
                details['has_furniture'] = any(k in desc_text for k in ['furnished', 'with furniture', 'мебел', 'ar mēbelēm'])
                details['has_parking'] = any(k in desc_text for k in ['parking', 'парковка', 'stāvvieta', 'autostāvvieta'])
                details['pets_allowed'] = any(k in desc_text for k in ['pets allowed', 'животные разрешены', 'dzīvnieki atļauti'])
                if any(k in desc_text for k in ['one year', '1 year', 'на год', 'uz gadu']):
                    details['min_rent_term'] = '1 year'
                elif any(k in desc_text for k in ['6 months', '6 mēneši', '6 месяцев']):
                    details['min_rent_term'] = '6 months'
                else:
                    details['min_rent_term'] = None
                details['utilities_included'] = 'utilities included' in desc_text or 'including utilities' in desc_text
            else:
                details.update({'has_furniture': None, 'has_parking': None, 'pets_allowed': None, 'min_rent_term': None, 'utilities_included': False})

            details['published_date'] = datetime.date.today().isoformat()

        except Exception:
            pass

        return details