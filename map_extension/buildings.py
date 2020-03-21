import numpy as np
import json
import overpy

class building():

    def __init__(self, way, tags, hdd, cdd):
        self.way = way
        self.tags = tags
        self.hdd = hdd
        self.cdd = cdd

    @abstractmethod
    def estimate_height(self):
        pass

    @abstractmethod
    def estimate_type(self):
        pass
    
    @abstractmethod
    def calc_energy_usage(self, trained_classifier):
        pass

    def estimate_area(self):

        return area

class res_building(building):

    def __init__(self, way, tags, hdd, cdd):
        super().__init__()

    def estimate_height(self):

        return height 

    def estimate_type(self):

        return building_type

    def calc_energy_usage(self, trained_classifier):

        sqft = self.estimate_area()
        stories = self.estimate_height()
        building_type = self.estimate_type()

        data = np.array([sqft, stories, building_type, self.hdd, self.cdd])
        energy_usage = trained_classifier.predict(data)

        return energy_usage
    

class commercial_building(building):

    def __init__(self, way, tags, hdd, cdd):
        super().__init__()

    def estimate_height(self):

        return height 

    def estimate_type(self):

        return building_type

    def calc_energy_usage(self, trained_classifier):

        sqft = self.estimate_area()
        building_type = self.estimate_type()

        data = np.array([sqft, building_type, self.hdd, self.cdd])
        energy_usage = trained_classifier.predict(data)

        return energy_usage
