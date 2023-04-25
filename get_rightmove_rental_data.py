# %% Acquire property value and rental value information from Rightmove
#
# Inputs: .txt file of Rightmove location identifiers
#
# Outputs: Property value and rental value data as .json
#
# Script developed by Jake Kolliari

# %% Import libraries

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import random
import numpy as np

# %% User inputs

mode = "rent"           # Rent or buy
file_name = "london"    # Naming to use in output csv file

# %% Function to obtain data based on a dictionary of locations and location IDs

def get_rightmove_data(location_dict, mode = "buy", pages = 41, retries = 10):
    
    # Initialise lists for storage of property information
    all_property_descriptions = []
    all_property_addresses = []
    all_property_areas = []
    all_property_monthly_rentals = []
    all_property_type = []
    all_property_num_bedrooms = []
    all_property_num_bathrooms = []
    all_property_size = []
    all_property_rental_date = []
    all_property_deposit = []
    all_property_min_tenancy = []
    all_property_let_type = []
    all_property_furnish_type = []
    all_property_ns1 = []
    all_property_nsd1 = []
    all_property_ns2 = []
    all_property_nsd2 = []
    all_property_ns3 = []
    all_property_nsd3 = []
    all_property_latitude = []
    all_property_longitude = []
    all_property_urls = []

    # Select location ids individually
    for location in location_dict:
        
        # Set up page index to track page numbers
        page_index = 0
        
        # Print progress update
        print(f"Obtaining data for {location}")
        
        # Loop through each page (max is currently 42 pages)
        for page_number in range(min(41,pages)):
            
            # Set-up user header
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
            
            # Create page URL based on mode (sale/buy), page number and location
            mode = mode if mode == "rent" else "sale"
            if page_index == 0:
                rightmove_url = f"https://www.rightmove.co.uk/property-for-{mode}/find.html?locationIdentifier=REGION%{location_dict[location]}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="  
            elif page_index != 0:
                rightmove_url = f"https://www.rightmove.co.uk/property-for-{mode}/find.html?locationIdentifier=REGION%{location_dict[location]}&sortType=6&index={page_index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            # Get webpage with list of properties
            for n in range(retries):
                try:
                    res = requests.get(rightmove_url, headers=headers)
                    res.raise_for_status()
                    break
                except HTTPError as exc:
                    print(exc)
                    time.sleep(n)
                    continue
                    
            soup = BeautifulSoup(res.text, "html.parser")
            
            # Get list of property listings on page 
            page_listings = soup.find_all("div", class_ ="l-searchResult is-list")
            
            # Get number of listings
            number_of_listings = int(soup.find("span", {"class": "searchHeader-resultCount"}).get_text().replace(",", ""))       

            # Loop through each property listing
            for listing_no in range(len(page_listings)):
                
                # Get listing and information
                listing = page_listings[listing_no]
                listing_info = listing.find("a", class_="propertyCard-link")
                
                # Listing url
                listing_link = "https://www.rightmove.co.uk" + listing_info.attrs["href"]
                all_property_urls.append(listing_link)
                
                # Listing description
                listing_desc = listing_info.find("h2", class_="propertyCard-title").get_text().strip()
                all_property_descriptions.append(listing_desc)

                # Listing address and postcode
                listing_address = listing_info.find("address", class_="propertyCard-address").get_text().strip()
                all_property_addresses.append(listing_address)
                all_property_areas.append(location)
                
                # Listing price
                listing_price = listing.find("span", class_="propertyCard-priceValue").get_text().strip()
                all_property_monthly_rentals.append(listing_price)
                
                # "Click" on property for additional information
                for n in range(retries):
                    try:
                        property_res = requests.get(listing_link, headers=headers)
                        property_res.raise_for_status()
                        break
                    except HTTPError as exc:
                        print(exc)
                        time.sleep(n)
                        continue
               
                soup = BeautifulSoup(property_res.text, "html.parser")
                
                # Get overview details
                listing_overview_titles = soup.find_all("div", class_ = "IXkFvLy8-4DdLI1TIYLgX")
                listing_overview_details = soup.find_all("div", class_ = "_3OGW_s5TH6aUqi4uHum5Gy")
                listing_overview_args = [arg.dt.get_text().lower() for arg in listing_overview_titles]
                
                property_type = listing_overview_details[listing_overview_args.index('property type')].get_text() if 'property type' in listing_overview_args else np.nan
                all_property_type.append(property_type)
                num_bedrooms = listing_overview_details[listing_overview_args.index('bedrooms')].get_text() if 'bedrooms' in listing_overview_args else np.nan
                all_property_num_bedrooms.append(num_bedrooms)
                num_bathrooms = listing_overview_details[listing_overview_args.index('bathrooms')].get_text() if 'bathrooms' in listing_overview_args else np.nan
                all_property_num_bathrooms.append(num_bathrooms)
                property_size = listing_overview_details[listing_overview_args.index('size')].get_text() if 'size' in listing_overview_args else np.nan
                all_property_size.append(property_size)

                # Get additional information
                listing_additional_info = soup.find_all("div", class_ = "_2RnXSVJcWbWv4IpBC1Sng6")
                listing_additional_info_args = [additional_info.dt.get_text().lower().replace(': ', '') for additional_info in listing_additional_info]
                
                available_date = listing_additional_info[listing_additional_info_args.index('let available date')].dd.get_text() if 'let available date' in listing_additional_info_args else np.nan
                all_property_rental_date.append(available_date)
                deposit_val = listing_additional_info[listing_additional_info_args.index('deposit')].dd.get_text().split("A deposit provides")[0] if 'deposit' in listing_additional_info_args else np.nan
                all_property_deposit.append(deposit_val)
                min_tenancy = listing_additional_info[listing_additional_info_args.index('min. tenancy')].dd.get_text() if 'min. tenancy' in listing_additional_info_args else np.nan
                all_property_min_tenancy.append(min_tenancy)
                let_type = listing_additional_info[listing_additional_info_args.index('let type')].dd.get_text() if 'let type' in listing_additional_info_args else np.nan
                all_property_let_type.append(let_type)
                furnish_type = listing_additional_info[listing_additional_info_args.index('furnish type')].dd.get_text() if 'furnish type' in listing_additional_info_args else np.nan
                all_property_furnish_type.append(furnish_type)
                
                # Up to 3 nearest train stations
                nearest_stations = soup.find_all("div", class_ = "mlEuHXZpfrrzJtwlRmwBe")
                num_nearest_stations = len(nearest_stations)
                
                ns1 = nearest_stations[0].get_text("///").split("///")[0] if num_nearest_stations >=1 else np.nan
                all_property_ns1.append(ns1)
                nsd1 = nearest_stations[0].get_text("///").split("///")[1] if num_nearest_stations >=1 else np.nan
                all_property_nsd1.append(nsd1)
                ns2 = nearest_stations[1].get_text("///").split("///")[0] if num_nearest_stations >=2 else np.nan
                all_property_ns2.append(ns2)
                nsd2 = nearest_stations[1].get_text("///").split("///")[1] if num_nearest_stations >=2 else np.nan
                all_property_nsd2.append(nsd2)
                ns3 = nearest_stations[2].get_text("///").split("///")[0] if num_nearest_stations >=3 else np.nan
                all_property_ns3.append(ns3)
                nsd3 = nearest_stations[2].get_text("///").split("///")[1] if num_nearest_stations >=3 else np.nan
                all_property_nsd3.append(nsd3)
                
                # Approximate location (lat/long)
                soup_str = str(soup)
                latitude = soup_str[soup_str.find("latitude")+10:].split(',')[0] if "latitude" in soup_str else np.nan
                all_property_latitude.append(latitude)
                longitude = soup_str[soup_str.find("longitude")+11:].split(',')[0] if "longitude" in soup_str else np.nan
                all_property_longitude.append(longitude)
            
            # Delay to avoid over-exhausting website
            time.sleep(random.randint(1, 3))
            
            # Add listings per page to page_index, and break if number of listings is exceeded
            print(f"{number_of_listings - page_index} listings left to go")
            page_index = page_index + 24
            if page_index >= number_of_listings:
                break
        
    # Convert data to a dataframe
    data = {
            "Address": all_property_addresses,
            "Area": all_property_areas,
            "Description": all_property_descriptions,
            "Monthly Rental": all_property_monthly_rentals,
            "Property Type": all_property_type,
            "Bedrooms": all_property_num_bedrooms,
            "Bathrooms": all_property_num_bathrooms,
            "Size": all_property_size,
            "Available Date": all_property_rental_date,
            "Deposit": all_property_deposit,
            "Min Tenancy": all_property_min_tenancy,
            "Let Type": all_property_let_type,
            "Furnish Type": all_property_furnish_type,
            "Nearest Station": all_property_ns1,
            "Nearest Station Dist": all_property_nsd1,
            "Second Nearest Station": all_property_ns2,
            "Second Nearest Station Dist": all_property_nsd2,
            "Third Nearest Station": all_property_ns3,
            "Third Nearest Station Dist": all_property_nsd3,
            "Latitude": all_property_latitude,
            "Longitude": all_property_longitude,
            "Url": all_property_urls
            }
    
    data = pd.DataFrame.from_dict(data)

    return data

# %% Function to process and save data obtained from rightmove
    
def process_rightmove_data(data, file_prename):
    
    # Process functions
    def process_price(x):
        if x!=x:
            x = np.nan
        elif '£' in x:
            x = int(x.replace(' ', '').replace(',', '').replace('£', '').replace('pcm', ''))
        else:
            x = np.nan
        return x

    # Process rooms
    def process_rooms(x):
        if x == x:
            x = int(x.replace('×',''))
        else:
            x = np.nan
        return x
    
    # Process size
    def process_size(x):
        if x == x:
            x = int(x.split('-')[0].split(' ')[0].replace(',',''))
        else:
            x = np.nan
        return x
    
    # Process date
    def process_date(x):
        if x!=x:
            x = np.nan
        elif 'ask agent' in x.lower():
            x = np.nan
        elif 'now' in x.lower():
            x = datetime.now().date()
        elif x == x:
            x = datetime.strptime(x, '%d/%m/%Y').date()
        return x
    
    # Process min tenancy
    def process_tenancy(x):
        if x == x:
            x = 'Unknown' if 'agent' in x else x
        else:
            x = np.nan
        return x
    
    # Process furnish type
    def process_type(x):
        if x == x:
            x = 'Flexible' if 'flexible' in x.lower() else x
            x = 'Unknown' if 'agent' in x else x
        else:
            x = np.nan
        return x
    
    # Process station distance
    def process_dist(x):
        if x!=x:
            x = np.nan
        elif 'miles' in x:
            x = float(x.replace(' ', '').replace('miles', ''))
        else:
            x = np.nan
        return x
    
    # Copy dataframe
    processed_data = data.copy(deep=False)
    
    # Remove irrelevant property types
    processed_data = processed_data[~processed_data['Property Type'].isin(['Character Property', 'Equestrian Facility', 'Flat Share', 'Garages', 'Hotel Room', 'House of Multiple Occupation', 'House Share', 'Land', 'Parking', 'Private Halls', 'Plot', 'Retirement Property'])]
    
    # Format data
    processed_data['Monthly Rental'] = processed_data['Monthly Rental'].apply(process_price)
    processed_data['Bedrooms'] = processed_data['Bedrooms'].apply(process_rooms)
    processed_data['Bathrooms'] = processed_data['Bathrooms'].apply(process_rooms)
    processed_data['Size'] = processed_data['Size'].apply(process_size)
    processed_data['Latitude'] = pd.to_numeric(processed_data['Latitude'], errors='coerce')
    processed_data['Longitude'] = pd.to_numeric(processed_data['Longitude'], errors='coerce')
    processed_data['Deposit'] = processed_data['Deposit'].apply(process_price)
    processed_data['Available Date'] = processed_data['Available Date'].apply(process_date)
    processed_data['Min Tenancy'] = processed_data['Min Tenancy'].apply(process_tenancy)
    processed_data['Furnish Type'] = processed_data['Furnish Type'].apply(process_type)
    processed_data['Nearest Station Dist'] = processed_data['Nearest Station Dist'].apply(process_dist)
    processed_data['Second Nearest Station Dist'] = processed_data['Second Nearest Station Dist'].apply(process_dist)
    processed_data['Third Nearest Station Dist'] = processed_data['Third Nearest Station Dist'].apply(process_dist)

    # Reset index
    processed_data.reset_index(inplace=True, drop = True)

    # Build file path
    file_path = f"data_directory/rental_data/{file_prename}-{str(datetime.now().date())}.csv"
    processed_data.to_csv(file_path)
    
    return processed_data


# %% Read in location ids

with open("rightmove_location_ids.txt") as f:
    location_dict = dict(x.rstrip().split(': ', 1) for x in f)

# %% Choose location_ids from dictionary and scrape data

location_dict_scrape = {k: location_dict[k] for k in list(location_dict.keys())}
data = get_rightmove_data(location_dict = location_dict_scrape, mode = mode, pages=15)

# %% Process data for consumption and save to file

processed_data = process_rightmove_data(data, file_prename = file_name)