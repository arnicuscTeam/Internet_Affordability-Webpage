import os
import numpy as np
import pandas as pd


def filter_pums_data(
        data_dir: str, state: str, aian: int = 0, asian: int = 0, black: int = 0, nhpi: int = 0, white: int = 0,
        hispanic: int = 0, veteran: int = 0, elderly: int = 0, disability: int = 0, not_eng_very_well: int = 0
        ) -> dict:
    
    """
    This function will filter the PUMS data based on the demographic criteria. It will return a dataframe with the data
    that meets the criteria.
    :param data_dir: The path to the data directory.
    :param state: The state name.
    :param aian: American Indian or Alaska Native.
    :param asian: Asian.
    :param black: Black or African American.
    :param nhpi: Native Hawaiian or Other Pacific Islander.
    :param white: White.
    :param hispanic: Hispanic or Latino.
    :param veteran: Veteran.
    :param elderly: Elderly.
    :param disability: Disability.
    :param not_eng_very_well: Does Not Speak English Very Well.
    :return: A dataframe with the data that meets the criteria.
    """
    
    state_mapping = {
        "ALABAMA": "al", "ALASKA": "ak", "ARIZONA": "az", "ARKANSAS": "ar", "CALIFORNIA": "ca",
        "COLORADO": "co", "CONNECTICUT": "ct", "DELAWARE": "de", "FLORIDA": "fl", "GEORGIA": "ga", "HAWAII": "hi",
        "IDAHO": "id", "ILLINOIS": "il", "INDIANA": "in", "IOWA": "ia", "KANSAS": "ks", "KENTUCKY": "ky",
        "LOUISIANA": "la", "MAINE": "me", "MARYLAND": "md", "MASSACHUSETTS": "ma", "MICHIGAN": "mi", "MINNESOTA": "mn",
        "MISSISSIPPI": "ms", "MISSOURI": "mo", "MONTANA": "mt", "NEBRASKA": "ne", "NEVADA": "nv", "NEW HAMPSHIRE": "nh",
        "NEW JERSEY": "nj", "NEW MEXICO": "nm", "NEW YORK": "ny", "NORTH CAROLINA": "nc", "NORTH DAKOTA": "nd",
        "OHIO": "oh", "OKLAHOMA": "ok", "OREGON": "or", "PENNSYLVANIA": "pa", "RHODE ISLAND": "ri",
        "SOUTH CAROLINA": "sc", "SOUTH DAKOTA": "sd", "TENNESSEE": "tn", "TEXAS": "tx", "UTAH": "ut", "VERMONT": "vt",
        "VIRGINIA": "va", "WASHINGTON": "wa", "WEST VIRGINIA": "wv", "WISCONSIN": "wi", "WYOMING": "wy"
        }
    
    state = state_mapping[state]
    
    covered_populations = [
        ("American Indian and Alaska Native", "aian"),
        ("Asian", "asian"),
        ("Black or African American", "black"),
        ("Native Hawaiian", "nhpi"),
        ("White", "white"),
        ("Hispanic or Latino", "hispanic"),
        ("Veteran", "veteran"),
        ("Elderly", "elderly"),
        ("DIS", "disability"),
        ("English less than very well", "not_eng_very_well")
        ]
    
    name_mapping = {
        "aian": "American Indian and Alaska Native",
        "asian": "Asian",
        "black": "Black or African American",
        "nhpi": "Native Hawaiian or Other Pacific Islander",
        "white": "White",
        "hispanic": "Hispanic or Latino",
        "veteran": "Veteran",
        "elderly": "Elderly",
        "disability": "People with a disability",
        "not_eng_very_well": "People who speak English less than very well"
        }
    
    state_data = data_dir + "ACS_PUMS/2022_Data/state_data/"
    
    state_file = state_data + state + "/" + state + "-eligibility-state.csv"
    
    if not os.path.exists(state_file):
        raise Exception("State file does not exist")
    
    df = pd.read_csv(state_file)
    
    results = {}
    
    for population_name, population_var in covered_populations:
    
        if locals()[population_var] == 1:
        
            pop_df = df[df[population_name] == 1]
            
            income = np.average(pop_df["HH Income"], weights = pop_df["WGTP"])
            
            col_name = name_mapping[population_var]
            
            results[col_name] = income / 12
    
    return results


def calc_average_income(filtered_df: pd.DataFrame) -> float:
    
    # Calculate the average for HH Income using WGTP as weights
    average_income = np.average(filtered_df["HH Income"], weights = filtered_df["WGTP"])
    
    return average_income / 12
