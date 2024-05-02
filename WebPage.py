import numpy as np
import pandas as pd
import streamlit as st
from Code.Cost_Data.cost_data import get_possible_values, collect_min_price
from Code.acs_pums.acs_pums import filter_pums_data, calc_average_income


# Set page name
st.set_page_config(
        page_title = 'Estimating Percentage Of Income Spent On Internet Service', page_icon = ':bar_chart:',
        layout = 'wide', initial_sidebar_state = 'expanded', )

st.cache_data.clear()

# Set page title
st.header('Estimating Percentage Of Income Spent On Internet Service')

st.text("")

st.text("")

# table_data = [
#     ["Medicaid, Medical Assistance, or any kind of government-assistance plan for those with low incomes or a "
#      "disability", "HINS4"],
#     ["Yearly food stamp/Supplemental Nutrition Assistance Program (SNAP)", "FS"],
#     ["Public assistance income over the past 12 months (any amount)", "PAP"],
#     ["Supplemental Security Income over the past 12 months (any amount)", "SSIP"]
#     ]
#
# # Create an HTML table
# table_html = ("<table style='border-collapse: collapse; width: 100%; border: 1px solid #ccc; background-color: "
#               "transparent;'>")
# table_html += "<tr style='background-color: transparent;'>"
# table_html += ("<th style='border: 1px solid #ccc; padding: 8px; text-align: left; background-color: transparent;'>ACS "
#                "Variable Description</th>")
# table_html += ("<th style='border: 1px solid #ccc; padding: 8px; text-align: left; background-color: "
#                "transparent;'>Variable name</th>")
# table_html += "</tr>"
#
# for row in table_data:
#     table_html += "<tr>"
#     table_html += f"<td style='border: 1px solid #ccc; padding: 8px;'>{row[0]}</td>"
#     table_html += f"<td style='border: 1px solid #ccc; padding: 8px;'>{row[1]}</td>"
#     table_html += "</tr>"
#
# table_html += "</table>"

# Display the HTML table
# st.markdown(table_html, unsafe_allow_html = True)

st.text("")
st.text("")

data_directory = "Data/"

# List of geographies
states = get_possible_values(data_directory, "State")
states.remove("PUERTO RICO")

techs = get_possible_values(data_directory, "Technology")
techs.append("All Technologies")

down_speeds = get_possible_values(data_directory, "Download Bandwidth Mbps")
up_speeds = get_possible_values(data_directory, "Upload Bandwidth Mbps")
usage_allowances = get_possible_values(data_directory, "Usage Allowance GB")

# Collect the states
state = st.selectbox('Select State', states)

# Collect the technology
tech = st.selectbox('Select Technology', techs)

# Collect the min download speed
down_speed = st.slider('Select Minimum Download Speed', min_value = 0, max_value = 500)

# Collect the min upload speed
up_speed = st.slider('Select Minimum Upload Speed', min_value = 0, max_value = 500)

# Collect the min usage allowance
usage_allowance = st.slider('Select Minimum Usage Allowance (0 for unlimited)', min_value = 0, max_value = 1000)

# Demographic Criteria
st.subheader('Sub-Populations')

# Checkboxes for demographic criteria, turned into integers
aian = int(st.checkbox('American Indian or Alaska Native'))
asian = int(st.checkbox('Asian'))
black = int(st.checkbox('Black or African American'))
nhpi = int(st.checkbox('Native Hawaiian or Other Pacific Islander'))
white = int(st.checkbox('White'))
hispanic = int(st.checkbox('Hispanic or Latino'))
veteran = int(st.checkbox('Veteran'))
elderly = int(st.checkbox('Elderly'))
disability = int(st.checkbox('Disability'))
not_eng_very_well = int(st.checkbox('Does Not Speak English Very Well'))

bottom_text = True

df = pd.DataFrame()

# Submit button
st.text("")
if st.button('Run Query'):
    
    price, technology = collect_min_price(data_directory, state, tech, down_speed, up_speed, usage_allowance)
    
    if price is None:
        st.write('No plans found for the selected criteria.')
        
    else:
    
        st.write(f'The lowest price for the selected plan is ${price} for {technology}.')
        st.text("")
        
        if aian or asian or black or nhpi or white or hispanic or veteran or elderly or disability or not_eng_very_well:
            
            results = filter_pums_data(
                    data_directory, state, aian, asian, black, nhpi, white, hispanic, veteran, elderly,
                    disability, not_eng_very_well
                    )
            for key, value in results.items():
                
                st.write(f'The average monthly income for {key} is ${round(value, 2)}.')
                st.write(f'The percentage of income spent on the selected plan for {key} is'
                         f' {round((price / value) * 100, 2)}%.')
                
                st.text("")
                st.text("")
                
        else:
        
            results = filter_pums_data(data_directory, state, aian, asian, black, nhpi, white, hispanic, veteran,
                                       elderly, disability, not_eng_very_well)
            
            st.write(f'The average monthly income for the total population is ${round(results["Total Population"], 2)}.')
            st.write(f'The percentage of income spent on the selected plan for the total population is'
                     f' {round((price / results["Total Population"]) * 100, 2)}%.')
            
            st.text("")
            st.text("")

if bottom_text:
    
    for i in range(10):
        st.text("")
    
    st.markdown(
            "<span style='font-size: 14px;'>This tool was developed by a team at the University of Southern "
            "California led by [Prof. Hernan Galperin](https://annenberg.usc.edu/faculty/hernan-galperin) and ["
            "Prof. François Bar](https://annenberg.usc.edu/faculty/fran%C3%A7ois-bar), with research assistance "
            "from Angel Chavez-Penate.</span>", unsafe_allow_html = True
            )
