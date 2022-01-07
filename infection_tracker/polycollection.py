import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection
from infection_tracker.disease import Disease
from infection_tracker.person import Person

class PolyCollection:
    def __init__(self, disease):
        self.data = []
        self.cats = []
        self.collection_name = disease.get_disease_name()

    def add(self, person, last_meeting_date, last_meeting_duration):
        self.data += [
            (last_meeting_date, last_meeting_date + last_meeting_duration, person.__str__())
            ]
        self.cats += {person.__str__()}

    def show(self):
        verts = []
        for d in self.data:
            v =  [(mdates.date2num(d[0]), self.cats[d[2]]-.4),
                (mdates.date2num(d[0]), self.cats[d[2]]+.4),
                (mdates.date2num(d[1]), self.cats[d[2]]+.4),
                (mdates.date2num(d[1]), self.cats[d[2]]-.4),
                (mdates.date2num(d[0]), self.cats[d[2]]-.4)]
            verts.append(v)

        bars = PolyCollection(self.verts)

        fig, ax = plt.subplots()
        ax.add_collection(bars)
        ax.autoscale()
        loc = mdates.MinuteLocator(byminute=[0,15,30,45])
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

        ax.set_yticks([1,2,3])
        ax.set_yticklabels(["sleep", "eat", "work"])
        plt.show()