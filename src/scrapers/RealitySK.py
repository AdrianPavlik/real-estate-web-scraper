import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import math

# not working currently !!!!!!!!!!!!

class RealityScraper:
    def __init__(self, url):
        self.baseUrl = url
        self.pageUrl = f"{self.baseUrl}/?page="
        self.csv_file = f"{self.get_domain_name(self.baseUrl)}.csv"
        self.district = url.split("/")[3]
        self.previous_data = []

    def get_number_of_pages(self):
        # Make a GET request to the website
        response = requests.get(self.baseUrl)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find no of offers
        no_of_offers = soup.find("h1", class_="page-title").find_parent("div").find("div")
        no_of_offers = no_of_offers.get_text().replace(" ", "")
        no_of_offers = ''.join(map(str, [int(i) for i in no_of_offers if i.isdigit()]))

        # Calc no of pages
        return math.ceil(int(no_of_offers) / 24)

    def scrape_data(self):

        scraped_data = []

        for page in range(1, self.get_number_of_pages() + 1):
            # Make a GET request to the website
            response = requests.get(f"{self.pageUrl}{page}")

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Get div element containing the adverts
            data_elements = soup.findAll("div", class_="offer-item-in")

            # Iterate through adverts and scrape data
            for element in data_elements:
                title = element.find("h2")
                if title is not None and title != -1:
                    # Title
                    title = title["title"]

                    print(f"Currently on page {page}, with title {title}")

                    # City
                    city = city_type_size_data.find("div").find("div")["title"]  # Get element with title
                    city = city.split(",")
                    if len(city) > 2:
                        city = city[1]
                    else:
                        city = city[0]

                    # Type
                    type = city_type_size_data.find("div").findAll("div")[1]
                    if type is not None and type != -1:
                        type = type.get_text().split("•")[0]

                    # Size
                    size = city_type_size_data.find("div").findAll("div")[1].find("span")
                    if size is not None and size != -1:
                        size = size.get_text().split(" ")[0]

                    # Price
                    price = element.find("div", class_="advertisement-item--content__price")["data-adv-price"].replace("€", "")

                    # Date posted
                    date_posted = element.find("span", class_="d-none advertisement-item--content__additional-info--text").get_text()

                    # Create a dictionary for each data entry
                    data_entry = {
                        "title": title,
                        "district": self.district,
                        "city": city,
                        "type": type,
                        "size": size,
                        "price": price,
                        "date_posted": date_posted,
                        "timestamp": datetime.now()
                    }
                    scraped_data.append(data_entry)

        return scraped_data

    def get_domain_name(self, url):
        # Extract the domain name from the URL
        domain_name = url.split("//")[-1].split("/")[0].split(":")[0]
        return domain_name

    def load_previous_data(self):
        try:
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.previous_data = list(reader)
        except FileNotFoundError:
            pass

    def save_data_to_csv(self, data):
        with open(self.csv_file, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "district", "city", "type", "size", "price", "date_posted"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(data)

    def scrape_and_save_data(self):
        self.load_previous_data()
        scraped_data = self.scrape_data()
        new_data = [entry for entry in scraped_data if entry not in self.previous_data]

        if new_data:
            self.save_data_to_csv(new_data)
            print(f"{len(new_data)} new data entry(s) added to {self.csv_file}.")
        else:
            print("No new data found.")

        # Save the current data as the previous data for the next iteration
        with open(self.csv_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "district", "city", "type", "size", "price", "date_posted"])
            writer.writeheader()
            writer.writerows(scraped_data)


sites = [
    "https://www.reality.sk/presovsky-kraj",
    "https://www.reality.sk/trenciansky-kraj",
    "https://www.reality.sk/trnavsky-kraj",
    "https://www.reality.sk/bratislavsky-kraj",
    "https://www.reality.sk/zilinsky-kraj",
    "https://www.reality.sk/kosicky-kraj",
    "https://www.reality.sk/banskobystricky-kraj",
    "https://www.reality.sk/nitriansky-kraj"
]

for site in sites:
    scraper = RealityScraper(site)
    scraper.scrape_and_save_data()
