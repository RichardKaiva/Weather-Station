from WeatherDataFromInternet import WeatherDataFromInternet
from WeatherDataFiles import WeatherDataFiles
import os
import numpy as np
import time
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Frame, Label, Button, OptionMenu, StringVar, Text, Toplevel, ttk, TOP, BOTH
import matplotlib

matplotlib.use("TkAgg")

style.use("ggplot")


class WS:
    def __init__(self):
        self.master = Tk()
        self.master.title("Weather Station")
        self.master.configure(background="gray")
        self.master.geometry("800x1000")
        self.data = WeatherDataFromInternet()
        self.create_widgets()

    def run(self):
        self.master.mainloop()  # starts/shows the GUI

    def quit(self, exitCode):
        self.isRunningFlag = False
        self.master.quit()  # stops mainloop
        if os.name == "nt":
            self.master.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        # exit(exitCode)

    def create_widgets(self):

        headLabel = Label(self.master, text="Buienradar Desktop", font=("Helvetica", 24))
        headLabel.grid(row=0, columnspan=5, pady=5)

        self.draw_dropdown()

        self.draw_overview_part()

        self.draw_selected_location_part()

        creditsLabel = Label(self.master, text="Created by Richard & Dimitriy", height=2, width=24)
        buienradarLabel = Label(self.master, text="@Buienradar.nl", height=2, width=24)

        creditsLabel.grid(row=13, column=0, pady=(16, 0))
        buienradarLabel.grid(row=13, column=3, pady=(16, 0))
        self.history_button = Button(self.master, text="Show Archived Data", command=self.show_history)
        self.history_button.grid(row=8, column=3, columnspan=4)

    def draw_dropdown(self):
        regions = [
            "Venlo",
            "Arnhem",
            "Berkhout",
            "Cadzand",
            "Utrecht",
            "Den Helder",
            "Eindhoven",
            "Weert",
            "Noordzee",
            "Gilze Rijen",
            "Goes",
            "Oost-Overijssel",
            "Groningen",
            "Oost-Zeeland",
            "Zwolle",
            "Gorinchem",
            "Hoek van Holland",
            "Hoogeveen",
            "Wadden",
            "Enkhuizen-Lelystad",
            "Schiermonnikoog",
            "IJmond",
            "IJmuiden",
            "Noord-Groningen",
            "Goeree",
            "Leeuwarden",
            "Lelystad",
            "West-Utrecht",
            "Maastricht",
            "Noordoostpolder",
            "Oost-Groningen",
            "Oosterschelde",
            "Rotterdam",
            "Rotterdam Haven",
            "Schaar",
            "Amsterdam",
            "Midden-Zeeland",
            "West-Friesland",
            "Texel",
            "Tholen",
            "Twente",
            "West-Zeeland",
            "Vlieland",
            "Vlissingen",
            "Uden",
            "Voorschoten",
            "Terneuzen",
            "Hoorn",
            "Wijk aan Zee",
            "Woensdrecht",
            "Noordzee",
            "Noordzee",
        ]

        # A function called whenever a new location is chosen.
        def callback(*args):
            station = self.data.get_station_data(self.selectedRegion.get())
            self.description_text["text"] = station.weatherDescription
            self.visibility_text["text"] = station.visibility
            self.temperature_text["text"] = station.temperature
            self.airpressure_text["text"] = station.airPressure
            self.sunpower_text["text"] = station.sunPower
            self.rain_text["text"] = station.rainLastHour
            self.winddirection_text["text"] = station.windDirection
            self.windspeed_text["text"] = station.windSpeed
            self.windgusts_text["text"] = station.windGusts
            self.file = WeatherDataFiles()
            self.file.write_data(station)
            self.draw_airpressure_temp_chart()

        self.selectedRegion = StringVar(self.master)
        self.selectedRegion.set("Choose a location")
        self.selectedRegion.trace("w", callback)
        self.dropDown = ttk.Combobox(
            self.master, textvariable=self.selectedRegion, values=regions, font=("Helvetica", 16)
        )
        self.dropDown.grid(row=1, columnspan=5, pady=5)

    def draw_airpressure_temp_chart(self):
        self.pullDataTemp = {}
        self.pullDataAirPressure = {}

        def animate(i):
            records = self.file.read_data(self.selectedRegion.get())
            if records == None:
                return
            for record in records:
                self.pullDataTemp[record.timeStamp] = record.temperature
                self.pullDataAirPressure[record.timeStamp] = record.airPressure
            self.chartTemp.clear()
            self.chartAirPressure.clear()
            try:
                self.chartTemp.plot(list(self.pullDataTemp.keys()), list(self.pullDataTemp.values()))
                self.chartAirPressure.plot(
                    list(self.pullDataAirPressure.keys()), list(self.pullDataAirPressure.values())
                )
            except ValueError:
                print("INVALID INPUT: .plot(**kwargs)")
                return

        self.f = Figure(figsize=(7, 4), dpi=100)
        self.chartTemp = self.f.add_subplot(211)
        self.chartAirPressure = self.f.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.f, self.master)
        ani = animation.FuncAnimation(self.f, animate, interval=5000)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=14, rowspan=5, column=1, columnspan=4, pady=(16, 0))

        tempreture_label = Label(self.master, text="Tempreture", width=16, font=("Helvetica", 12))
        airpressure_label = Label(self.master, text="Air Pressure", width=16, font=("Helvetica", 12))
        tempreture_label.grid(row=15, column=0)
        airpressure_label.grid(row=17, column=0)
        self.toolbarFrame = Frame(self.master)
        self.toolbarFrame.grid(row=19, column=1, columnspan=4, pady=(4, 0))
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.update()

    def show_history(self):
        chartWindow = Toplevel(self.master)
        chartWindow.title("Data")
        self.history_figure = Figure(dpi=100)
        self.history_temp_chart = self.history_figure.add_subplot(421)
        self.history_air_chart = self.history_figure.add_subplot(422)
        self.history_rain_chart = self.history_figure.add_subplot(423)
        self.history_sun_chart = self.history_figure.add_subplot(424)
        self.history_wind_chart = self.history_figure.add_subplot(425)
        canvas = FigureCanvasTkAgg(self.history_figure, master=chartWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, chartWindow)
        toolbar.update()
        toolbar.pack(fill=BOTH, expand=True)

    def draw_overview_part(self):
        label1 = Label(self.master, text="Warmest: ", height=3, width=24)
        label2 = Label(self.master, text="Coldest:", height=3, width=24)
        label3 = Label(self.master, text="Sunniest:", height=3, width=24)
        label4 = Label(self.master, text="Least windy:", height=3, width=24)
        label5 = Label(self.master, text="Most windy:", height=3, width=24)

        self.warmest_text = Label(self.master, height=2, width=24)
        self.coldest_text = Label(self.master, height=2, width=24)
        self.sunniest_text = Label(self.master, height=2, width=24)
        self.leastwindy_text = Label(self.master, height=2, width=24)
        self.mostwindy_text = Label(self.master, height=2, width=24)

        self.warmest_text["text"] = self.data.find_warmest()
        self.coldest_text["text"] = self.data.find_coldest()
        self.sunniest_text["text"] = self.data.find_sunniest()
        self.leastwindy_text["text"] = self.data.find_least_windy()
        self.mostwindy_text["text"] = self.data.find_most_windy()

        label1.grid(row=2, column=0)
        label2.grid(row=2, column=1)
        label3.grid(row=2, column=2)
        label4.grid(row=2, column=3)
        label5.grid(row=2, column=4)

        self.warmest_text.grid(row=3, column=0)
        self.coldest_text.grid(row=3, column=1)
        self.sunniest_text.grid(row=3, column=2)
        self.leastwindy_text.grid(row=3, column=3)
        self.mostwindy_text.grid(row=3, column=4)

    def draw_selected_location_part(self):
        label6 = Label(self.master, text="Description: ", height=2, width=24)
        label7 = Label(self.master, text="Visibility:", height=2, width=24)
        label8 = Label(self.master, text="Temperature:", height=2, width=24)
        label9 = Label(self.master, text="Air Pressure:", height=2, width=24)
        label10 = Label(self.master, text="Sun Power:", height=2, width=24)
        label11 = Label(self.master, text="Rain 1h:", height=2, width=24)
        label12 = Label(self.master, text="Wind Direction:", height=2, width=24)
        label13 = Label(self.master, text="Wind Speed:", height=2, width=24)
        label14 = Label(self.master, text="Wind Gusts:", height=2, width=24)

        self.description_text = Label(self.master, height=2, width=24)
        self.visibility_text = Label(self.master, height=2, width=24)
        self.temperature_text = Label(self.master, height=2, width=24)
        self.airpressure_text = Label(self.master, height=2, width=24)
        self.sunpower_text = Label(self.master, height=2, width=24)
        self.rain_text = Label(self.master, height=2, width=24)
        self.winddirection_text = Label(self.master, height=2, width=24)
        self.windspeed_text = Label(self.master, height=2, width=24)
        self.windgusts_text = Label(self.master, height=2, width=24)

        label6.grid(row=4, column=0, pady=(64, 0))
        label7.grid(row=5, column=0)
        label8.grid(row=6, column=0)
        label9.grid(row=7, column=0)
        label10.grid(row=8, column=0)
        label11.grid(row=9, column=0)
        label12.grid(row=10, column=0)
        label13.grid(row=11, column=0)
        label14.grid(row=12, column=0)

        self.description_text.grid(row=4, column=1, pady=(64, 0))
        self.visibility_text.grid(row=5, column=1)
        self.temperature_text.grid(row=6, column=1)
        self.airpressure_text.grid(row=7, column=1)
        self.sunpower_text.grid(row=8, column=1)
        self.rain_text.grid(row=9, column=1)
        self.winddirection_text.grid(row=10, column=1)
        self.windspeed_text.grid(row=11, column=1)
        self.windgusts_text.grid(row=12, column=1)

    def set_overview_variables(self, warmest, coldest, sunniest, leastwindy, mostwindy):
        self.warmest_text["text"] = warmest
        self.coldest_text["text"] = coldest
        self.sunniest_text["text"] = sunniest
        self.leastwindy_text["text"] = leastwindy
        self.mostwindy_text["text"] = mostwindy

    def set_location_variables(
        self, description, visibility, temp, airpressure, sunpower, rain, winddirection, windspeed, windgusts
    ):
        self.description_text["text"] = description
        self.visibility_text["text"] = visibility
        self.temperature_text["text"] = temp
        self.airpressure_text["text"] = airpressure
        self.rain_text["text"] = rain
        self.winddirection_text["text"] = winddirection
        self.windspeed_text["text"] = windspeed
        self.windgusts_text["text"] = windgusts