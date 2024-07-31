from os.path import exists
from Evaluators.Evaluator import Evaluator


class HDFSEvaluator(Evaluator):

    def __init__(self, anomaly_file=None):
        super().__init__()
        self._anomalies = {}
        self._normals = {}
        self._cache_valid = False
        if anomaly_file is not None and exists(anomaly_file):
            with open(anomaly_file) as file:
                for line in file:
                    self._anomalies[line.strip()] = [0, 0]

    def _load_stats_cache(self):
        if not self._cache_valid:
            self._true_positives = 0
            self._false_positives = 0
            self._true_negatives = 0
            self._false_negatives = 0

            for values in self._normals.values():
                if values[0] > 0:
                    self._false_positives = self._false_positives + 1
                elif values[1] > 0:
                    self._true_negatives = self._true_negatives + 1
            for values in self._anomalies.values():
                if values[0] > 0:
                    self._true_positives = self._true_positives + 1
                elif values[1] > 0:
                    self._false_negatives = self._false_negatives + 1
            self._cache_valid = True

    # Wrapper overrides to optimize calculations through value caching

    def false_positives(self):
        self._load_stats_cache()
        return super().false_positives()

    def true_positives(self):
        self._load_stats_cache()
        return super().true_positives()

    def false_negatives(self):
        self._load_stats_cache()
        return super().false_negatives()

    def true_negatives(self):
        self._load_stats_cache()
        return super().true_negatives()

    def f_measure(self):
        self._load_stats_cache()
        return super().f_measure()

    def fpr(self):
        self._load_stats_cache()
        return super().fpr()

    def accuracy(self):
        self._load_stats_cache()
        return super().accuracy()

    def recall(self):
        self._load_stats_cache()
        return super().recall()

    def precision(self):
        self._load_stats_cache()
        return super().precision()

    def evaluate(self, data, anomaly, ground_truth=None):

        if data is not None and len(data) > 0:
            block_id = None
            tokens = data.strip().split()
            for token in tokens:
                if token.startswith("blk_"):
                    block_id = token
                    if ground_truth is None:
                        ground_truth = (block_id in self._anomalies)
                    break

            if block_id is not None and ground_truth is not None:
                self._cache_valid = False
                if ground_truth is True:
                    if block_id not in self._anomalies:
                        self._anomalies[block_id] = [0, 0]
                    if anomaly is True:
                        self._anomalies[block_id][0] = self._anomalies[block_id][0] + 1
                    else:
                        self._anomalies[block_id][1] = self._anomalies[block_id][1] + 1
                else:
                    if block_id not in self._normals:
                        self._normals[block_id] = [0, 0]
                    if anomaly is True:
                        self._normals[block_id][0] = self._normals[block_id][0] + 1
                    else:
                        self._normals[block_id][1] = self._normals[block_id][1] + 1


    def reset(self):
        for anomaly in self._anomalies:
            anomaly = [0, 0]
        self._cache_valid = False
        self._normals = {}
        super().__init__()

