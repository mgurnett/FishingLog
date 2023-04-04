import pandas as pd
import asyncio
from env_canada import ECHistoricalRange, get_historical_stations
from datetime import datetime

coordinates = ['48.508333', '-68.467667']

stations = pd.DataFrame(asyncio.run(get_historical_stations(coordinates, start_year=2022,
                                                end_year=2022, radius=200, limit=100))).T

ec = ECHistoricalRange(station_id=int(stations.iloc[0,2]), timeframe="daily",
                        daterange=(datetime(2022, 7, 1, 12, 12), datetime(2022, 8, 1, 12, 12)))

ec.get_data()

#yield an XML formated str. 
# For more options, use ec.to_xml(*arg, **kwargs) with pandas options
ec.xml
 
#yield an CSV formated str.
# For more options, use ec.to_csv(*arg, **kwargs) with pandas options
ec.csv