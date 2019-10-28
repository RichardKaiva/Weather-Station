from WeatherStation import WeatherStation
import csv
import os.path
import traceback
import sys


class WeatherDataFiles:
    def write_data(self, WeatherStation):
        # First, the file is opened to check if this data record already exists (i.e. timestamp is the same)
        try:
            with open(
                os.path.join(os.path.join(os.getcwd(), "Archived data"), "{}.csv".format(WeatherStation.regionName)),
                "r",
            ) as rfile:
                lines = rfile.read().splitlines()
                lastLine = lines[-1]
                rfile.close()
                if WeatherStation.timeStamp == lastLine.split(",")[0]:
                    return
        except FileNotFoundError:
            pass
        # Second, the file is created if it does't exit yet and the data record is saved.
        with open(
            os.path.join(os.path.join(os.getcwd(), "Archived data"), "{}.csv".format(WeatherStation.regionName)),
            "a+",
            newline="",
        ) as wfile:
            fieldnames = ["timestamp", "temperature", "airPressure", "sunPower", "rainLastHour", "windSpeed"]
            writer = csv.DictWriter(wfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "timestamp": WeatherStation.timeStamp,
                    "temperature": WeatherStation.temperature,
                    "airPressure": WeatherStation.airPressure,
                    "sunPower": WeatherStation.sunPower,
                    "rainLastHour": WeatherStation.rainLastHour,
                    "windSpeed": WeatherStation.windSpeed,
                }
            )
            wfile.close()

    def read_data(self, stationName):
        # File for the chosen region is opened and a Weather Station object is created for every data record. All ws objects are returned.
        fieldnames = ["timestamp", "temperature", "airPressure", "sunPower", "rainLastHour", "windSpeed"]
        dataRecords = []
        try:
            with open(
                os.path.join(os.path.join(os.getcwd(), "Archived data"), "{}.csv".format(stationName)), "r"
            ) as rfile:
                reader = csv.DictReader(rfile, fieldnames=fieldnames)
                for line in reader:
                    ws = WeatherStation()
                    ws.timeStamp = line["timestamp"]
                    ws.temperature = line["temperature"]
                    ws.airPressure = line["airPressure"]
                    ws.setRainLastHour = line["rainLastHour"]
                    ws.sunPower = line["sunPower"]
                    ws.windSpeed = line["windSpeed"]
                    dataRecords.append(ws)
                rfile.close()
            return dataRecords
        except FileNotFoundError:
            print("Weather station {} not found.".format(stationName))
            traceback.print_exc(limit=1, file=sys.stdout)
