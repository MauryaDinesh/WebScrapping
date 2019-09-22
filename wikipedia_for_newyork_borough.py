
import json
import requests
import folium
import pandas as pd
import numpy as np
from lxml import etree
from pandas.io.json import json_normalize
import matplotlib.cm as cm
import matplotlib.colors as colors
from geopy.geocoders import Nominatim

wikiData = requests.get('https://en.wikipedia.org/wiki/Boroughs_of_New_York_City')
html = etree.HTML(wikiData.text)
boroughTable = html.xpath('//table[@class="wikitable sortable"]/tbody/tr')

geolocator = Nominatim(user_agent="ny_explorer")

newyork_df_columns = ['Borough','Latitude','Longitude', 'Population', 'Density(Persons/Sq. Km)']
newyork_borough_df = pd.DataFrame(columns = newyork_df_columns)

for row in boroughTable[3:8]:
    rowElements = row.xpath('td')
    name = rowElements[0].xpath('div/b/a')[0].text.strip()

    population_str = rowElements[2].text.strip().split(',')
    population = int("".join(population_str))

    density_str = rowElements[8].text.strip().split(',')
    density = int("".join(density_str))

    location = geolocator.geocode(name)
    latitude = location.latitude
    longitude = location.longitude
    newyork_borough_df = newyork_borough_df.append({'Borough' : name,
                                                    'Latitude' : latitude,
                                                    'Longitude' : longitude,
                                                    'Population' : population,
                                                    'Density(Persons/Sq. Km)' : density}, ignore_index=True)


newyork_borough_df = newyork_borough_df.sort_values(by = 'Density(Persons/Sq. Km)',ascending = False)
newyork_borough_df = newyork_borough_df.reset_index(drop=True)

location = geolocator.geocode('New York City')
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of New York City are {}, {}.'.format(latitude, longitude))

# create map of New York using latitude and longitude values
map_newyork = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough in zip(newyork_borough_df['Latitude'], newyork_borough_df['Longitude'], newyork_borough_df['Borough']):
    label = '{}'.format(borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_newyork)


map_newyork.save('map.html')

