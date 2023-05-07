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

    def accuracy(self):
        ret_val = 0
        tp = self.true_positives()
        tn = self.true_negatives()
        fp = self.false_positives()
        fn = self.false_negatives()
        if (tp + tn + fp + fn) > 0:
            ret_val = (tp + tn) / \
                      (tp + tn + fp + fn)
        return ret_val

    def recall(self):
        ret_val = 0
        tp = self.true_positives()
        fn = self.false_negatives()
        if (tp + fn) > 0:
            ret_val = tp / (tp + fn)
        return ret_val

    def precision(self):
        ret_val = 0
        tp = self.true_positives()
        fp = self.false_positives()
        if (tp+fp) > 0:
            ret_val = tp / (tp + fp)
        return ret_val

    def get_result_summary(self):
        return "Precision: {:.4f} | ".format(self.precision()) + \
               "Recall: {:.4f} | ".format(self.recall()) + \
               "Accuracy: {:.4f} | ".format(self.accuracy()) + \
               "F-measure: {:.4f}\n".format(self.f_measure()) + \
               "True Positives: {:d} | ".format(self.true_positives()) + \
               "False Positives: {:d} | ".format(self.false_positives()) + \
               "True Negatives: {:d} | ".format(self.true_negatives()) + \
               "False Negatives: {:d}".format(self.false_negatives())

    def evaluate(self, data, anomaly):
        raise NotImplementedError("evaluate method implementation missing.")