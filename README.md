# Redbus-Data-Scraping-with-Selenium-Dynamic-Filtering-using-Streamlit
Project Overview
The Redbus Ticket Booking System is a web application designed to facilitate the search and booking of bus tickets through a streamlined interface. This project leverages web scraping with Selenium, data storage in a MySQL database, and the development of a multipage Streamlit application for user interaction.

Features
Data Scraping with Selenium:

Utilizes Selenium to extract bus ticket details (such as Bus Name, Route Name, Price, Start/End of Journey, Duration, Star Rating, and Seat Availability) from the Redbus website.
Converts the scraped data into a structured format (DataFrame) using pandas for further processing.
Data Storage in SQL Database:

Stores the scraped bus ticket data into a MySQL database.
Creates a table (Bus_Details) to store information including Bus Name, Route Name, Bus Type, Price, Start/End of Journey timestamps, Duration, Star Rating, and Seat Availability.
Multipage Streamlit Application:

Page 1: Welcome and Introduction

Displays a welcoming interface using Lottie animations to introduce users to the application.
Provides an overview of the project, its purpose, and how to navigate through the application.
Page 2: Bus Search and Filtering

Allows users to select a Regional Transport Corporation (RTC) from a dropdown menu (e.g., APSRTC, KSRTC, WBTC).

Offers multiple filter options to refine search results:

Bus Route(s)
Bus Type(s)
Price Range (via slider)
Star Rating (via slider)
Seats Available (via slider)
Retrieves and displays filtered bus ticket details based on user-selected criteria from the SQL database.

Enables users to dynamically adjust filters and update results in real-time.

Setup Instructions
Prerequisites:

Ensure Python 3.x is installed.
Install necessary libraries using pip: selenium, pandas, mysql-connector-python, pymysql, streamlit, plotly, requests, streamlit_lottie.
Installation:

Clone the project repository from GitHub.
Set up a virtual environment (venv) and activate it.
Install dependencies using pip install -r requirements.txt.
Execution:

Run the Streamlit application by executing streamlit run app.py in the project directory.
Navigate to localhost:8501 in your web browser to access the application.
Project Structure
data_scraping/: Contains scripts for web scraping using Selenium (scrape_redbus.py).
database/: SQL database scripts (create_tables.sql) for initializing database schema.
streamlit_app/: Streamlit application files (app.py) implementing multipage functionality with Lottie animations and filtering features.
README.md: This file, providing an overview, setup instructions, and project details.
Dependencies
Python Libraries: selenium, pandas, mysql-connector-python, pymysql, streamlit, plotly, requests, streamlit_lottie.
Tools: ChromeDriver (for Selenium web scraping), MySQL database.
Authors
Manigandan M
