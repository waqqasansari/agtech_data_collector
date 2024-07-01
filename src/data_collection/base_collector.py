import csv
from bs4 import BeautifulSoup
import requests
import os
import logging

logging.basicConfig(filename='data_collector.log', level=logging.INFO)

#Crop Data: Collect information on planted acres and yield forecasts.
class CropYieldDataCollector:
    def __init__(self, config, data_type, state):
        self.config = config  # Initialize with configuration data
        self.data_type = data_type  # Initialize with the type of data (e.g., 'planted_acres', 'fertilizer_sales')
        self.state = state
        self.csv_data = []  # Initialize an empty list to store CSV data
        logging.info(f"Initializing {data_type} DataCollector for {state}...")  # Log initialization information

    def parse_html(self, html_content):
        logging.info(f"Parsing HTML for {self.data_type}...")  # Log HTML parsing information
        # Parse HTML content and extract table data
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'border': '1'})
        headers = [th.text for th in table.find_all('th')]  # Extract headers from the table
        self.csv_data.append(headers)  # Add headers to the CSV data
        for row in table.find_all('tr', class_='datarow'):
            row_data = [td.text.strip() for td in row.find_all('td')]  # Extract row data
            if any(row_data):  # Only add non-empty rows to CSV data
                self.csv_data.append(row_data)

    def fetch_data(self, link):
        logging.info(f"Fetching {self.data_type} data for {self.state} from {link}...")  # Log data fetching information
        try:
            response = requests.get(link)  # Send HTTP GET request to fetch data from the provided link
            response.raise_for_status()  # Raise an exception for bad status codes
            self.parse_html(response.content)  # Parse fetched HTML content
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {self.data_type} data from {link}: {e}")  # Log error if fetching fails

    def write_to_csv(self, filename):
        logging.info(f"Writing {self.data_type} data to {filename}...")  # Log CSV writing information
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)  # Create a CSV writer
            csv_writer.writerows(self.csv_data)  # Write all CSV data to the CSV file
    
    def run(self):
        logging.info(f"Running {self.data_type} data collection for {self.state}...")  # Log data collection process start
        link = self.config['data_sources'][self.data_type][self.state][0]  # Get the link for the current state
        self.fetch_data(link)  # Fetch data for the current state
        # filename = self.config['output_files'][self.data_type][self.state]  # Get the output file name for the current state
        filename = os.path.join('D:/Stealth (B2B AI)/AGTECH/agtech_data_collector/data', self.config['output_files'][self.data_type][self.state])
        self.write_to_csv(filename)  # Write all fetched data to the specified CSV file
        logging.info(f"CSV file '{filename}' has been created successfully.")  # Log success message
        logging.info(f"File path: {os.path.abspath(filename)}")  # Log the absolute file path

    # def run(self):
    #     logging.info(f"Running {self.data_type} data collection for {self.state}...")  # Log data collection process start
    #     for link in self.config['data_sources'][self.data_type]:
    #         self.fetch_data(link)  # Fetch data for each link in the data sources
    #     self.write_to_csv(self.config['output_files'][self.data_type])  # Write all fetched data to the specified CSV file
    #     logging.info(f"CSV file '{self.config['output_files'][self.data_type]}' has been created successfully.")  # Log success message
    #     logging.info(f"File path: {os.path.abspath(self.config['output_files'][self.data_type])}")  # Log the absolute file path


class FertilizerSalesCollector:
    def __init__(self, config, state):
        self.config = config
        self.csv_data = []
        logging.info("Initializing Fertilizer Sales DataCollector...")

    def parse_html(self, html_content):
        logging.info("Parsing HTML for fertilizer sales...")
        # implementation specific to historical sales data of fertilizers
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        headers = [th.text for th in table.find_all('th')]
        self.csv_data.append(headers)
        for row in table.find_all('tr', class_='sales_row'):
            row_data = [td.text.strip() for td in row.find_all('td')]
            if any(row_data):  # Only add non-empty rows
                self.csv_data.append(row_data)

    def fetch_data(self, link):
        logging.info(f"Fetching fertilizer sales data from {link}...")
        try:
            response = requests.get(link)
            response.raise_for_status()  # Raise an exception for bad status codes
            self.parse_html(response.content)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching fertilizer sales data from {link}: {e}")

    def write_to_csv(self, filename):
        logging.info(f"Writing fertilizer sales data to {filename}...")
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(self.csv_data)

    def run(self):
        logging.info("Running fertilizer sales data collection...")
        for link in self.config['data_sources']['fertilizer_sales']:
            self.fetch_data(link)
        self.write_to_csv(self.config['output_files']['fertilizer_sales'])
        logging.info(f"CSV file '{self.config['output_files']['fertilizer_sales']}' has been created successfully.")
        logging.info(f"File path: {os.path.abspath(self.config['output_files']['fertilizer_sales'])}")