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

As homebuyers and renters spend time trawling through pages and pages of Rightmove listings they naturally tend to develop biases, identify trends, and formulate hypothesese about the property market. On average are properties in North London cheaper than those in South London? Is there a strong relationship between the distance of a property to the nearest tube station and the property value? To better understand the trends and peculiarities of the property market, it would be useful to have a large rental listing dataset available to investigate and analyse.

This repository aims to do just that, and contains a simple Python interface to extract property listing data from Rightmove. The tool enables the user to provide a list of regions/areas of interest and scrapes the relevant data from Rightmove, before preparing it for further analysis.

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
    │   │   ├── Tableau Dashboard - Renting a Property in London.png
    │   │   ├── Tableau Dashboard - Renting a Property in London - Filtered.png
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

This tool contains a function that uses these unique IDs to understand the regions that the user requires property listing data from. The function requires a dictionary of area names and corresponding IDs (where each key-value pair represents an area) as an input. For simplicity a text file is used to provide this information - **rightmove_location_ids.txt**. By default it contains the information required to extract Rightmove data for all London boroughs, but should be updated to complete alternative searches.

For example, to search for properties in Enfield, the user would update the text file to:<br>
```
Enfield: 5E93950
```

Or to search for properties in various areas surrounding Manchester, the user would update the text file to:<br>
```
Oldham: 5E1025
Salford: 5E1164
Trafford: 5E61424
```

With this in mind, the following steps should be taken to use the tool.
1. Clone this Git repository to an area on a local machine.
2. Search the [Rightmove website](https://www.rightmove.co.uk/) for areas/regions of choice, and copy the region unique identifier from the search URL.
3. Update **rightmove_location_ids.txt** to contain a list of the unique identifiers for search areas of choice.
4. Open **get_rightmove_rental_data.py** in a Python IDE of choice.
5. Ensure that the packages listed at the top of the script are installed locally.
6. Adjust the user inputs at the top of the script as required:
    * Set _mode_ to _buy_ to obtain sales listings, or _rent_ to obtain rental listings
    * Change _file_name_ to the desired name of the csv output file
7. Run the script

Note: Functionality for sales listings (_mode_=_buy_) is currently restricted. 

## Data Definition

**get_rightmove_rental_data.py** produces a csv output containing the following information

<ins>Rental Listing Data</ins>

* **Address:** Full address of property
* **Area:** Area/Region that the property is located in
* **Description:** Brief description of the property
* **Monthly Rental:** Monthly cost to rent property (£)
* **Property Type:** Type of property (E.g. Flat, Apartment, House, Duplex, etc.)
* **Bedrooms:** Number of bedrooms in property
* **Bathrooms:** Number of bathrooms in property
* **Size:** Total size of property (sqft)
* **Available Date:** Date from which the property is available to rent
* **Deposit:** Value of required deposit (£)
* **Min Tenancy:** Minimum required duration of tenancy (months)
* **Let Type:** Terms of rental (E.g. Short term, Long term, etc)
* **Furnish Type:** Status of furnishing (E.g. Furnished, Unfurnished, Part-furnished)
* **Nearest Station:** Name of nearest train/tube station
* **Nearest Station Dist:** Distance to nearest train/tube station (miles)
* **Second Nearest Station:** Name of second nearest train/tube station
* **Second Nearest Station Dist:** Distance to second nearest train/tube station (miles)
* **Third Nearest Station:** Name of third nearest train/tube station
* **Third Nearest Station Dist:** Distance to third nearest train/tube station (miles)
* **Latitude:** Property co-ordinates - latitude (deg)
* **Longitude:** Property co-ordinates - longitude (deg)
* **Url**: Rightmove URL of property listing

## Visualisation

Output data is in a format that can be readily imported into Tableau. To demonstrate just how valuable this data is, I have developed a Tableau dashboard to analyse and investigate the London rental market. The dashboard not only identifies market trends, but provides users with a quick and efficient mechanism to drill-through rental listings and find their next property.

The tool is available for use on [Tableau Public](https://public.tableau.com/app/profile/jake.kolliari/viz/RentingaPropertyinLondon/RentingaPropertyinLondon?publish=yes), and will be updated intermittently. 

<p align="center">
  <img width="90%" src="./data_directory/dashboard_images/Tableau Dashboard - Renting a Property in London.png">
</p>

## Legal

As per [Rightmove terms and conditions](https://www.rightmove.co.uk/this-site/terms-of-use.html) the use of webscrapers is not authorised by Rightmove, and therefore this package should no longer be used.

## References

[1] Low. B, "Scraping property listings from Rightmove." Medium. https://low-brandon96.medium.com/scraping-property-listings-from-rightmove-bd3cfb36516a (accessed 18th March 2023)
