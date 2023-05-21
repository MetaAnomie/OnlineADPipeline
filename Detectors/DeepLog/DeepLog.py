import torch
import torch.nn as nn
from Detectors.DeepLog.DeepLogLSTM import DeepLogLSTM
from Detectors.Detector import Detector
from datetime import datetime, timedelta


class DeepLog(Detector):

    def __init__(self, training_records=10000, training_time=604800, top=1, window_size=4):
        self._trainingRecords = training_records
        self._recordCount = 0
        self._trainingTime = datetime.now() + timedelta(seconds=training_time)
        self._startTime = datetime.now()
        self._device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._input = 300
        self._hidden = 64
        self._layers = 2
        self._top = top
        self._window_size = window_size
        self._window = []
        self._training_labels = []
        self._training_seqs = []
        self._training_complete = False

        self._model = DeepLogLSTM(input_size=self._input, hidden_size=self._hidden,
                                  output_size=self._input, num_layers=self._layers).to(self._device)

    def detect(self, data):
        ret_val = None
        if data is not None:
            self._window.append(data)
            while len(self._window) > self._window_size:
                self._window.pop(0)

            if self._recordCount >= self._trainingRecords or datetime.now() > self._trainingTime:
                if not self._training_complete:
                    self.train()
                else:
                    seq = torch.Tensor([self._window[:-1]]).to(torch.long)
                    y_pred, confidence = self._model.predict(X=seq, k=self._top)
                    if data not in y_pred:
                        ret_val = str(data)
            else:
                if len(self._window) == self._window_size:
                    self._training_labels.append(data)
                    self._training_seqs.append(self._window[:-1])
                self._recordCount = self._recordCount + 1
        return ret_val

    def train(self, epochs=1000, batch_size=128):
        print("Training Network...")
        seqs = torch.Tensor(self._training_seqs).to(torch.long)
        labels = torch.Tensor(self._training_labels).to(torch.long)
        self._model.fit(X=seqs, y=labels, epochs=epochs, batch_size=batch_size,
                        criterion=nn.CrossEntropyLoss())
        self._training_complete = True
