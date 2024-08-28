import requests
from bs4 import BeautifulSoup
import json
import re
import html
import sys

# Configure stdout to handle UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Data setup
months = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
length = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# List to hold the data
events = []

for i, month in enumerate(months):
    for j in range(length[i]):
        date = f"{j+1:02d}-{i+1:02d}"  # Format date as DD-MM
        url = f"https://da.wikipedia.org/wiki/{j+1}._{month}"

        try:
            # Fetch the webpage
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the <div> with the class "mw-heading mw-heading3"
            target_div = soup.find('div', class_='mw-heading mw-heading3')

            # Initialize the variable to hold the <ul> found after the target <div>
            following_ul = None

            # If the target <div> is found, search for the next sibling <ul>
            if target_div:
                following_ul = target_div.find_next_sibling('ul')

            if following_ul:
                # Find all <li> elements within the <ul>
                li_elements = following_ul.find_all('li')

                for li_element in li_elements:
                    # Get text and clean up
                    clear_text = li_element.get_text(separator=' ', strip=True)
                    
                    # Normalize whitespace: Replace non-breaking spaces and multiple spaces with a single space
                    clear_text = clear_text.replace('\xad', ' ')
                    clear_text = re.sub(r'\s+', ' ', clear_text)
                    
                    # Decode HTML entities
                    clear_text = html.unescape(clear_text)

                    event = {
                        "date": date,
                        "event": clear_text
                    }
                    print(event)
                    events.append(event)

        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")

# Write the collected events to a JSON file
with open('events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=4)

print("Data has been written to events.json")
