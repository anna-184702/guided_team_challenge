from grid_cell import *
from buildings import *
import ee

if __name__ == "__main__":

    # Make a lat - lon grid
    # Make a residential energy array
    # Make a commercial energy array

    # Load in the usage dataset
    ee.Initialize()
    land_cover = ee.ImageCollection("COPERNICUS/CORINE/V20/100m").filterDate(1546214400000)

    val = lc.select('landcover').reduceRegion(ee.Reducer.mode(),p,100).get('landcover').getInfo()

    ee.Number(lc.reduceRegion(ee.Reducer.count(),p,100).get('constant'))
    # Load in the hdd dataset
    # Load in the cdd dataset

    # For each lat - lon grid cell, do:

        # Get usage - if not land, write zeros and continue
        p = ee.Geometry.Point([lon, lat])
        lc = land_cover.filterBounds(p).first()
        # Get HDD
        # Get CDD

        # Make a grid cell object
        # Get residential energy use
        # Get commercial energy use

meanDict = lc.reduceRegion(reducer= ee.Reducer.mean(),geometry= feature_geometry,scale= 90)