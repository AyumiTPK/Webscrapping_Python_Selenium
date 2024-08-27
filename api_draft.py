import requests
import pandas as pd
import time
import json

# API endpoint
url = "https://www.trafficengland.com/api/network/getJunctionSections?roadName=M1&_=1724348355123"

# Function to get and parse data from the API
# def get_speed_data(url):
    # Send GET request to the API
response = requests.get(url)

    # Check if the request was successful
if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve data: {response.status_code}")
        # Parse the content to JSON
