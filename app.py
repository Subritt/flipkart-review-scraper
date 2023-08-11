import requests
import csv
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

url = f'https://www.flipkart.com/apple-2020-macbook-air-m1-8-gb-256-gb-ssd-mac-os-big-sur-mgn63hn-a/product-reviews/itmde54f026889ce?pid=COMFXEKMGNHZYFH9&lid=LSTCOMFXEKMGNHZYFH9P56X45&marketplace=FLIPKART'
response = requests.get(url)

# get the scraped reviews
def get_reviews(url):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all review sections on the page
    review_sections = soup.find_all('div', class_='col _2wzgFH K0kLPL')

    # Create a list to store the review data
    reviews = []

    # Loop through each review section and extract the full review description
    for section in review_sections:
        #Extract the rating
        rating = section.find('div', class_='_3LWZlK _1BLPMq').text.strip()

        # Extract the review header from the existing HTML
        header = section.find('p', class_='_2-N8zT').text.strip()
        # print(header)

        # Extract the full review description from the existing HTML
        description = section.find('div', class_='t-ZTKy').find('div').find('div', class_='').text.strip()
        # print(description)

        # Add the review data to the list of reviews
        reviews.append({'Header': header, 'Rating': rating, 'Description': description})

    return reviews

df = pd.DataFrame(get_reviews(url))
csv_file = df.to_csv().encode('utf-8')

st.write('# Review Summary')

st.download_button(
    label="Download data as CSV",
    data=csv_file,
    file_name='reviews.csv',
    mime='text/csv',
)

# st.table(df.style.hide_index())


