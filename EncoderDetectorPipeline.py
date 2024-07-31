from Detectors.Detector import Detector
from Encoders.Encoder import Encoder


class EncoderDetectorPipeline:

    def __init__(self, encoders=None, detectors=None):

        # Set encoders
        self._encoders = []
        if isinstance(encoders,list):
            type_check = True
            for encoder in encoders:
                if not isinstance(encoder,Encoder):
                    type_check = False
                    break
            if type_check:
                self._encoders = encoders

        # Set decoders
        self._detectors = []
        if isinstance(detectors,list):
            type_check = True
            for detector in detectors:
                if not isinstance(detector,Detector):
                    type_check = False
                    break
            if type_check:
                self._detectors = detectors

    def feedback(self, data, anomalous):
        ret_val = data
        if ret_val is not None and len(ret_val) > 0:
            for encoder in self._encoders:
                ret_val = encoder.feedback(ret_val, anomalous)
            for detector in self._detectors:
                ret_val = detector.feedback(ret_val, anomalous)
        else:
            ret_val = None
        return ret_val

    def retrain(self, training_records=None, training_time=None):
        for encoder in self._encoders:
            ret_val = encoder.retrain(training_records, training_time)
        for detector in self._detectors:
            ret_val = detector.retrain(training_records, training_time)

    def process(self, data):
        ret_val = data
        if ret_val is not None and len(ret_val) > 0:
            for e in self._encoders:
                ret_val = e.encode(ret_val)
            for d in self._detectors:
                ret_val = d.detect(ret_val)
        else:
            ret_val = None
        return ret_val

