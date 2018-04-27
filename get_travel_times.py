import googlemaps
import pandas as pd
from sqlalchemy import create_engine

from datetime import datetime


def get_travel_time(from_loc, to_loc):
    now = datetime.now()
    directions_result = gmaps.directions(from_loc,
                                         to_loc,
                                         mode="driving",
                                         departure_time=now)
    
    return directions_result[0]['legs'][0]['duration_in_traffic']['value'] / 60

gmaps = googlemaps.Client(key='AIzaSyDtE2L_xEizY3_xTNCOx1KWgXsw5r_UhoA')

# Set up raw data
df = pd.DataFrame({'from_loc': ['SO16 6DB',
                                'SO16 6DB',
                                "50.911720, -1.401067",
                                "50.917649, -1.457254"],
                   'to_loc':['SO17 1BJ',
                             'Bournemouth',
                             "50.908905, -1.390853",
                             "50.922220, -1.469614"],
                   'route_name': ['Home-Uni',
                                  'Home-Bournemouth',
                                  'Southampton Centre AURN',
                                  'Southampton A33 AURN']})

# Get travel times from API
df['duration'] = df.apply(lambda s: get_travel_time(s['from_loc'], s['to_loc']), axis=1)

df['datetime'] = pd.datetime.now()

# Insert into database
eng = create_engine('mysql://travel_times:traveltimesforairquality@127.0.0.1:3306/travel_times')
df.to_sql('travel_times_raw', eng, if_exists='append', index=False)