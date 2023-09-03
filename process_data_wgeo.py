import csv
import json

def extract_data_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data_list = [row for row in reader]
    return data_list

def transform_to_desired_format(data):
    series = []
    labels = ["Answered", "Missed", "Blocked"]
    colors = ["#ff0000", "#00ff00", "#0000ff"]  # You can update these values to your desired colors

    answered_calls = sum(1 for call in data if call['Call Result'] == 'Answered')
    missed_calls = sum(1 for call in data if call['Call Result'] == 'Missed')
    blocked_calls = sum(1 for call in data if call['Call Result'] == 'Blocked')

    series.extend([answered_calls, missed_calls, blocked_calls])

    return {
        "series": series,
        "labels": labels,
        "colors": colors
    }

def main():
    csv_file = 'call-history_all-calls_on-8_28_2023.csv'
    json_file = 'callstatswgeo.json'

    data = extract_data_from_csv(csv_file)
    transformed_data = transform_to_desired_format(data)

    with open(json_file, 'w') as file:
        json.dump(transformed_data, file, indent=4)

if __name__ == "__main__":
    main()
