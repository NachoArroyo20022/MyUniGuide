import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the DataFrame with the program links
df = pd.read_csv('C:/Users/nacho/PycharmProjects/MyUniGuide/data/OUINFO_Scrape_data.csv')  # Adjust filename if necessary

# List to store all extracted program details
all_program_details = []

# Iterate through each program in the DataFrame
for index, row in df.iterrows():
    program_name = row['Program Name']
    program_link = row['Program Link']

    print(f"Processing program: {program_name} - {program_link}")

    # Send a GET request to the program page
    response = requests.get(program_link)
    if response.status_code != 200:
        print(f"Failed to access program page: {program_link}. HTTP Status code: {response.status_code}")
        continue

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the "Program Summary" section
    program_summary_section = soup.find('div', class_='tabbed-section')

    # If the program summary section is missing, skip this program
    if not program_summary_section:
        print(f"No program summary section found for: {program_name}")
        continue

    # Extract key-value pairs from the "Program Summary"
    program_details = {'Program Name': program_name}  # Add the program name from the CSV
    items = program_summary_section.find_all(['dt', 'dd'])

    # Iterate through <dt> (keys) and <dd> (values)
    for i in range(0, len(items), 2):
        key = items[i].text.strip()  # Get the <dt> content
        value = items[i + 1].text.strip()  # Get the <dd> content
        program_details[key] = value

    # Filter only the required fields and add them to the list
    required_fields = [
        "Program Name",
        "University",
        "Degree",
        "Grade Range",
        "Experiential Learning",
        "Enrollment",
        "Instruction Language"
    ]
    filtered_details = {key: program_details.get(key, "N/A") for key in required_fields}
    all_program_details.append(filtered_details)

# Create a DataFrame from the collected program details
all_programs_df = pd.DataFrame(all_program_details)

all_programs_df.to_csv('OUINFO_Total_Scrape.csv', index=False)

print("All program details have been saved")
