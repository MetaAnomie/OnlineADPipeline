from Detector import Detector
from Encoder import Encoder


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
        if data is not None:
            for detector in self._detectors:
                detector.feedback(data, anomalous)

    def process(self, data):
        ret_val = data
        if ret_val is not None and len(ret_val) > 0:
            for e in self._encoders:
                ret_val = e.encode(ret_val)
            for d in self._detectors:
                ret_val = d.detect(ret_val)
        return ret_val

