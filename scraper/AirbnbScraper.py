import requests, pickle, urllib3
from bs4 import BeautifulSoup
import json

try:
    import pandas as pd
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    import undetected_chromedriver as uc
    import concurrent.futures
    import re
except ImportError as ie:
    print(ie)
    print("Modules not found, should be ok if only fetching Airbnb pictures")

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

    def get_stay_soup(self, id):
        headers = dict(**self.base_headers)
        domain = ".br" if self.language == "pt_br" else ""
        url = f"https://www.airbnb.com{domain}/rooms/{id}"

        response = requests.get(
            url, cookies=self.cookies, headers=headers, verify=False
        )

        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def get_stay_pictures(self, id):
        soup = self.get_stay_soup(id)
        #pictures = [picture.find_all("source")[0]['srcset'].split()[0] for picture in soup.find_all("picture")]

        data_script = soup.find("script", {"id": "data-deferred-state-0"})
        data_json = json.loads(data_script.text)

        product_detail = data_json["niobeMinimalClientData"][0][1]["data"][
            "presentation"
        ]["stayProductDetailPage"]["sections"]["sections"]

        preview_images = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["sectionId"] == "HERO_DEFAULT"
        ][0]["section"]["previewImages"]

        pictures = [img["baseUrl"] for img in preview_images][:5]

        return pictures

    def get_stay_data(self, id):
        soup = self.get_stay_soup(id)
        data_script = soup.find("script", {"id": "data-deferred-state-0"})
        data_json = json.loads(data_script.text)
        product_detail = data_json["niobeMinimalClientData"][0][1]["data"][
            "presentation"
        ]["stayProductDetailPage"]["sections"]["sections"]

        name = ""
        personCapacity = ""
        roomType = ""
        rating = 0
        reviews = 0
        title = ""
        latitude = ""
        longitude = ""
        description = ""
        amenities = []
        pictures = []

        # Embed_data
        embed_data = []

        embed_data_section = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["sectionId"] == "TITLE_DEFAULT"
            and "shareSave" in s["section"]
            and s["section"]["shareSave"] != None
            and "embedData" in s["section"]["shareSave"]
            and s["section"]["shareSave"]["embedData"] != None
        ]

        if len(embed_data_section) > 0:
            embed_data = embed_data_section[0]["section"]["shareSave"]["embedData"]
            name = embed_data["name"]
            if name:
                name = name.replace("\n", " ")
            personCapacity = embed_data["personCapacity"]
            roomType = embed_data["propertyType"]
            rating = embed_data["starRating"]
            reviews = embed_data["reviewCount"]

        # Title
        sbui_data = data_json["niobeMinimalClientData"][0][1]["data"]["presentation"][
            "stayProductDetailPage"
        ]["sections"]["sbuiData"]["sectionConfiguration"]["root"]["sections"]

        title_section = [
            s
            for s in sbui_data
            if isinstance(s, dict)
            and s["sectionId"] == "OVERVIEW_DEFAULT_V2"
            and "sectionData" in s
            and s["sectionData"] != None
            and "title" in s["sectionData"]
        ]
        if len(title_section) > 0:
            title = title_section[0]["sectionData"]["title"]

        # Description
        description_section = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["section"] != None
            and "htmlDescription" in s["section"]
            and s["section"]["htmlDescription"] != None
            and "htmlText" in s["section"]["htmlDescription"]
        ]

        if len(description_section) > 0:
            description = description_section[0]["section"]["htmlDescription"][
                "htmlText"
            ]
            if description:
                description = description.replace("\n", " ").replace("\t", " ")

        # Amenities
        amenities_groups = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["sectionId"] == "AMENITIES_DEFAULT"
            and "seeAllAmenitiesGroups" in s["section"]
            and s["section"]["seeAllAmenitiesGroups"] != None
        ]

        if len(amenities_groups) > 0:
            ag = amenities_groups[0]["section"]["seeAllAmenitiesGroups"]
            amenities = [a["title"] for ag in ag for a in ag["amenities"]]

        # Pictures
        pictures_groups = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["sectionId"] == "PHOTO_TOUR_SCROLLABLE_MODAL"
            and "mediaItems" in s["section"]
            and s["section"]["mediaItems"] != None
        ]

        if len(pictures_groups) > 0:
            pg = pictures_groups[0]["section"]["mediaItems"]
            pictures = [p["baseUrl"] for p in pg]

        # Coordinates
        coordinates_section = [
            s
            for s in product_detail
            if isinstance(s, dict)
            and "section" in s
            and s["sectionId"] == "LOCATION_DEFAULT"
            and "lat" in s["section"]
            and s["section"]["lat"] != None
            and "lng" in s["section"]
            and s["section"]["lng"] != None
        ]

        if len(coordinates_section) > 0:
            coordinates = coordinates_section[0]["section"]
            latitude = coordinates["lat"]
            longitude = coordinates["lng"]

        return {
            "name": name,
            "title": title,
            "roomType": roomType,
            "personCapacity": personCapacity,
            "rating": rating,
            "reviews": reviews,
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
            "amenities": amenities,
            "pictures": pictures,
        }

    def get_stay_details(self, stays, region):
        def process_listing(stay):
            id = stay["id"]
            price = stay["price"]
            badge = stay["badge"]
            # Try to get stay details, otherwise return empty
            try:
                stay_data = self.get_stay_data(id)
            except:
                return dict()
            (
                name,
                title,
                roomType,
                personCapacity,
                rating,
                reviews,
                latitude,
                longitude,
                description,
                amenities,
                pictures,
            ) = (
                stay_data["name"],
                stay_data["title"],
                stay_data["roomType"],
                stay_data["personCapacity"],
                stay_data["rating"],
                stay_data["reviews"],
                stay_data["latitude"],
                stay_data["longitude"],
                stay_data["description"],
                stay_data["amenities"],
                stay_data["pictures"],
            )
            # Extracting data
            return {
                "Region": region,
                "Listing ID": id,
                "Name": name,
                "Title": title,
                "Room Type": roomType,
                "Person Capacity": personCapacity,
                "Price per Night (R$)": price,
                "Rating": rating,
                "Reviews": reviews,
                "Latitude": latitude,
                "Longitude": longitude,
                "Badge": badge,
                "Description": description,
                "Amenities": amenities,
                "Pictures": pictures,
            }

        # Use ThreadPoolExecutor to parallelize fetching stay details
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_listing, stays))
            results = [r for r in results if len(r) > 0]

        # Convert to DataFrame
        df = pd.DataFrame(results)

        return df

    def get_stays_list(self):
        # Wait for element
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/a',
                    )
                )
            )
        except TimeoutException as ex:
            # Não existe mais um botão
            return None
        # Find all the divs under the specified parent div
        parent_divs = self.driver.find_elements(
            By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div'
        )

        # List to store all hrefs
        stays = []

        # Loop through each div and extract hrefs
        for i in range(1, len(parent_divs) + 1):  # XPath index starts at 1
            try:
                # Construct the dynamic XPath for each 'a' tag inside the div[i]
                a_tag_xpath = f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/a'

                # Find the 'a' tag using the dynamic XPath
                a_tag = self.driver.find_element(By.XPATH, a_tag_xpath)

                # Extract the href attribute if available
                href = a_tag.get_attribute("href")
                if href:
                    match = re.search(r"/rooms/(\d+)\?", href)
                    if match:
                        id = match.group(1)
                        price_tag_xpath = f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[5]/div[2]/div/div/span/div/span[position() = (last() - 1)]'
                        # Find the 'a' tag using the dynamic XPath
                        price_tag = self.driver.find_element(By.XPATH, price_tag_xpath)
                        price_str = price_tag.text
                        price = int(
                            price_str.replace("R$", "")
                            .replace(",", "")
                            .replace(".", "")
                        )
                        badge = ""
                        badge_xpath = f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[1]/div/div/div[1]/div/div[1]/div[1]/div/span'
                        badge_elements = self.driver.find_elements(
                            By.XPATH, badge_xpath
                        )
                        if badge_elements:
                            # If the list is not empty, the element exists, and you can access the text
                            badge = badge_elements[0].text
                        else:
                            # If the list is empty, no badge was found
                            badge = None
                        stays.append({"id": id, "price": price, "badge": badge})
            except Exception as e:
                # print(f"Error extracting href from div[{i}]: {e}")
                pass

        return stays

    def get_stays(self, region):
        print(f"Getting stays from: `{region}`")

        domain = ".br" if self.language == "pt_br" else ""
        region1 = region.replace(" ", "-")
        region2 = region.replace(" ", "%20")

        url = f"https://www.airbnb.com{domain}/s/{region1}--Brazil/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&query={region2}%2C%20Brazil&date_picker_type=flexible_dates&source=structured_search_input_header&search_type=autocomplete_click"

        dfs = []

        self.driver.get(url)

        # Máximo de páginas retornadas na consulta. Limite do Airbnb é 15
        num_paginas = 15

        for i in range(num_paginas):
            print(f"Getting page {i}:")
            stays = self.get_stays_list()
            if stays == None:
                break
            dfs.append(self.get_stay_details(stays, region))
            # Se estiver na página 15 não precisa procurar o botão
            if i == num_paginas - 1:
                break
            try:
                # Espera até que o elemento <a> com aria-label="Próximo" seja clicável
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Próximo']"))
                )
            except TimeoutException as ex:
                # Não existe mais um botão
                break

            # Clica no botão de próxima página
            next_button.click()

        return pd.concat(dfs, ignore_index=True)

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
        self.driver = uc.Chrome(headless=False, use_subprocess=False)
        dfs = [self.get_stays(region) for region in regions]
        self.driver.quit()
        return pd.concat(dfs, ignore_index=True)
