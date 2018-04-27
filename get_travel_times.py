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
                                "50.910748, -1.401117",
                                "50.917270, -1.455860",
                                "50.914120, -1.401942"],
                   'to_loc':['SO17 1BJ',
                             'Bournemouth',
                             "50.909902, -1.389125",
                             "50.922313, -1.470873",
                             "50.952391, -1.403923"],
                   'route_name': ['Home-Uni',
                                  'Home-Bournemouth',
                                  'Southampton Centre AURN',
                                  'Southampton A33 AURN',
                                  'Avenue']})

# Add reverse routes of the above to the data frame
rev_df = df.copy()
rev_df.columns = ['to_loc', 'route_name', 'from_loc']
rev_df['route_name'] = rev_df.route_name + " Rev"

df = pd.concat([df, rev_df])


# Get travel times from API
df['duration'] = df.apply(lambda s: get_travel_time(s['from_loc'], s['to_loc']), axis=1)

df['datetime'] = pd.datetime.now()

# Insert into database
eng = create_engine('mysql://travel_times:traveltimesforairquality@127.0.0.1:1234/travel_times')
df.to_sql('travel_times_raw', eng, if_exists='append', index=False)