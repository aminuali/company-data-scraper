
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:22:50 2024

@author: Ali Aminu 
"""
#import required packages
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# url of the site to extract data from
url = "https://www.ycombinator.com/companies"

# Define Chrome webdriver options
options = webdriver.ChromeOptions()

# Set the chrome webdriver to run in headless mode
options.add_argument("--headless")

# Pass the defined options object to initialize the web driver
driver = webdriver.Chrome(options=options)

# Set an implicit wait of five seconds
driver.implicitly_wait(5)

driver.get(url)
time.sleep(5)

pages = 10  # Number of pages to load
page_delay = 5  # Time to wait for each page to load

for i in range(pages):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(page_delay)
    print(f"Page {i+1} of {pages} loaded")  # Prints the page number for debugging purpose

# Get the page source and parse with BeautifulSoup
html = driver.page_source

sp = BeautifulSoup(html, 'html.parser')


company = []  # List to store company data

# Extract Company data using BeautifulSoup 
for item in sp.find_all('a', class_='_company_99gj3_339'):
    title = item.find_next('span', class_='_coName_99gj3_454').text.strip()  # Get text and strip whitespace
    address = item.find_next('span', class_='_coLocation_99gj3_470').text.strip()
    description = item.find_next('span', class_='_coDescription_99gj3_479').text.strip()
    # Assuming tags are in separate spans with class 'pill_19sud_33'
    tags = [tag.text.strip() for tag in item.find_all('span', class_='pill _pill_99gj3_33')]
    tag_string = ", ".join(tags) if tags else ""  # Join tags with comma and space
    
    #append extracted data to companies list
    company.append({
        "Title": title,
        "Address": address,
        "Description": description,
        "Tag": tag_string
    })

# Close the web driver
driver.close()

# Save scraped data to CSV 
df = pd.DataFrame(company)
df.to_csv('Ycom_Data.csv', index=False)
