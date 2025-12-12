import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URL (This is a sandbox website specifically made for scraping practice)
url = 'http://books.toscrape.com/'

# Set a User-Agent to mimic a real browser request (prevents being blocked as a bot)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_books():
    print("Starting data extraction... please wait.")
    
    try:
        # Send GET request to the website
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (Status Code 200)
        if response.status_code != 200:
            print(f"Connection failed! Status code: {response.status_code}")
            return

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all container elements that hold book information
        books = soup.find_all('article', class_='product_pod')
        
        # List to store the extracted data
        book_data = []

        for book in books:
            # Extract Title (found in <h3> -> <a> tag, attribute 'title')
            title = book.h3.a['title']
            
            # Extract Price
            price = book.find('p', class_='price_color').text
            
            # Extract Availability status
            availability = book.find('p', class_='instock availability').text.strip()
            
            # Append the row to our list
            book_data.append([title, price, availability])
            
        # Save the data to a CSV file
        output_filename = 'scraped_books.csv'
        
        with open(output_filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the Header row
            writer.writerow(['Book Title', 'Price', 'Availability']) 
            # Write the data rows
            writer.writerows(book_data)
            
        print(f"Success! Extracted {len(book_data)} books and saved them to '{output_filename}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    scrape_books()