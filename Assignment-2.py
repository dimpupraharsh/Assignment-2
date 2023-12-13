#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 21:02:20 2023

@author: Praharsh Vijay
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy.stats as stats


def data_cleaning(filename):
    """
       create a function , clean the data, transpose the data

       Parameters:
       - filename (str): The path to the CSV file containing data.

       Returns:
       - data  (pd.DataFrame): DataFrame with country as column.     
       - data_describe  (pd.DataFrame): stattical method using describe()    
       - data_countries (pd.DataFrame): DataFrame with country as column.
       - data_years (pd.DataFrame): DataFrame with year as column.
    """
    data = pd.read_csv(filename)
    # Copy the data
    copy_data = data.copy()
    data_countries = copy_data.drop(["Indicator"], axis=1).dropna().fillna(0)
    data_years = data_countries.transpose()
    data_describe = data.describe()
    return data_describe, data, data_countries, data_years


def urban_population(data, countries, indicator_name, years):
    ''' Create a function to acheive a line plot to visualize Urban population
        for top 6 economies over 2 decades using groupby method

    Parameters:
    - data : The input DataFrame containing data.
    - countries : A list of country names to be selected in the plot.
    - indicator_name : A list of indicator names to filter the data.
    - years : A list of years to include in the plot.'''

    # Filter the data for the selected countries, Indicators and years
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years].fillna(0)

    # Convert values to millions
    for year in years:
        data_filtered[year] = data_filtered[year] / 1e7

     # Grouping by Country Name and adding the values for each year
    data_arrange = data_filtered.groupby('Country Name').sum().reset_index()

    # Prepare the DataFrame to make it suitable for plotting
    data_prepared = data_arrange.melt(
        id_vars='Country Name', var_name='Year', value_name='Urban Population')

    # Create a Line plot
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid", palette="bright")
    sns.barplot(x='Year', y='Urban Population',
                hue='Country Name', data=data_prepared)

    # Add Title & Labels
    plt.title('Urban Population in last two Decades ')
    plt.xlabel('Year')
    plt.ylabel('Urban Population in Millions')

    # Add Rotation
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')

    # Format the y-axis in billions
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f'{x:.0f}M'))

    # Add Legends
    plt.legend(title='', loc="upper left")

    # Show the Plot
    plt.show()
    return


def pie_emission(data, selected_countries, selected_indicator, years):
    """
    Filter the data based on selected countries, indicators, and years,
    then plot a pie chart based on the emission data.

    Parameters:
    - data : The input DataFrame containing emission data.
    - selected_countries : A list of country names to be selected.
    - selected_indicator : A list of indicator names to filter the data.
    - years: A list of years to include in the plot.
    """
    # Filter the data
    data_filtered = data[
        (data['Country Name'].isin(selected_countries)) &
        (data['Indicator'].isin(selected_indicator))
    ][['Country Name'] + years].fillna(0)

    data_filtered["Total Greenhouse emissions"] = data_filtered[years].sum(
        axis=1)
    emission_data = data_filtered.drop(years, axis=1)

    # Plot pie chart
    plt.figure(figsize=(10, 8))

    # Choose vibrant colors
    colors = ['#FF9999', '#FFD700', '#87CEFA', '#90EE90', '#FF6347', '#D3D3D3']

    plt.pie(
        emission_data['Total Greenhouse emissions'],
        labels=emission_data['Country Name'],
        autopct="%0.1f%%",
        pctdistance=0.9,
        startangle=140,
        explode=(0.01, 0, 0, 0, 0, 0),
        colors=colors
    )

    plt.title("Countries with the highest proportions of Greenhouse Gas emissions")

    # Show the Plot
    plt.show()
    return


def power_consumption(data, countries, indicator_name, years):
    '''function to create a line plot to visuailize the power consumption 
        for specific countries in selected years'''

    # Filter the data for the selected countries, Indicators and years
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years]

    # Preparing the DataFrame to make it suitable for plotting
    data_prepared = data_filtered.melt(id_vars=[
                                       'Country Name'], var_name='Year', 
        value_name='Electric power consumption (kWh per capita)')

    # Plotting
    plt.figure(figsize=(20, 8))
    sns.set(style="whitegrid", palette="bright")
    sns.lineplot(x='Year', y='Electric power consumption (kWh per capita)',
                 hue='Country Name', data=data_prepared, marker='o')

    # Add Title & Labels
    plt.title('Total Electric power consumption (kWh per capita)')
    plt.xlabel('Year')
    plt.ylabel('power consumption (kWh per capita)')

    # Add Legends
    plt.xticks(rotation=45)
    plt.legend(title='', loc="upper left")

    # Add Gridlines
    plt.grid(True)

    # Show the Plot
    plt.show()
    return


def renewable_energy(data, countries, indicator_name, years):
    ''' function to create a line plot to visualize Renewable energy gerneration
        for selected countries over specific years.

    Parameters:
    - data (DataFrame): The input DataFrame containing Renewable energy data.
    - countries (list): A list of country names to be selected in the plot.
    - indicator_name (list): A list of indicator names to filter the data.
    - years (list): A list of years to include in the plot.'''

    # Filter the data for the selected countries, Indicators and years
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years].fillna(0)

    # Convert values to billions
    for year in years:
        data_filtered[year] = data_filtered[year] / 1e9

    # Prepare the DataFrame to make it suitable for plotting
    data_prepared = data_filtered.melt(id_vars=[
                                       'Country Name'], var_name='Year',
                    value_name='Electricity production from renewable sources')

    # Create a Line plot
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid", palette="bright")
    sns.lineplot(x='Year', y='Electricity production from renewable sources',
                 hue='Country Name', data=data_prepared)

    # Add Title & Labels
    plt.title('Electricity production from renewable sources')
    plt.xlabel('Year')
    plt.ylabel('Electricity production (in Billions KWh)')

    # Add Rotation
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')

    # Format the y-axis in billions
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f'{x:.0f}B'))

    # Add Legends
    plt.legend(title='', loc="upper left")

    # Show the Plot
    plt.show()
    return


def skew(data, countries, indicator_name, years):
    """Calculates the centralised and normalised skewness """
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years]

    # Prepare the DataFrame to make it suitable for calculating skewness
    data_prepared = data_filtered.melt(
        id_vars=['Country Name'], var_name='Year', value_name='Emissions')
    dist = data_prepared["Emissions"]

    # calculates average and std, dev for centralising and normalising
    aver = np.mean(dist)
    std = np.std(dist)

    # now calculate the skewness
    value = np.sum(((dist - aver) / std)**3) / len(dist-2)
    print("skewness: Total greenhouse emissions for china from 1993-2020 is :",
          np.round(value, 6))
    return value


def kurtosis(data, countries, indicator_name, years):
    """ Calculates the centralised and normalised excess kurtosis . """

    # Filter the data for specific countries,Indicators & years
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years].fillna(0)

    # Prepare the DataFrame to make it suitable for calculating kurtosis
    data_prepare = data_filtered.melt(
        id_vars=['Country Name'], var_name='Year', value_name='Emissions')

    dist = data_prepare["Emissions"]
    # calculates average and std, dev for centralising and normalising
    aver = np.mean(dist)
    std = np.std(dist)

    # now calculate the kurtosis
    value = np.sum(((dist-aver) / std)**4) / len(dist-3) - 3.0

    print("kurtosis: Total greenhouse emissions for china from 1993-2020 is :",
          np.round(value, 6))

    return value


def fossil_fuel(data, countries, indicator_name, years):
    '''function to create a line plot to visualize the fossil fuel consumption
        of different countries for selected years'''

    # Filtering the data for the selected countries indicator and years
    data_filtered = data[(data['Country Name'].isin(countries)) & (
        data['Indicator'].isin(indicator_name))][['Country Name'] + years]

    # Prepare the DataFrame for plotting
    data_prepared = data_filtered.melt(
        id_vars=['Country Name'], var_name='Year', value_name=('fossil fuel'))

    # Create line plot
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid", palette="husl")
    sns.lineplot(x='Year', y=('fossil fuel'), hue='Country Name',
                 data=data_prepared, marker='o')

    # Add Title & Labels
    plt.title('Fossil Fuel Energy Consumption (% of Total)')
    plt.xlabel('Year')
    plt.ylabel('percentage of fossil fuel consumption')

    # Add rotation & legends
    plt.xticks(rotation=45)
    plt.legend(title='', loc="lower left")

    # Show the plot
    plt.show()

    return


def correlation_heatmap(data, country_name, indicators):
    ''' funtion to create a correlation heatmap of a selected country
        for specific years '''
    # Filter data
    data_filtered = data[(data['Country Name'] == country_name) & (
        data['Indicator'].isin(indicators))]

    # Drop non-numeric columns and transpose for correlation calculation
    numeric_data = data_filtered.drop(
        columns=['Indicator', 'Country Name']).transpose()
    numeric_data.columns = data_filtered['Indicator']

    # Calculate correlation matrix
    correlation_matrix = numeric_data.corr()

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='inferno', linewidths=.5)
    plt.title(f'Correlation Heatmap for {country_name}')

    # Show the Plot
    plt.show()

    return


if __name__ == '__main__':

    # Calling the world_bank_data function
    data_describe, data, data_countries, data_years = data_cleaning(
        "/Users/vijaym/Downloads/Dimpu UH/Assignment_data2.csv")

    # Specified years,countries,indicators for the urban Bar Plot
    years_for_plot = ['1999', '2002', '2005',
                      '2008', '2011', '2014', '2017', '2020']
    selected_countries = ['China', 'United States',
                          'India', 'Japan', "Germany", "United Kingdom"]
    selected_indicator = ["Urban population"]

    # Calling the function to plot the data for urban Bar Plot
    urban_population(data, selected_countries,
                     selected_indicator, years_for_plot)

    # Specified years,countries,indicators for the Line Plot
    years_for_plot = ['1993', '1996', '1999', '2002',
                      '2005', '2008', '2011', '2014', '2017', '2020']
    selected_countries = ['China', 'United States',
                          'India', 'Japan', "Germany", "United Kingdom"]
    selected_indicator = [
        "Total greenhouse gas emissions (kt of CO2 equivalent)"]

    # Calling the function to plot the data for Line plot
    pie_emission(data, selected_countries, selected_indicator, years_for_plot)
    # Specified years,countries,indicators for the Bar Plot [Power Consumption]
    years_for_plot = ['1993', '1996', '1999', '2002',
                      '2005', '2008', '2011', '2014', '2017', '2020']
    selected_countries = ['China', 'United States',
                          'India', 'Japan', "Germany", "United Kingdom"]
    selected_indicator = ["Electric power consumption (kWh per capita)"]

    # Calling the function to plot the data
    power_consumption(data, selected_countries,
                      selected_indicator, years_for_plot)

    # Specified years,countries,indicators for the line Plot
    years_for_plot = ['1993', '1996', '1999', '2002',
                      '2005', '2008', '2011', '2014', '2017', '2020']
    selected_countries = ['China', 'United States',
                          'India', 'Japan', "Germany", "United Kingdom"]
    selected_indicator = [
    "Electricity production from renewable sources, excluding hydroelectric (kWh)"]

    # Calling the function to plot
    renewable_energy(data, selected_countries,
                     selected_indicator, years_for_plot)
    # calling the function skew,kurtosis

    years_to_plot = ['1993', '1996', '1999', '2002',
                     '2005', '2008', '2011', '2014', '2017', '2020']
    selected_countries = ["China"]
    selected_indicator = [
        "Total greenhouse gas emissions (kt of CO2 equivalent)"]
    skew_value = skew(data, selected_countries,
                      selected_indicator, years_to_plot)
    kurtosis_value = kurtosis(data, selected_countries,
                              selected_indicator, years_to_plot)

    # Specified years,countries,indicators for the Plot
    years_for_plot = ['1993', '1996', '1999', '2002',
                      '2005', '2008', '2011', '2014', '2017', '2020']
    selected_countries = ['China', 'United States',
                          'India', 'Japan', "Germany", "United Kingdom"]
    selected_indicator = ["Fossil fuel energy consumption (% of total)"]

    # Calling the function to plot the data
    fossil_fuel(data, selected_countries, selected_indicator, years_for_plot)

    # Specified years,countries,indicators for the Plot
    indicators_of_interest = [
        "Urban population",
        "Electricity production from renewable sources, excluding hydroelectric (kWh)",
        "Electric power consumption (kWh per capita)",
        'PM2.5 air pollution, mean annual exposure (micrograms per cubic meter)',
        "Fossil fuel energy consumption (% of total)",
        "Total greenhouse gas emissions (kt of CO2 equivalent)"
    ]

    # calling the functions for heatmap
    correlation_heatmap(data, "Germany", indicators_of_interest)
    correlation_heatmap(data, "China", indicators_of_interest)
    correlation_heatmap(data, "United States", indicators_of_interest)
