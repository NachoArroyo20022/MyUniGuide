import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the website
base_url = "https://www.ouinfo.ca/programs/search/?search=&group="

# Groups to scrape (A, B, C, ..., T-Z)
groups = [
    "a", "b", "c", "d-e", "f-g", "h", "i", "j-l", "m", "n-p", "q-s", "t-z"
]

# Initialize an empty list to store all data
all_data = []

# Loop through each group
for group in groups:
    print(f"Scraping group: {group.upper()}")

    # Construct the URL for the current group
    url = base_url + group

    # Send a GET request to the website
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for group {group}. HTTP Status code: {response.status_code}")
        continue

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the section containing all program cards
    programs_section = soup.find('div', class_='results results-programs')
    if not programs_section:
        print(f"No programs section found for group {group}.")
        continue

    # Extract information from each program card
    program_articles = programs_section.find_all('article', class_='result result-program')
    for article in program_articles:
        # Extract program name
        program_name_tag = article.find('h2', class_='result-heading')
        program_name = program_name_tag.text.strip() if program_name_tag else None

        # Extract program link
        program_link = program_name_tag.find('a')['href'] if program_name_tag and program_name_tag.find('a') else None
        if program_link:  # Append the base URL if the link is relative
            program_link = "https://www.ouinfo.ca" + program_link

        # Extract university name
        university_name_tag = article.find('h3', class_='result-subheading')
        university_name = university_name_tag.text.strip() if university_name_tag else None

        # Append the data
        all_data.append({
            'Program Name': program_name,
            'University Name': university_name,
            'Program Link': program_link,
        })

# Create a DataFrame from the accumulated data
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv('OUINFO_Scrape_data.csv', index=False)

# Display the DataFrame
print(df)
