import requests
import pandas as pd

# API endpoint
url = "https://www.trafficengland.com/api/network/getJunctionSections?roadName=M1&_=1724348355123"


# Function to get and parse data from the API
def get_speed_data(url):
    # Send GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # data["01:J1"]["primaryDownstreamJunctionSection"]["avgSpeed"]

        # Extract relevant information
        speed_data = []
        #for junction in data:
        #print(data[junction]["primaryDownstreamJunctionSection"]["avgSpeed"])

        for junction in data:
            junction_name = data[junction]["junctionName"]
            # Check if primaryDownstreamJunctionSection exists and is not None
            if data[junction]["primaryDownstreamJunctionSection"]:
                try:
                    north_direction = data[junction]["primaryDownstreamJunctionSection"]["direction"]
                    north_speed = data[junction]["primaryDownstreamJunctionSection"]["avgSpeed"]
                except KeyError:
                    north_direction = "Unknown Direction"
                    north_speed = None
            else:
                north_direction = "Unknown Direction"
                north_speed = None

            # Check if secondaryUpstreamJunctionSection exists and is not None
            if data[junction]["secondaryUpstreamJunctionSection"]:
                try:
                    south_direction = data[junction]["secondaryUpstreamJunctionSection"]["direction"]
                    south_speed = data[junction]["secondaryUpstreamJunctionSection"]["avgSpeed"]
                except KeyError:
                    south_direction = "Unknown Direction"
                    south_speed = None
            else:
                south_direction = "Unknown Direction"
                south_speed = None

            speed_data.append({
                'Junction': junction_name,
                'NB Direction': north_direction,
                'NB Speed Value': north_speed,
                'SB Direction': south_direction,
                'SB Speed Value': south_speed
            })

        # Convert the list to a DataFrame
        speed_df = pd.DataFrame(speed_data)
        return speed_df

    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


# Call the function and get the data
speed_df = get_speed_data(url)

# Display the DataFrame
if speed_df is not None:
    speed_df.to_csv("speed_data.csv", index=False)
    print("Data saved to speed_data.csv")
