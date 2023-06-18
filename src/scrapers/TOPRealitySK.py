import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


class NehnutelnostiScraper:
    def __init__(self, url):
        self.baseUrl = url
        self.csv_file = f"{self.get_domain_name(self.baseUrl)}.csv"
        self.district = url.split("/")[3]
        self.previous_data = []

    def get_number_of_pages(self):
        # Make a GET request to the website
        response = requests.get(self.baseUrl)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find div of pagination box and find the last li element
        no_of_pages = soup.find("ul", class_="pagination").findAll("li")
        no_of_pages = int(no_of_pages[len(no_of_pages) - 2].get_text())

        return no_of_pages

    def scrape_data(self):

        scraped_data = []
        used_titles = []

        for page in range(1, self.get_number_of_pages() + 1):
            # Make a GET request to the website
            response = requests.get(f"{self.baseUrl}/{page}.html")

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Get div element containing the adverts
            data_elements = soup.find("div", class_="listing-items").findAll("div")

            # Iterate through adverts and scrape data
            for element in data_elements:
                title = element.find("h2")
                if title is not None and title != -1:
                    # Title
                    title = title.find('a').get_text()

                    if title not in used_titles:
                        used_titles.append(title)

                        print(f"[{self.district}][{page}] - {title}")

                        # City
                        city = element.find("span", class_="location-city")
                        if city is not None and city != -1:
                            city = city.get_text()

                        # Size
                        size = element.find("span", class_="value")
                        if size is not None and size != -1:
                            size = size.get_text().split(" ")[0]

                        # Price
                        price = element.find("strong", class_="price")
                        if price is not None and price != -1:
                            price = price.get_text().replace("€", "")

                        # Date posted
                        date_posted = element.find("li", class_="date")
                        if date_posted is not None and date_posted != -1:
                            date_posted = date_posted.get_text()

                        # Type
                        type = element.find("li", class_="date")
                        if type is not None and type != -1:
                            type = type.find_parent("ul").findAll("li")[1].get_text()

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
            writer = csv.DictWriter(file,
                                    fieldnames=["title", "district", "city", "type", "size", "price", "date_posted", "timestamp"])
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
            writer = csv.DictWriter(file,
                                    fieldnames=["title", "district", "city", "type", "size", "price", "date_posted", "timestamp"])
            writer.writeheader()
            writer.writerows(scraped_data)


sites = [
    "https://www.topreality.sk/presovsky-kraj",
    "https://www.topreality.sk/trenciansky-kraj",
    "https://www.topreality.sk/trnavsky-kraj",
    "https://www.topreality.sk/bratislavsky-kraj",
    "https://www.topreality.sk/zilinsky-kraj",
    "https://www.topreality.sk/kosicky-kraj",
    "https://www.topreality.sk/banskobystricky-kraj",
    "https://www.topreality.sk/nitriansky-kraj"
]

for site in sites:
    scraper = NehnutelnostiScraper(site)
    scraper.scrape_and_save_data()
