# Property Value Analysis
This repository contains a simple Python interface to scrape rental listings from Rightmove and prepare data for further analysis and investigation.

## Contents

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction"> ➤ Introduction</a></li>
    <li><a href="#folder-structure"> ➤ Folder Structure</a></li>
    <li><a href="#usage-information"> ➤ Usage Information</a></li>
    <li><a href="#data-definition"> ➤ Data Definition</a></li>
    <li><a href="#visualisation"> ➤ Visualisation</a></li>
    <li><a href="#legal"> ➤ Legal</a></li>
    <li><a href="#references"> ➤ References</a></li>

</ol>
</details>

## Introduction

Rightmove is the UK's largest online real estate property portal, and is a constituent of the FTSE 100 Index. Rightmove is effectively a property marketplace, both in sales and rentals, that aims to make moving home easier.

As homebuyers and renters spend time trawling through pages and pages of Rightmove listings, they tend to naturally develop biases, identify trends, and formulate hypothesese about the property market with which they are concerned. Are properties in North London cheaper than those in South London on average? Is there a strong relationship between proximity of tube station and property value? To better understand the trends and peculiarities of the property market, it would be useful to have a large rental listing dataset available that one could investigate and analyse.

This repository aims to do just that, and contains a simple Python interface to extract property listing data from Rightmove. The tool enables the user to provide a list of regions/areas of interest, and scrapes the relevant data from Rightmove before preparing it for further analysis.

To demonstrate the value of using the tool to acquire property listing data, a Tableau dashboard that presents and analyses the London rental market has been provided.

## Folder Structure

The tree below (click drop-down to expand) presents the folder structure of this git repository. Note that some individual files are omitted from the diagram for simplicity.

<details>
<summary>Show folder structure</summary>


    property-value-analysis
    │
    ├── data_directory
    │   ├── dashboard_images
    │   │   ├── rightmove_logo.png
    │   │   ├── station_logo.png
    │   ├── rental_data [contains csvs of extracted data]
    │   ├── shape_files [contains London Borough shape files for Tableau visualisation]
    │   ├── station_locations
    │   │   ├── London stations.csv
    │ 
    ├── get_rightmove_rental_data.py
    │
    ├── rightmove_location_ids.txt
    │     
    ├── LICENSE 
    │ 
    ├── README.md 

</details>

## Usage Information

When manually searching for properties on Rightmove the user is asked to search for a specific area/region or postcode. In doing so, Rightmove embeds a unique identifier into the search URL. For example: when searching for properties in Enfield the Rightmove search URL contains the string _locationIdentifier=REGION%5E93950_, where _5E93950_ is the unique ID. 

The tool contains a function that uses these unique IDs to understand the regions that the user requires property listing data from. The function requires a dictionary of area names and corresponding IDs (where each key-value pair represents an area) as an input. For simplicity a text file is used to provide this information **rightmove_location_ids.txt**. By default it contains the information required to extract Rightmove data for all London boroughs, but should be updated to complete alternative searches.

For example, to search for properties in Enfield, the user would update the text file to:<br>
```
Enfield: 5E93950
```

Or to search for properties in various areas surrounding Manchester, the user would update the text file:<br>
```
Oldham: 5E1025
Salford: 5E1164
Trafford: 5E61424
```

With this in mind, the following steps should be taken to use the tool.
1. Clone this Git repository to an area on a local machine.
2. Search the [Rightmove website](https://www.rightmove.co.uk/) for areas/regions of choice, and copy the region unique identifier from the search URL.
3. Update **rightmove_location_ids.txt** to contain a list of the search areas of choice.
4. Open **get_rightmove_rental_data.py** in a Python IDE of choice.
5. Ensure that the required packages are installed.
6. Adjust the user inputs at the top of the script as required:
    * Set _mode_ to _buy_ to obtain sales listings, or _rent_ to obtain rental listings
    * Change _file_name_ to the desired name of the csv output file
7. Run the script

Note: Functionality for sales listings (_mode_=_buy_) is currently restricted. 



