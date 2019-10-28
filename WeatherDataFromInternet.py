# -*- coding: UTF-8 -*-

import urllib.request
from WeatherStation import WeatherStation
import json


class WeatherDataFromInternet:
    def __init__(self):
        self.jsonData = None
        self.stations = None
        self.url = "https://data.buienradar.nl/2.0/feed/json"
        self.response = urllib.request.urlopen(self.url)
        if self.response.getcode() == 200:
            data = self.response.read()
            self.jsonData = json.loads(data)
            self.stations = self.jsonData["actual"]["stationmeasurements"]
        else:
            print("Error receiving data ", self.response.getcode())

    def update(self):
        self.response = urllib.request.urlopen(self.url)
        if self.response.getcode() == 200:
            data = self.response.read()
            self.jsonData = json.loads(data)
            self.stations = self.jsonData["actual"]["stationmeasurements"]
        else:
            print("Error receiving data", self.response.getcode())

    def get_station_data(self, region):
        result = None
        for station in self.stations:
            # print('\"%s\"' % station['regio'], ", ")
            if station["regio"] == region:
                result = station
        return WeatherStation(result)

    def find_warmest(self):
        result = None
        maxTemp = 0
        for station in self.stations:
            if "temperature" in station:
                if float(station["temperature"]) > maxTemp:
                    maxTemp = float(station["temperature"])
                    result = [station["regio"], maxTemp]
        return result[0] + ": " + str(result[1]) + "°C"

    def find_coldest(self):
        result = None
        minTemp = 100.0
        for station in self.stations:
            if "temperature" in station:
                if float(station["temperature"]) < minTemp:
                    minTemp = float(station["temperature"])
                    result = [station["regio"], minTemp]
        return result[0] + ": " + str(result[1]) + "°C"

    def find_sunniest(self):
        result = None
        sunpower = 0.0
        for station in self.stations:
            if "sunpower" in station:
                if float(station["sunpower"]) > sunpower:
                    sunpower = float(station["sunpower"])
                    result = [station["regio"], sunpower]
        if sunpower == 0.0:
            return "Het is donker"
        else:
            return result[0] + ": " + str(result[1]) + " W/m²"

    def find_least_windy(self):
        result = None
        windspeed = 300.0
        for station in self.stations:
            if "windspeed" in station:
                if float(station["windspeed"]) < windspeed:
                    windspeed = float(station["windspeed"])
                    result = [station["regio"], windspeed]
        return result[0] + ": " + str(result[1]) + " m/s"

    def find_most_windy(self):
        result = None
        windspeed = 0.0
        for station in self.stations:
            if "windspeed" in station:
                if float(station["windspeed"]) > windspeed:
                    windspeed = float(station["windspeed"])
                    result = [station["regio"], windspeed]
        return result[0] + ": " + str(result[1]) + " m/s"
