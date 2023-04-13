import requests
from bs4 import BeautifulSoup
import csv

# Define the URL to scrape
url = "https://www.drugs.com/alpha/a.html"
baseurl="https://www.drugs.com"

# Send a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "lxml")

# Finding all the drug links on the page
drug_links = soup.select("ul.ddc-list-column-2 li a")

# function to scrape the drug information from a drug page
def scrape_drug_info(url):
    # Send a request to the drug page and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using Beautifulsoup
    soup = BeautifulSoup(html_content, "lxml")

    # Find the drug name
    drug_name = soup.select_one("div.ddc-pronounce-title h1")

    # find the description
    drug_desc = soup.find('div', {'class': 'contentBox'}).contents[11].text.strip()+soup.find('div', {'class': 'contentBox'}).contents[13].text.strip()+soup.find('div', {'class': 'contentBox'}).contents[15].text.strip()
    
    # find the missed dose question
    missed_dose=soup.find('div', {'class': 'contentBox'}).contents[80].text.strip()

    #find the over dose
    over_dose=soup.find('div', {'class': 'contentBox'}).contents[86].text.strip()
    

    
   

    # Find the drug side effects

    side_effects = soup.find('div', {'class': 'contentBox'}).contents[108].text.strip()+soup.find('div', {'class': 'contentBox'}).contents[110].text.strip()
    

    return [drug_name, drug_desc,missed_dose,over_dose,side_effects]

# Open a CSV file to write the drug information
with open("Adrugs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Name", "Description","missed_dose","over_dose","side_effects"])

    # Loop through each drug link and scrape its information
    for link in drug_links:
        # Construct the full URL of the drug page
        drug_url = baseurl+ link["href"]

        # Scrape the drug information from the drug page
        drug_info = scrape_drug_info(drug_url)
    
        

        # Write the drug information to the CSV file
        writer.writerow(drug_info)
