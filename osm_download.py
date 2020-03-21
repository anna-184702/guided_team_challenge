# Author: Anna Vaughan
# Created: 11/3/2020
# Last modified:

import numpy as np 
import json
import overpy

''' Top level script for creating the European energy usage maps '''

# Querying the overpass API

api = overpy.Overpass()

overpass_query = """[out:json][timeout:25];
(
  way[building](52.20,0.118,52.205,0.123);
  node(w);
);
out body;
>;
"""

data = api.query(overpass_query)

way_ids = data.get_way_ids()

for way_id in way_ids:
    try:
        print(data.get_way(way_id).tags['levels'])
        print(data.get_way(way_id).tags['building'])
    except KeyError:
        continue

# Make a github repo

# For each square in the grid, we need to know the approximate land use
# This allows us to transform building = yes to building = residential or building = commercial
# Decide on usage classes
# Need to figure out which usage class the building falls into (if possible)
# Otherwise, at least need commercial vs. residential

# We need to get the area of the building from the polygon
# Number of levels 
# -> Floorspace

# Heating and cooling degree days

# Set up and run all the code

# Normalise out

