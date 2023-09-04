
import pandas as pd
import json
import phonenumbers
from phonenumbers import geocoder

def get_location_from_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        location = geocoder.description_for_number(parsed_number, 'en')
        return location
    except:
        return "Unknown"

def update_json_files_with_libphonenumber(csv_path, json_paths):
    # Load the JSON files
    with open(json_paths['callhistorydb'], 'r') as file:
        callhistorydb_data = json.load(file)
        
    with open(json_paths['callstatswgeo'], 'r') as file:
        callstatswgeo_data = json.load(file)
        
    with open(json_paths['calloverview'], 'r') as file:
        calloverview_data = json.load(file)
    
    # Read the CSV file
    csv_data = pd.read_csv(csv_path)
    
    # Determine the state/location for each call record in the CSV
    csv_data['Location'] = csv_data['From Number'].apply(get_location_from_number)
    
    # Update callhistorydb (1).json and calloverview.json
    new_calls = csv_data.to_dict(orient='records')
    callhistorydb_data['calls'].extend(new_calls)
    calloverview_data['calls'].extend(new_calls)
    
    # Update callstatswgeo.json
    # Update callsByState
    location_counts = csv_data['Location'].value_counts().to_dict()
    for location, count in location_counts.items():
        callstatswgeo_data['callsByState'][location] = callstatswgeo_data['callsByState'].get(location, 0) + count
        
    # Other updates remain the same as before...
    
    # Save the updated JSON files
    with open(json_paths['callhistorydb'], 'w') as file:
        json.dump(callhistorydb_data, file, indent=4)
        
    with open(json_paths['callstatswgeo'], 'w') as file:
        json.dump(callstatswgeo_data, file, indent=4)
        
    with open(json_paths['calloverview'], 'w') as file:
        json.dump(calloverview_data, file, indent=4)
    
    return "JSON files updated successfully!"

# Paths to the JSON files
json_paths = {
    'callhistorydb': '/var/www/n2p/json/callhistorydb.json',
    'callstatswgeo': '/var/www/n2p/json/callstatswgeo.json',
    'calloverview': '/var/www/n2p/json/calloverview.json'
}

csv_path = '/var/www/n2p/json/call-history_all-calls_on-8_28_2023.csv'
update_json_files_with_libphonenumber(csv_path, json_paths)
