from Detector import Detector
from datetime import datetime, timedelta


class UniqueEvents(Detector):

    def __init__(self, training_records=10000, training_time=604800):
        self._events = {}
        self._trainingRecords = training_records
        self._recordCount = 0
        self._trainingTime = datetime.now() + timedelta(seconds=training_time)
        self._startTime = datetime.now()

    def set_training_time(self, training_records, training_time):
        self._startTime = datetime.now()
        self._recordCount = 0
        self._trainingRecords = training_records
        self._trainingTime = datetime.now() + timedelta(seconds=training_time)

    def detect(self, data):
        ret_val = None
        if data is not None:
            if self._recordCount >= self._trainingRecords or datetime.now() > self._trainingTime:
                if data in self._events.keys():
                    if self._events[data] is True:
                        ret_val = data
                else:
                    ret_val = data
            else:
                self._events[data] = False
                self._recordCount = self._recordCount + 1
        return ret_val

    def feedback(self, data, feedback):
        if data is not None:
            if feedback is True:
                self._events[data] = True
            if feedback is False:
                self._events[data] = False
