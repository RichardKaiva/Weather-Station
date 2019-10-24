class WeatherStation:
    # Insert json data from buienradar, variables are assigned.
    def __init__(self, jsonData=None):
        if jsonData != None:
            self.stationName = jsonData["stationname"]
            self.regionName = jsonData["regio"]
            self.timeStamp = jsonData["timestamp"]
            try:
                self.weatherDescription = jsonData["weatherdescription"]
            except KeyError:
                self.weatherDescription = "N/A"
            try:
                self.visibility = jsonData["visibility"]
            except KeyError:
                self.visibility = "N/A"
            try:
                self.temperature = jsonData["temperature"]
            except KeyError:
                self.temperature = "N/A"
            try:
                self.airPressure = jsonData["airpressure"]
            except KeyError:
                self.airPressure = "N/A"
            try:
                self.sunPower = jsonData["sunpower"]
            except KeyError:
                self.sunPower = "N/A"
            try:
                self.rainLastHour = jsonData["rainFallLastHour"]
            except KeyError:
                self.rainLastHour = "N/A"
            try:
                self.windDirection = jsonData["winddirection"]
            except KeyError:
                self.windDirection = "N/A"
            try:
                self.windSpeed = jsonData["windspeed"]
            except KeyError:
                self.windSpeed = "N/A"
            try:
                self.windGusts = jsonData["windgusts"]
            except KeyError:
                self.windGusts = "N/A"
        else:
            self.stationName = None
            self.regionName = None
            self.timeStamp = None
            self.temperature = None
            self.airPressure = None
            self.sunPower = None
            self.rainLastHour = None
            self.windSpeed = None

