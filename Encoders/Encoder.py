class Encoder:

    def encode(self, data):
        raise NotImplementedError("encode method implementation missing.")
    
    def feedback(self, data, feedback):
        pass

    def retrain(self, training_records, training_time):
        pass
