import overpass 

api = overpass.API()
response = api.get('https://data.osmbuildings.org/0.2/anonymous/tile/15/17605/10743.json')