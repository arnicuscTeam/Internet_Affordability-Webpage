import os
import numpy as np
import pandas as pd


def clean_fcc_cost_data(data_dir: str):
    
    """
    This function cleans the FCC cost data
    :param data_dir: The directory where the data is stored
    :return: None
    """
    
    file_path = data_dir + "cost_data/2024_urs_broadband_website_data 2023-12-26.xlsx"
    clean_final_file_path = data_dir + "cost_data/cleaned_cost_data.csv"
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    if os.path.exists(clean_final_file_path):
        return None
    
    # Read in the data
    cost_data = pd.read_excel(file_path, sheet_name = "Data")
    
    # Drop the Model Data column
    cost_data.drop(columns = "Model Data", inplace = True)
    
    # Save the cleaned data
    cost_data.to_csv(clean_final_file_path, index = False)
    
    return None


def get_possible_values(data_dir: str, column: str) -> list:
    
    """
    This function gets the possible values for a given column.
    :param data_dir: The path to the data directory.
    :param column: The column for which the possible values are being found.
    :return: A list of possible values for the column.
    """
    
    # Read in the data
    cost_data = pd.read_csv(data_dir + "cost_data/cleaned_cost_data.csv")
    
    # Get the possible values
    possible_values = cost_data[column].unique()
    
    return possible_values


def collect_min_price(data_dir: str, state: str, tech: str, down_speed, up_speed, usage_allowance: str) -> float:
    
    """
    This function selects the plans based on the given parameters.
    :param data_dir: The directory where the data is stored.
    :param state: The state for which the plans are being selected.
    :param tech: The technology of the plans.
    :param down_speed: The download speed of the plans.
    :param up_speed: The upload speed of the plans.
    :param usage_allowance: The usage allowance of the plans.
    :return: Lowest price of filtered plans.
    """
    
    # If usage allowance is 0, set it to infinity
    if usage_allowance == 0:
        usage_allowance = np.inf
    
    # Read in the data
    cost_data = pd.read_csv(data_dir + "cost_data/cleaned_cost_data.csv")
    
    # Filter the data
    if usage_allowance == np.inf:
        cost_data = cost_data[(cost_data["State"] == state) & (cost_data["Technology"] == tech) &
                              (cost_data["Download Bandwidth Mbps"] >= down_speed) & (
                                          cost_data["Upload Bandwidth Mbps"] >= up_speed) &
                              (cost_data["Usage Allowance GB"] == np.inf)]
    else:
        cost_data = cost_data[(cost_data["State"] == state) & (cost_data["Technology"] == tech) &
                              (cost_data["Download Bandwidth Mbps"] >= down_speed) & (
                                          cost_data["Upload Bandwidth Mbps"] >= up_speed) &
                              (cost_data["Usage Allowance GB"] >= usage_allowance)]
    
    # Find the lowest price
    lowest_price = cost_data["Total Charge"].min()
    
    return lowest_price
