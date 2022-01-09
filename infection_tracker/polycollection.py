import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection


class PolyCollection:
    def __init__(self, disease):
        self.disease = disease
        self.event = []
        self.begin = []
        self.end = []

    def add(self, person1, person2, last_meeting_date, last_meeting_duration):
        self.event.append(f'{person1} | {person2}')
        self.begin.append(last_meeting_date)
        self.end.append(last_meeting_date + last_meeting_duration + self.disease.get_infectious_period())

    def show(self):
        self.event = np.array(self.event)
        self.begin = np.array(self.begin)
        self.end = np.array(self.end)

        beg_sort = np.sort(self.begin)
        end_sort = self.end[np.argsort(self.begin)]
        evt_sort = self.event[np.argsort(self.begin)]
        plt.rcParams['ytick.labelsize'] = 'xx-small'

        plt.barh(range(len(beg_sort)), end_sort-beg_sort, left=beg_sort, align='center')

        plt.yticks(range(len(beg_sort)), evt_sort)

        plt.show()