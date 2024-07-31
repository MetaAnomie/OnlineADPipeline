from os.path import exists
from Evaluators.Evaluator import Evaluator


class OneToOneEvaluator(Evaluator):

    def __init__(self, anomaly_file=None):
        super().__init__()
        self._anomalies = []
        if anomaly_file is not None and exists(anomaly_file):
            with open(anomaly_file) as file:
                for line in file:
                    self._anomalies.insert(0,line.strip())

    def evaluate(self, data, anomaly, ground_truth=None):

        if data is not None and len(data) > 0:
            if ground_truth is None:
                ground_truth = (data in self._anomalies)

        if ground_truth is True:
            if anomaly is True:
                self._true_positives += 1
            else:
                self._false_negatives += 1
        else:
            if anomaly is True:
                self._false_positives += 1
            else:
                self._true_negatives += 1

    
    def reset(self):
        super().__init__()
