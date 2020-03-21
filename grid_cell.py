import numpy as np
import json
import overpy

class grid_cell():

    def __init__(self, lat_b, lat_t, lon_l, lon_r, usage, hdd, cdd):
        self.usage = usage
        self.api = overpy.Overpass()
        self.query = """[out:json][timeout:25];
            (
            way[building]({},{},{},{});
            node(w);
            );
            out body;
            >;
            """.format(lat_b, lon_l, lat_t, lon_r)
        self.buildings = self.api.query(overpass_query)
        self.way_ids = self.buildings.get_way_ids()
        self.res_way_ids = self.make_way_id_list()
        self.hdd = hdd
        self.cdd = cdd

    def make_way_id_list(self):

        for way_id in self.way_ids:

            tag = self.buildings.get_way(way_id).tags['building']

            # Handle the different cases
            if tag == "yes":
                if self.usage == "res":
                    tag_type = 

    def get_total_res_energy(self):
        