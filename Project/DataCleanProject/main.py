# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
from Levenshtein import distance


def DetectAndFixingAddress():
    # Load data from CSV file
    df = pd.read_csv('building_V1.csv')

    # Detect Building_ID -> Address
    e0_violations = df.groupby('Building_ID')['Address'].nunique()

    # building_address_counts = df.groupby('Building_ID')['Address'].nunique().reset_index()
    # violations = building_address_counts[building_address_counts['Address'] > 1]

    e0_violations = e0_violations[e0_violations > 1]

    # print violations
    print("Violation of e0: Building_ID → Address:")
    print(e0_violations)

    #
    violation_pairs = pd.merge(df, df, on='Building_ID', suffixes=('_1', '_2'))
    violation_pairs = violation_pairs[(violation_pairs['Address_1'] != violation_pairs['Address_2'])]

    # Print the offending tuple pair
    print("Violation of e0: Building_ID → Address tuple pair:")
    print(violation_pairs[['Building_ID', 'Address_1', 'Address_2']])

    # Fixing Violations
    # As an example of frequency, select the most frequently occurring Building_ID for each Address
    # frequent_ids = df.groupby('Address')['Building_ID'].agg(lambda x: x.value_counts().idxmax())
    # print(violations)
    # df['Building_ID'] = df['Address'].map(frequent_ids)

    # Save the repaired data back to a CSV file
    # df.to_csv('fixed_data.csv', index=False)


def DetectAndFixingState():
    # read data
    df = pd.read_csv('building_V3.csv')

    # e1: Zip → State
    # Detection of e1 violation
    e1_violations = df.groupby('Zip')['State'].nunique()
    e1_violations = e1_violations[e1_violations > 1]

    # Print the Stat for each Zip violation
    # e Number
    # print("Violation of e1:Zip → State:")
    # print(e1_violations)

    # Get the list of Zip codes that violate the constraints
    violating_zips = e1_violations.index.tolist()

    # Printing violations of e1:Zip → State
    print("Violation of e1:Zip → State:")
    print(e1_violations)

    # Filtering out data that violates constraints
    violating_data = df[df['Zip'].isin(violating_zips)]

    # Grouping data for constraint violations by 'Zip' and 'State'
    violating_distribution = violating_data.groupby(['Zip', 'State']).size().reset_index(name='Count')

    # Output the ZIP codes that violate the constraints and their corresponding State distributions.
    print(violating_distribution.to_string(index=False))

    # Calculate the frequency of occurrence for each state
    state_counts = df['State'].value_counts(normalize=True)

    # Convert frequency of occurrence to weights (any logic can be added here to adjust the weights)
    weights = state_counts / state_counts.sum()

    print("=========================", weights)

    # Find the State with the most weight
    state_with_max_weight = weights.idxmax()

    # For records with an empty Zip, set the State with the most weights
    df.loc[df['Zip'].isnull(), 'State'] = state_with_max_weight

    # Sort the data within each zip code, descending according to Count and ascending according to weight (because in the case of juxtaposition, the higher the weight, the better)
    # This will put the states with the highest counts and the most weighted states in the same zip code at the top of the list
    violating_distribution['weight'] = violating_distribution['State'].map(weights)
    sorted_violations = violating_distribution.sort_values(by=['Zip', 'Count', 'weight'],
                                                           ascending=[True, False, False])

    # Remove states with smaller counts and keep only the states with the largest counts under each ZIP code (if tied, select the most heavily weighted)
    max_states = sorted_violations.drop_duplicates(subset=['Zip'])

    print("Violation of e1:Zip → State, and state of choice:")
    print(max_states)

    # Next, we find the state with the largest count for each zip code
    # max_states = violating_distribution.loc[violating_distribution.groupby(['Zip'])['Count'].idxmax()]

    print("++++++++++++++",max_states)

    # Create a mapping from zip codes to selected states
    state_map = max_states.set_index('Zip')['State'].to_dict()
    print("======================",state_map)

    # Before mapping, we first keep the State value where the original Zip is empty
    mask = df['Zip'].notnull() & df['Zip'].apply(str).str.strip().ne('')

    # Updating State Columns with Mapping
    df.loc[mask, 'State'] = df.loc[mask, 'Zip'].map(state_map)

    # df['State'] = df['Zip'].map(state_map)

    df.to_csv('building_V4.csv', index=False)

    # If you also want to see specific rows of violated data
    # if not e1_violations.empty:
    #    print("Data rows that violate the 'Zip → State' constraint:")
    #    print(e1_violations.to_string(index=False))

    # Find the most frequent State in each Zip.
    # frequent_states = df.groupby('Zip')['State'].agg(lambda x: x.value_counts().idxmax()).reset_index()

    # Update violation data based on the most frequent State
    # for index, row in frequent_states.iterrows():
    #    zip_code = row['Zip']
    #    most_frequent_state = row['State']
    #    print("Zip:",zip_code," Most_frequent_state:",most_frequent_state)

    # Fixing Violations
    # As an example of frequency, select the most frequently occurring Building_ID for each Address
    # frequent_ids = df.groupby('Address')['Building_ID'].agg(lambda x: x.value_counts().idxmax())
    # print(violations)
    # df['Building_ID'] = df['Address'].map(frequent_ids)

    # Save the repaired data back to a CSV file
    # df.to_csv('fixed_data.csv', index=False)


def DetectAndFixingCity():
    # read data
    df = pd.read_csv('building_V4.csv')

    # e2: Zip → City
    # Detection of e2 violation
    e2_violations = df.groupby('Zip')['City'].nunique()
    e2_violations = e2_violations[e2_violations > 1]

    # Print the number of City violations per Zip
    print("Violation of e2:Zip → City:")
    print(e2_violations)

    # Filtering out data that violates constraints
    violating_zips = e2_violations.index.tolist()
    violating_data = df[df['Zip'].isin(violating_zips)]

    # Grouping data for constraint violations by 'Zip' and 'City'
    violating_distribution = violating_data.groupby(['Zip', 'City']).size().reset_index(name='Count')

    # Calculate the frequency of occurrence for each city
    city_counts = df['City'].value_counts(normalize=True)

    # Convert frequency of occurrence to weights (any logic can be added here to adjust the weights)
    weights = city_counts / city_counts.sum()

    # Find the most weighted City
    city_with_max_weight = weights.idxmax()

    # For records with an empty Zip, set the City with the largest weight
    df.loc[df['Zip'].isnull(), 'City'] = city_with_max_weight

    # Sort the data within each zip code, descending according to Count and ascending according to weight (because in the case of juxtaposition, the higher the weight, the better)
    violating_distribution['Weight'] = violating_distribution['City'].map(weights)
    sorted_violations = violating_distribution.sort_values(by=['Zip', 'Count', 'Weight'],
                                                           ascending=[True, False, False])

    # Remove cities with smaller counts and keep only the cities with the largest counts under each ZIP code (if tied, select the most heavily weighted)
    max_cities = sorted_violations.drop_duplicates(subset=['Zip'])

    print("Violation of e2:Zip → City, and the selected city:")
    print(max_cities)

    # Create a mapping from zip codes to selected cities
    city_map = max_cities.set_index('Zip')['City'].to_dict()
    print(city_map)

    # Before mapping, we first keep the City value where the original Zip is empty
    mask = df['Zip'].notnull() & df['Zip'].apply(str).str.strip().ne('')

    # Updating City Columns with Mapping
    df.loc[mask, 'City'] = df.loc[mask, 'Zip'].map(city_map)

    # Update the 'City' column in the original dataframe
    # df['City'] = df['Zip'].map(city_map)

    # Save the corrected dataframe as a new CSV file
    df.to_csv('building_V5.csv', index=False)

def DetectAndFixingLocation():
    # read data
    df = pd.read_csv('building_V5.csv')

    # Detection of violations of e4 constraints
    e4_violations = df.groupby(['Latitude', 'Longitude'])['Location'].nunique()
    e4_violations = e4_violations[e4_violations > 1]
    print("e4_violations:",e4_violations.to_string())

    # Get a list of latitude and longitude combinations that violate the constraints, ensuring that null values are not included
    violating_coords  = e4_violations.index.tolist()
    # Filtering out data that violates constraints
    violating_data  = df.set_index(['Latitude', 'Longitude']).loc[violating_coords].reset_index()
    print("violating_data:",violating_data.to_string())

    # Grouping of constraint violation data by 'Latitude', 'Longitude' and 'Location'
    violating_distribution = violating_data .groupby(['Latitude', 'Longitude', 'Location']).size().reset_index(name='Count')

    # Assuming that we do not have an external system to verify the exact location corresponding to each pair of latitude and longitude, we can choose the Location with the most counts
    max_locations = violating_distribution.loc[violating_distribution.groupby(['Latitude', 'Longitude'])['Count'].idxmax()]

    print("max_locations:",max_locations.to_string())

    # Create a mapping from latitude and longitude to the selected location
    location_map_e4 = max_locations.set_index(['Latitude', 'Longitude'])['Location'].to_dict()
    print(location_map_e4)

    # Update the 'Location' column in the original dataframe
    for (lat, long), location in location_map_e4.items():
        mask = (df['Latitude'] == lat) & (df['Longitude'] == long)
        df.loc[mask, 'Location'] = location

    # For cases where latitude and longitude are null, if you have a default value or can get Location somehow, you can set it here
    # For example, you can leave it blank or set it to unknown
    # df.loc[df['Latitude'].isnull() | df['Longitude'].isnull(), 'Location'] = 'Unknown'  # 或者您的默认值

    # Save to new file
    df.to_csv('building_V6.csv', index=False)

def DetectAndFixingLocation2():
    df = pd.read_csv('building_V6.csv')
    df['Location'] = df.apply(lambda row: f"({row['Latitude']}, {row['Longitude']})", axis=1)

    # The 'Location' column will now contain a tuple with the format (Latitude, Longitude)
    # The next step is to deal with any data integrity issues, such as duplicate location information, etc.
    # ... (any desired data cleaning steps can be added here)

    # Save the modified DataFrame to a CSV file
    df.to_csv('building_V7.csv', index=False)

def DetectAndFixingAddressLocation():
    # read data
    df = pd.read_csv('building_V8.csv')

    # e3: Address → Location
    # First define Location as a combination of Latitude and Longitude.
    df['Location'] = list(zip(df['Latitude'], df['Longitude']))

    # Detection of violations of e3 constraints
    e3_violations = df.groupby('Address')['Location'].nunique()
    e3_violations = e3_violations[e3_violations > 1]

    # Output violation of e3 constraints
    print("violate e3: Address → Location data:")
    print(e3_violations)

    # Filtering out addresses that violate constraints
    violating_addresses = e3_violations.index.tolist()
    violating_data = df[df['Address'].isin(violating_addresses)]

    # Grouping data that violates constraints by 'Address' and 'Location'
    violating_distribution = violating_data.groupby(['Address', 'Location']).size().reset_index(name='Count')

    # Calculate the frequency of occurrence of each position
    location_counts = df['Location'].value_counts(normalize=True)

    # Convert frequency of occurrence to weights (any logic can be added here to adjust the weights)
    weights = location_counts / location_counts.sum()

    # Sort the data within each address, based on Count descending and weight ascending
    violating_distribution['Weight'] = violating_distribution['Location'].apply(lambda x: weights.get(x, 0))
    sorted_violations = violating_distribution.sort_values(by=['Address', 'Count', 'Weight'],
                                                           ascending=[True, False, False])

    # Remove locations with small counts and keep only the locations with the largest counts under each address (if tied, choose the one with the largest weight)
    max_locations = sorted_violations.drop_duplicates(subset=['Address'])
    print(max_locations)

    # Create a mapping from an address to a selected location
    location_map = max_locations.set_index('Address')['Location'].to_dict()
    print(location_map)

    # Updating the DataFrame
    for address, location in location_map.items():
        df.loc[df['Address'] == address, ['Latitude', 'Longitude']] = location

    # Saving corrected data
    # df.to_csv('building_V9.csv', index=False)

def clean_location(location):
    try:
        # Assuming that the format of the location is "(lat, lon)".
        lat, lon = location.replace('(', '').replace(')', '').split(',')
        # Formatted as a string with 6 decimal places
        return f"({float(lat):.6f}, {float(lon):.6f})"
    except Exception as e:
        print(f"Error processing location: {location} - {e}")
        # Handle errors, return the original string or consider returning a special value to indicate an error
        return location

def DetectAndFixingLocationCommunity():
    df = pd.read_csv('building_V8.csv')
    # Detection of e5 violation
    e5_violations = df.groupby(['Location', 'Community_Number'])['Community_Name'].nunique()
    e5_violations = e5_violations[e5_violations > 1]

    # Get a list of Location and Community_Number combinations that violate e5 constraints.
    violating_locs = e5_violations.index.tolist()

    # Screening out data that violates e5 constraints
    violating_data = df.set_index(['Location', 'Community_Number']).loc[violating_locs].reset_index()

    # Grouping of constraint violation data by 'Location', 'Community_Number' and 'Community_Name'
    violating_distribution = violating_data.groupby(
        ['Location', 'Community_Number', 'Community_Name']).size().reset_index(name='Count')

    # Calculate the frequency of occurrence of each community name
    community_name_counts = df['Community_Name'].value_counts(normalize=True)

    # Converting frequency of occurrence to weights
    weights = community_name_counts / community_name_counts.sum()

    # Find the Community_Name with the highest weight for each combination that violates the constraints
    def get_max_community_name(row, group_df):
        max_count = group_df['Count'].max()
        # Check if more than one Community_Name has the same maximum count
        if group_df[group_df['Count'] == max_count].shape[0] == 1:
            return group_df[group_df['Count'] == max_count]['Community_Name'].values[0]
        else:
            # If there is more than one Community_Name with the maximum count, use the weighting decision
            max_weight = group_df['Weight'].max()
            return group_df[group_df['Weight'] == max_weight]['Community_Name'].values[0]

    # Apply functions and create mappings
    community_name_map = {}
    for loc, group_df in violating_distribution.groupby(['Location', 'Community_Number']):
        group_df['Weight'] = group_df['Community_Name'].apply(lambda x: weights.get(x, 0))
        community_name_map[loc] = get_max_community_name(loc, group_df)

    # Update the 'Community_Name' column in the original data frame
    for (loc, comm_num), comm_name in community_name_map.items():
        mask = (df['Location'] == loc) & (df['Community_Number'] == comm_num)
        df.loc[mask, 'Community_Name'] = comm_name

    # Save the corrected dataframe as a new CSV file
    df.to_csv('building_V9.csv', index=False)


def DetectAndFixingLocationCommunity2():
    df = pd.read_csv('building_V10.csv')
    # Detection of e5 violation
    e5_violations = df.groupby(['Location', 'Community_Number'])['Community_Name'].nunique()
    e5_violations = e5_violations[e5_violations > 1]

    # Get a list of Location and Community_Number combinations that violate e5 constraints.
    violating_locs = e5_violations.index.tolist()

    # Screening out data that violates e5 constraints
    violating_data = df.set_index(['Location', 'Community_Number']).loc[violating_locs].reset_index()

    # Grouping of constraint violation data by 'Location', 'Community_Number' and 'Community_Name'
    violating_distribution = violating_data.groupby(
        ['Location', 'Community_Number', 'Community_Name']).size().reset_index(name='Count')

    # Calculate the frequency of occurrence of each community name
    community_name_counts = df['Community_Name'].value_counts(normalize=True)

    # Converting frequency of occurrence to weights
    weights = community_name_counts / community_name_counts.sum()

    # Find the Community_Name with the highest weight for each combination that violates the constraints
    def get_max_community_name(row, group_df):
        max_count = group_df['Count'].max()
        # Check if more than one Community_Name has the same maximum count
        if group_df[group_df['Count'] == max_count].shape[0] == 1:
            return group_df[group_df['Count'] == max_count]['Community_Name'].values[0]
        else:
            # If there is more than one Community_Name with the maximum count, use the weighting decision
            max_weight = group_df['Weight'].max()
            return group_df[group_df['Weight'] == max_weight]['Community_Name'].values[0]

    # Apply functions and create mappings
    community_name_map = {}
    for loc, group_df in violating_distribution.groupby(['Location', 'Community_Number']):
        group_df['Weight'] = group_df['Community_Name'].apply(lambda x: weights.get(x, 0))
        community_name_map[loc] = get_max_community_name(loc, group_df)

    # Update the 'Community_Name' column in the original data frame
    for (loc, comm_num), comm_name in community_name_map.items():
        mask = (df['Location'] == loc) & (df['Community_Number'] == comm_num)
        df.loc[mask, 'Community_Name'] = comm_name

    # Save the corrected dataframe as a new CSV file
    df.to_csv('building_V11.csv', index=False)



def calculate_weighted_edit_distance(row1, row2, weights):
    w_distance = 0
    for key in weights:
        w_distance += weights[key] * distance(str(row1[key]), str(row2[key]))
    return w_distance


def ZipStateCityDataFusion():
    threshold_beta = 5  # This is an example threshold
    weights = {'City': 1.5, 'State': 1.0, 'Zip': 2.0}

    df = pd.read_csv('building-V2.csv')
    medcond_data = df.to_dict('records')
    # Initialize a list to store duplicate items
    duplicates = []

    # Calculate weighted edit distance
    for i, row1 in enumerate(medcond_data):
        for j, row2 in enumerate(medcond_data):
            if i >= j:  # Avoiding repeated comparisons
                continue
            weighted_distance = calculate_weighted_edit_distance(row1, row2, weights)
            if weighted_distance < threshold_beta:
                duplicates.append((i, j))  # Store indexes instead of records to avoid duplicate data
    print(duplicates)

    # Getting a unique index
    unique_indices = list(set(idx for pair in duplicates for idx in pair))
    # Filter out duplicate rows
    duplicate_rows = df.loc[unique_indices]

    # Calculate the distribution of state columns
    state_distribution = duplicate_rows['State'].value_counts()
    print(state_distribution)

    # Resolve conflicts by selecting the more common state (state) value

    for i, j in duplicates:
        state1 = duplicate_rows.loc[i, 'State']
        state2 = duplicate_rows.loc[j, 'State']
        if state_distribution[state1] >= state_distribution[state2]:
            preferred_state = state1
        else:
            preferred_state = state2
        # Update the state value of a duplicate item
        duplicate_rows.at[i, 'State'] = preferred_state
        duplicate_rows.at[j, 'State'] = preferred_state

    # Save the fused data to a CSV file
    duplicate_rows.to_csv('building_V3.csv', index=False)


# function to compute the frequency and return a weighting map
def calculate_weights(df, column_name):
    counts = df[column_name].value_counts(normalize=True)
    weights = counts / counts.sum()
    return weights


def test_distance():
    # Use a breakpoint in the code line below to debug your script.
    print(distance('IL', 'HA'))  # 应输出 3


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_distance()
    # ZipStateCityDataFusion();
    # DetectAndFixingAddress()
    # DetectAndFixingState()
    # DetectAndFixingCity()
    # DetectAndFixingLocation()
    # DetectAndFixingLocation2()
    # DetectAndFixingAddressLocation()
    # DetectAndFixingLocationCommunity()
    DetectAndFixingLocationCommunity2();

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
