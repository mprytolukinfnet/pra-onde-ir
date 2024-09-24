import requests, pickle, json, urllib3
import pandas as pd
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AirbnbScraper(object):
    def __init__(self, language="pt_br"):
        self.base_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "device-memory": "8",
            "dpr": "1.25",
            "ect": "4g",
            "priority": "u=0, i",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-ch-ua-platform-version": '"6.8.12"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "viewport-width": "545",
        }
        self.language = language

        try:
            with open("cookies", "rb") as f:
                self.cookies = pickle.load(f)
        except FileNotFoundError:
            self.cookies = self.get_cookies()

    def get_cookies(self):
        domain = ".br" if self.language == "pt_br" else ""
        headers = dict(**self.base_headers)
        response = requests.get(
            f"https://www.airbnb.com{domain}", headers=headers, verify=False
        )
        return response.cookies

    def get_stay_description(self, id):
        headers = dict(**self.base_headers)
        domain = ".br" if self.language == "pt_br" else ""
        url = f"https://www.airbnb.com{domain}/rooms/{id}"

        response = requests.get(
            url, cookies=self.cookies, headers=headers, verify=False
        )

        soup = BeautifulSoup(response.text, "html.parser")
        data_script = soup.find("script", {"id": "data-deferred-state-0"})
        data_json = json.loads(data_script.text)
        product_detail = data_json["niobeMinimalClientData"][0][1]["data"][
            "presentation"
        ]["stayProductDetailPage"]["sections"]["sections"]

        target_section = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["section"] != None
            and "htmlDescription" in s["section"]
        ][0]

        description = target_section["section"]["htmlDescription"]["htmlText"]

        return description

    def parse_stays(self, response, region):
        soup = BeautifulSoup(response.text, "html.parser")
        data_script = soup.find("script", {"id": "data-deferred-state-0"})
        data_json = json.loads(data_script.text)
        data = data_json["niobeMinimalClientData"][0][1]["data"]["presentation"][
            "staysSearch"
        ]["results"]["searchResults"]

        # Extract relevant information and store in a list of dictionaries
        extracted_data = []

        for item in data:
            listing = item["listing"]
            pricing = item["pricingQuote"]["structuredStayDisplayPrice"]["primaryLine"]
            coordinates = listing["coordinate"]

            # Extract and clean name
            name = listing["name"].replace("\n", " ")

            # Extract and clean price
            price_str = (
                pricing["price"] if "price" in pricing else pricing["discountedPrice"]
            )
            price_num = int(
                price_str.replace("R$", "").replace(",", "").replace(".", "")
            )

            # Extract and clean rating and reviews
            rating_value, reviews_count = 0, 0
            rating_str = listing.get("avgRatingLocalized", "0.0 (0)")
            if rating_str not in ("New", "Novo", None):
                rating_value, reviews_count = rating_str.split(" (")
                if self.language == "pt_br":
                    rating_value = rating_value.replace(",", ".")
                rating_value = float(rating_value)
                reviews_count = int(reviews_count.strip(")"))

            # Amenities and Pictures
            amenities = (
                [
                    msg
                    for pic in listing["contextualPictures"]
                    if pic.get("caption")
                    and "messages" in pic["caption"]
                    and pic["caption"]["messages"] != None
                    for msg in pic["caption"]["messages"]
                ]
                if listing["contextualPictures"]
                else []
            )
            pictures = [
                pic["picture"]
                for pic in listing["contextualPictures"]
                if "picture" in pic
            ]

            try:
                description = self.get_stay_description(listing["id"])
            except:
                description = ""

            # Extracting data
            room_info = {
                "Region": region,
                "Listing ID": listing["id"],
                "Name": name,
                "Title": listing["title"],
                "Room Type": listing["roomTypeCategory"],
                "Price per Night (R$)": price_num,
                "Rating": rating_value,
                "Reviews": reviews_count,
                "Latitude": coordinates["latitude"],
                "Longitude": coordinates["longitude"],
                "Badge": item["badges"][0]["text"] if item["badges"] else None,
                "Description": description,
                "Amenities": amenities,
                "Pictures": pictures,
            }

            extracted_data.append(room_info)

        # Convert to DataFrame
        df = pd.DataFrame(extracted_data)

        return df

    def get_stays(self, region):
        print(f"Getting stays from: `{region}`")
        headers = dict(**self.base_headers)

        domain = ".br" if self.language == "pt_br" else ""
        region1 = region.replace(" ", "-")
        region2 = region.replace(" ", "%20")

        url = f"https://www.airbnb.com{domain}/s/{region1}--Brazil/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&query={region2}%2C%20Brazil&date_picker_type=flexible_dates&source=structured_search_input_header&search_type=autocomplete_click"
        response = requests.get(
            url, cookies=self.cookies, headers=headers, verify=False
        )
        return self.parse_stays(response, region)

    def fetch(self):
        regions = [
            "Acre",
            "Alagoas",
            "Amazonas",
            "Bahia",
            "Ceará",
            "Espírito Santo",
            "Goiás",
            "Maranhão",
            "Mato Grosso",
            "Mato Grosso do Sul",
            "Minas Gerais",
            "Pará",
            "Paraíba",
            "Paraná",
            "Pernambuco",
            "Piauí",
            "Rio de Janeiro",
            "Rio Grande do Norte",
            "Rio Grande do Sul",
            "Rondônia",
            "Roraima",
            "Santa Catarina",
            "São Paulo",
            "Sergipe",
            "Tocantins",
        ]
        dfs = [self.get_stays(region) for region in regions]
        return pd.concat(dfs, ignore_index=True)
