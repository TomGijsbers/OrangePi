import requests
import time
from datetime import datetime

def fetch_and_display_data():
    base_url = "https://api.thingspeak.com/channels/2463041/fields/{field_number}.json"
    api_key_param = "?api_key=IB9GK8DLGA9XDFTA"
    
    # Bepaal het aantal weer te geven records
    num_records_to_display = 15

    # Haal data op voor field 1 en field 2
    for field_number in [1, 2]:
        response = requests.get(base_url.format(field_number=field_number) + api_key_param)
        data = response.json()
        
        # Beperk tot de laatste 'num_records_to_display' records
        latest_records = data['feeds'][-num_records_to_display:]
        
        # Print veldinformatie
        print(f"Laatste {num_records_to_display} records voor Field {field_number} ({data['channel'][f'field{field_number}']}):")
        
        # Print elk record
        for record in latest_records:
            # Parse de datum en tijd, en formatteer deze naar DD-MM-YYYY
            created_at = datetime.strptime(record['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")
            value = record[f'field{field_number}']
            print(f"{created_at}: {value}")
        
        # Print een scheiding tussen de velden
        print("-" * 40)

# Herhaal het ophalen en weergeven van data elke 30 seconden
while True:
    fetch_and_display_data()
    time.sleep(30)
