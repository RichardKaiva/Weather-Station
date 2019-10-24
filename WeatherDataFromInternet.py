# -*- coding: UTF-8 -*-

import urllib.request
from WeatherStation import WeatherStation
import json


class WeatherDataFromInternet:
    def __init__(self):
        self.response = None
        self.stations = None
        self.url = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
        if self.url.getcode() == 200:
            data = self.url.read()
            self.response = json.loads(data)
            self.stations = self.response["actual"]["stationmeasurements"]
        else:
            print("Error receiving data", self.url.getcode())

    def get_station_data(self, region):
        for station in self.stations:
            # print('\"%s\"' % station['regio'], ", ")
            if station["regio"] == region:
                result = station
        return WeatherStation(result)

    def find_warmest(self):
        maxTemp = 0
        for station in self.stations:
            if "temperature" in station:
                if float(station["temperature"]) > maxTemp:
                    maxTemp = float(station["temperature"])
                    result = [station["regio"], maxTemp]
        return result[0] + ": " + str(result[1]) + "°C"

    def find_coldest(self):
        minTemp = 100.0
        for station in self.stations:
            if "temperature" in station:
                if float(station["temperature"]) < minTemp:
                    minTemp = float(station["temperature"])
                    result = [station["regio"], minTemp]
        return result[0] + ": " + str(result[1]) + "°C"

    def find_sunniest(self):
        sunpower = 0.0
        for station in self.stations:
            if "sunpower" in station:
                if float(station["sunpower"]) > sunpower:
                    sunpower = float(station["sunpower"])
                    result = [station["regio"], sunpower]
        if sunpower == 0.0:
            return "Het is donker"
        else:
            return result[0] + ": " + str(result[1])

    def find_least_windy(self):
        windspeed = 300.0
        for station in self.stations:
            if "windspeed" in station:
                if float(station["windspeed"]) < windspeed:
                    windspeed = float(station["windspeed"])
                    result = [station["regio"], windspeed]
        return result[0] + ": " + str(result[1])

    def find_most_windy(self):
        windspeed = 0.0
        for station in self.stations:
            if "windspeed" in station:
                if float(station["windspeed"]) > windspeed:
                    windspeed = float(station["windspeed"])
                    result = [station["regio"], windspeed]
        return result[0] + ": " + str(result[1])