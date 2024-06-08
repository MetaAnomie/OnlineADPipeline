class Evaluator:

    def __init__(self):
        self._true_positives = 0
        self._false_positives = 0
        self._true_negatives = 0
        self._false_negatives = 0

    def false_positives(self):
        return self._false_positives

    def true_positives(self):
        return self._true_positives

    def false_negatives(self):
        return self._false_negatives

    def true_negatives(self):
        return self._true_negatives

    def f_measure(self):
        ret_val = 0
        recall = self.recall()
        precision = self.precision()
        if (precision + recall) > 0:
            ret_val = 2 * ((precision * recall) / (precision + recall))
        return ret_val

    def fpr(self):
        ret_val = 0
        if (self._false_positives + self._true_negatives) > 0:
            ret_val = self._false_positives / (self._false_positives + self._true_negatives)
        return ret_val

    def accuracy(self):
        ret_val = 0
        if (self._true_positives + self._true_negatives + self._false_positives + self._false_negatives) > 0:
            ret_val = (self._true_positives + self._true_negatives) / \
                      (self._true_positives + self._true_negatives + self._false_positives + self._false_negatives)
        return ret_val

    def recall(self):
        ret_val = 0
        if (self._true_positives + self._false_negatives) > 0:
            ret_val = self._true_positives / (self._true_positives + self._false_negatives)
        return ret_val

    def precision(self):
        ret_val = 0
        if (self._true_positives + self._false_positives) > 0:
            ret_val = self._true_positives / (self._true_positives + self._false_positives)
        return ret_val

    def get_result_summary(self):
        return "Precision: {:.4f} | ".format(self.precision()) + \
               "Recall: {:.4f} | ".format(self.recall()) + \
               "Accuracy: {:.4f} | ".format(self.accuracy()) + \
               "F-measure: {:.4f}\n".format(self.f_measure()) + \
               "FPR: {:.4f}\n".format(self.fpr()) + \
               "True Positives: {:d} | ".format(self._true_positives) + \
               "False Positives: {:d} | ".format(self._false_positives) + \
               "True Negatives: {:d} | ".format(self._true_negatives) + \
               "False Negatives: {:d}".format(self._false_negatives)

    def evaluate(self, data, anomaly, ground_truth=None):
        raise NotImplementedError("evaluate method implementation missing.")

    def reset(self):
        raise NotImplementedError("evaluate method implementation missing.")
