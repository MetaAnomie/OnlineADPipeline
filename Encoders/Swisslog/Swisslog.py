from Encoders.Encoder import Encoder
from Encoders.Swisslog.layers.dictonline_group_layer import DictOnlineGroupLayer
from Encoders.Swisslog.layers.maskonline_layer import MaskOnlineLayer
from Encoders.Swisslog.layers.tokenizeonline_group_layer import TokenizeOnlineGroupLayer


class Swisslog(Encoder):

    def __init__(self, encode_to_indices=False, debug=False):
        self._templates = dict()
        self._encode_to_indices = encode_to_indices
        self._corpus = '../Encoders/Swisslog/EngCorpus.pkl'
        self._tokenize_layer = TokenizeOnlineGroupLayer(rex=[], debug=debug)
        self._dict_layer = DictOnlineGroupLayer(self._corpus, debug)
        self._mask_layer = MaskOnlineLayer(self._dict_layer, self._templates, debug)

    def encode(self, data):
        if data is not None:
            data = self._tokenize_layer.run(data)
            wordset = self._dict_layer.run(data)
            data = self._mask_layer.run(wordset, data, self._encode_to_indices)
        return data
