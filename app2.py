import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Weather EDA dashboard", page_icon=":bar_chart:", layout="wide")

# Directory where your CSV files are stored
csv_directory = 'data'

# List of years corresponding to the CSV files
years = [2016, 2017] #, 2018, 2019, 2020

# Initialize an empty list to store the DataFrames
dataframes = []

# Loop through each year, read the respective CSV, and add the year column
for year in years:
    # Construct the file name for each year
    file_path = os.path.join(csv_directory, f'cms_hospital_patient_satisfaction_{year}.csv')
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)
    
    # Add a column for the year
    df['Year'] = year
    
    # Append the DataFrame to the list
    dataframes.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# ---- SIDEBAR ----
st.sidebar.header("Please Select Variables Here:")

# Use multiselect to choose the variables you want to plot
variables = st.sidebar.multiselect(
    "Select Variables to Plot:",
    options=['Facility Name', 'City', 'State'],
    default=['Facility Name']  # Default to 'State'
)

# Use selectbox to choose the variable you want to plot
selected_variable = st.sidebar.selectbox(
    "Select Variable:",
    options=['City', 'State', 'Hospital Type', 'Hospital Ownership'],
    index=0  # Default to 'State'
)

# Radio button to select chart type (counts or pie chart)
chart_type = st.sidebar.radio(
    "Select Chart Type:",
    options=["Count (Bar Chart)", "Percentage (Pie Chart)"]
)

# MAIN PAGE
st.subheader(":bar_chart: Number of Facilities by Year (Total for Country or By State)")
st.markdown("##")

# Function to plot facilities by year and state (Count in Bar Chart)
def plot_facilities_by_year_state_count():
    facilities_by_year_state = combined_df.groupby(['Year', 'State'])['Facility Name'].nunique().reset_index()
    fig = px.bar(facilities_by_year_state, x='Year', y='Facility Name', color='State',
                 title='Number of Facilities by Year and State (Counts)',
                 labels={'Facility Name': 'Number of Facilities'})
    st.plotly_chart(fig)

# Function to plot facilities by year and state (Percentage in Pie Chart by Year)
def plot_facilities_by_year_state_percentage():
    # Loop through each year and create a pie chart for each one
    for year in combined_df['Year'].unique():
        facilities_by_year_state = combined_df[combined_df['Year'] == year].groupby(['State'])['Facility Name'].nunique().reset_index()
        total_facilities = facilities_by_year_state['Facility Name'].sum()
        
        # Calculate the percentage for each state within the year
        facilities_by_year_state['Percentage'] = (facilities_by_year_state['Facility Name'] / total_facilities) * 100
        
        # Create a pie chart
        fig = px.pie(facilities_by_year_state, names='State', values='Facility Name',
                     title=f'Percentage of Facilities by State in {year}',
                     labels={'Facility Name': 'Number of Facilities'},
                     hover_data=['Percentage'])
        st.plotly_chart(fig)


# Function to plot facilities by year, state, and city (Count in Bar Chart)
def plot_facilities_by_year_state_city_count():
    facilities_by_year_state_city = combined_df.groupby(['Year', 'State', 'City'])['Facility Name'].nunique().reset_index()
    fig = px.bar(facilities_by_year_state_city, x='Year', y='Facility Name', color='City',
                 title='Number of Facilities by Year, State, and City (Counts)',
                 labels={'Facility Name': 'Number of Facilities'})
    st.plotly_chart(fig)

# Function to plot facilities by year, state, and city (Percentage in Pie Chart)
def plot_facilities_by_year_state_city_percentage():
    facilities_by_year_state_city = combined_df.groupby(['Year', 'State', 'City'])['Facility Name'].nunique().reset_index()
    total_facilities = facilities_by_year_state_city['Facility Name'].sum()
    facilities_by_year_state_city['Percentage'] = (facilities_by_year_state_city['Facility Name'] / total_facilities) * 100
    fig = px.pie(facilities_by_year_state_city, names='City', values='Facility Name',
                 title='Percentage of Facilities by City',
                 labels={'Facility Name': 'Number of Facilities'},
                 hover_data=['Percentage'])
    st.plotly_chart(fig)

# Function to plot facilities by year (Country-wide) (Count in Bar Chart)
def plot_facilities_by_year_count():
    facilities_by_year = combined_df.groupby('Year')['Facility Name'].nunique().reset_index()
    fig = px.bar(facilities_by_year, x='Year', y='Facility Name',
                 title='Total Number of Facilities by Year (Country-wide - Counts)',
                 labels={'Facility Name': 'Number of Facilities'})
    st.plotly_chart(fig)

# Function to plot facilities by year (Country-wide) (Percentage in Pie Chart)
def plot_facilities_by_year_percentage():
    facilities_by_year = combined_df.groupby('Year')['Facility Name'].nunique().reset_index()
    total_facilities = facilities_by_year['Facility Name'].sum()
    facilities_by_year['Percentage'] = (facilities_by_year['Facility Name'] / total_facilities) * 100
    fig = px.pie(facilities_by_year, names='Year', values='Facility Name',
                 title='Percentage of Facilities by Year (Country-wide)',
                 labels={'Facility Name': 'Number of Facilities'},
                 hover_data=['Percentage'])
    st.plotly_chart(fig)

# Conditional rendering based on sidebar selection
if selected_variable == 'State':
    if chart_type == "Count (Bar Chart)":
        plot_facilities_by_year_state_count()
    else:
        plot_facilities_by_year_state_percentage()

elif selected_variable == 'City':
    if chart_type == "Count (Bar Chart)":
        plot_facilities_by_year_state_city_count()
    else:
        plot_facilities_by_year_state_city_percentage()

else:
    if chart_type == "Count (Bar Chart)":
        plot_facilities_by_year_count()
    else:
        plot_facilities_by_year_percentage()
