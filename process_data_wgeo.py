import csv
import requests

# Load the CDR data from a CSV file
def load_cdr_data(csv_file_path):
    cdr_data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cdr_data.append(row)
    return cdr_data

# Group CDR data by state and count calls
def group_cdr_by_state(cdr_data):
    calls_by_state = {}
    for record in cdr_data:
        state = record['State']
        calls = calls_by_state.get(state, 0)
        calls += 1
        calls_by_state[state] = calls
    return calls_by_state

# Fetch flag icons for each state
def fetch_flag_icons(calls_by_state):
    flag_icons = {}
    for state in calls_by_state.keys():
        icon_url = f"https://raw.githubusercontent.com/oxguy3/flags/master/iso/{state}.png"
        flag_icons[state] = icon_url
    return flag_icons

# Save the call statistics data to a JSON file
def save_call_stats_to_json(calls_by_state, flag_icons, output_file):
    call_stats = {
        "callsByState": calls_by_state,
        "flagIcons": flag_icons
    }
    with open(output_file, 'w') as jsonfile:
        json.dump(call_stats, jsonfile, indent=2)

if __name__ == '__main__':
    cdr_file_path = 'path/to/your/cdr/file.csv'
    output_json_file = 'call_stats_data.json'

    cdr_data = load_cdr_data(cdr_file_path)
    calls_by_state = group_cdr_by_state(cdr_data)
    flag_icons = fetch_flag_icons(calls_by_state)
    save_call_stats_to_json(calls_by_state, flag_icons, output_json_file)

    print("Call statistics data has been generated and saved to", output_json_file)
