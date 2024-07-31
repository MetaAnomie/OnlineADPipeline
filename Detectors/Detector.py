class Detector:

    def detect(self, data):
        raise NotImplementedError("detect method implementation missing.")

    def feedback(self, data, feedback):
        pass

    def retrain(self, training_records, training_time):
        pass
