from WeatherStation import WeatherStation
import csv


class WeatherDataFiles:
    def write_data(self, WeatherStation):
        try:
            with open("{}.csv".format(WeatherStation.regionName), "r") as rfile:
                lines = rfile.read().splitlines()
                lastLine = lines[-1]
                rfile.close()
                if WeatherStation.timeStamp == lastLine.split(",")[0]:
                    return
        except FileNotFoundError:
            pass
        with open("{}.csv".format(WeatherStation.regionName), "a+", newline="") as wfile:
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
        fieldnames = ["timestamp", "temperature", "airPressure", "sunPower", "rainLastHour", "windSpeed"]
        dataRecords = []
        try:
            with open("{}.csv".format(stationName), "r") as rfile:
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
