import time
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Function to collect route names and links from the current page
def collect_routes_from_page(driver):
    route_names = []
    route_links = []
    routes = driver.find_elements(By.XPATH, "//a[@class='route']")
    for route in routes:
        route_names.append(route.get_attribute('title'))
        route_links.append(route.get_attribute('href'))
    return route_names, route_links

# Function to extract bus details
def extract_bus_details(driver, route_name, wait):
    bus_details_list = []

    # Wait for bus details to load
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "bus-item")]')))

    bus_items = driver.find_elements(By.XPATH, '//div[contains(@class, "bus-item")]')

    for bus_item in bus_items:
        try:
            bus_name = bus_item.find_element(By.XPATH, './/div[contains(@class, "travels")]').text.strip()
        except:
            bus_name = 'N/A'

        try:
            bus_type = bus_item.find_element(By.XPATH, './/div[contains(@class, "bus-type")]').text.strip()
        except:
            bus_type = 'N/A'

        try:
            start_journey = bus_item.find_element(By.XPATH, './/div[contains(@class, "dp-time")]').text.strip()
        except:
            start_journey = 'N/A'

        try:
            end_journey = bus_item.find_element(By.XPATH, './/div[contains(@class, "bp-time")]').text.strip()
        except:
            end_journey = 'N/A'

        try:
            duration = bus_item.find_element(By.XPATH, './/div[contains(@class, "dur")]').text.strip()
        except:
            duration = 'N/A'

        try:
            price = bus_item.find_element(By.XPATH, './/div[contains(@class, "fare")]//span[contains(@class, "f-19 f-bold")]').text.strip()
        except:
            price = 'N/A'

        try:
            rating = bus_item.find_element(By.XPATH, './/div[contains(@class, "rating")]//span').text.strip()
        except:
            rating = 'N/A'

        try:
            seat_availability = bus_item.find_element(By.XPATH, './/div[contains(@class, "seat-left")]').text.strip()
        except:
            seat_availability = 'N/A'

        bus_details = {
            "Bus Name": bus_name,
            "Bus Type": bus_type,
            "Start of Journey": start_journey,
            "End of Journey": end_journey,
            "Duration": duration,
            "Price": price,
            "Star Rating": rating,
            "Seat Availability": seat_availability,
            "Route Name": route_name
        }

        bus_details_list.append(bus_details)

    return bus_details_list

# Initialize the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open the desired URL
driver.get("https://www.redbus.in/online-booking/astc")

# Define WebDriverWait
wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed

# Wait for the pagination container element
pagination_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'DC_117_paginationTable')))

# Find all page number elements
page_elements = pagination_container.find_elements(By.XPATH, '//div[contains(@class, "DC_117_pageTabs")]')

# Determine the number of pages
num_pages = len(page_elements)

all_route_names = []
all_route_links = []

# Iterate through each page
for page in range(1, num_pages + 1):
    # Construct XPath for the current page button
    xpath_expression = f'//div[contains(@class, "DC_117_pageTabs") and contains(text(), "{page}")]'

    # Find the page button
    page_button = pagination_container.find_element(By.XPATH, xpath_expression)

    # Scroll to the page button and click it
    actions = ActionChains(driver)
    actions.move_to_element(page_button).perform()
    time.sleep(1)  # Optional: Short delay for scrolling into view
    page_button.click()

    # Wait for the new page to load
    time.sleep(3)  # Adjust this delay based on how long it takes for the page to load

    # Collect routes from the current page
    route_names, route_links = collect_routes_from_page(driver)
    all_route_names.extend(route_names)
    all_route_links.extend(route_links)

# Container for all bus details
all_bus_details = []

# Process each URL with its corresponding route name
for url, route_name in zip(all_route_links, all_route_names):
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)

    # Click all "View Buses" buttons
    try:
        view_buses_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='button' and contains(text(),'View Buses')]"))
        )

        for button in reversed(view_buses_buttons):
            try:
                driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", button)
                time.sleep(1)
                button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error clicking button: {e}")
                continue
    except Exception as e:
        print(f"Error during 'View Buses' button processing: {e}")

    # Scroll to the bottom of the page multiple times to ensure all buses are loaded
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract bus details after all content is loaded
    try:
        bus_details = extract_bus_details(driver, route_name, wait)
        all_bus_details.extend(bus_details)
    except Exception as e:
        print(f"Error extracting bus details for route {route_name}: {e}")

# Close the browser
driver.quit()

# Convert bus details to a DataFrame and remove duplicates
df = pd.DataFrame(all_bus_details).drop_duplicates(subset=["Bus Name", "Route Name"])

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Display the DataFrame
print(df.head())

# Database connection details
user = 'root'
password = 'Digi08@Life'
host = 'localhost'
database = 'capstone1_redbus'

# Connect to the MySQL database
conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS ASTC_Bus_Details(
    Bus_Name VARCHAR(100),
    Bus_Type VARCHAR(100),
    Start_of_Journey VARCHAR(100),
    End_of_Journey VARCHAR(100),
    Duration VARCHAR(100),
    Price INT,
    Star_Rating FLOAT,
    Seat_Availability VARCHAR(100),
    Route_Name VARCHAR(100)
)
"""
cursor.execute(create_table_query)

# Insert data into the table
for index, row in df.iterrows():
    try:
        insert_query = """
        INSERT INTO ASTC_Bus_Details (
            Bus_Name, Bus_Type, Start_of_Journey, End_of_Journey, Duration, Price, Star_Rating, Seat_Availability, Route_Name
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        price = int(row["Price"].replace(",", "")) if row["Price"] not in ['N/A', ''] else None
        if isinstance(price, float):
            price = int(price)
        
        star_rating = float(row["Star Rating"]) if row["Star Rating"] not in ['N/A', ''] else None
        
        cursor.execute(insert_query, (
            row["Bus Name"], row["Bus Type"], row["Start of Journey"], row["End of Journey"], row["Duration"],
            price, star_rating,
            row["Seat Availability"], row["Route Name"]
        ))
    except ValueError as e:
        print(f"Error inserting row {index}: {e}")

# Commit and close the connection
conn.commit()
conn.close()