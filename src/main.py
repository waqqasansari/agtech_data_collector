import yaml
from data_collection.base_collector import CropYieldDataCollector, FertilizerSalesCollector


def main():
    # Open the config.yaml file in read mode and assign it to a file object 'f'
    with open('D:/Stealth (B2B AI)/AGTECH/agtech_data_collector/config/config.yaml', 'r') as f:
        # Load the YAML configuration from the file into a Python dictionary called 'config'
        config = yaml.safe_load(f)
    
    # Extract the state names from the 'planted_acres' section of the config dictionary
    # and store them in a list called 'states'
    states = list(config['data_sources']['planted_acres'].keys())
    
    # Iterate over each state in the 'states' list
    for state in states:
        # Create an instance of the CropYieldDataCollector class, passing in the config, data type, and state
        planted_acres_collector = CropYieldDataCollector(config, 'planted_acres', state)
        
        # Run the data collection process for the current state
        planted_acres_collector.run()

        # ↓↓↓↓↓ YOU CAN ADD MORE DATA SOURCE LIKE THIS ↓↓↓↓↓↓
        # Create an instance of the FertilizerSalesCollector class, passing in the config
        # fertilizer_sales_collector = FertilizerSalesCollector(config)
        
        # Run the data collection process for fertilizer sales
        # fertilizer_sales_collector.run()

# This is a guard clause to ensure the main function is only executed when the script is run directly
if __name__ == "__main__":
    # Call the main function to start the data collection process
    main()