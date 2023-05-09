from Detectors.Detector import Detector
import re

class RuleEngine(Detector):

    def __init__(self):
        self._events = {}
        self._rules = {}
        self._ci_rules = {}

    def detect(self, data):
        ret_val = None
        if data is not None:
            if data in self._events:
                if self._events[data]:
                    ret_val = data
            else:
                signal_flags = [0, 0]
                if len(self._rules) > 0:
                    for rule, anomaly in self._rules.items():
                        if re.search(rule, data) is not None:
                            if anomaly:
                                signal_flags[1] = 1
                            else:
                                signal_flags[0] = 1
                if len(self._ci_rules) > 0:
                    for rule, anomaly in self._ci_rules.items():
                        if re.search(rule, data, re.IGNORECASE) is not None:
                            if anomaly:
                                signal_flags[1] = 1
                            else:
                                signal_flags[0] = 1
                if signal_flags[1] == 1 and signal_flags[0] != 1:
                   ret_val = data
        return ret_val

    def add_keyword_rules(self, keywords=[], anomaly=True, case_insensitive=False):
        if keywords is not None and len(keywords) > 0:
            for word in keywords:
                rule = "((?<=[^A-Za-z0-9])|^)(" + word + ")((?=[^A-Za-z0-9])|$)"
                if case_insensitive:
                    self._ci_rules[rule] = anomaly
                else:
                    self._rules[rule] = anomaly

    def add_rules(self, rules=[], anomaly=True, case_insensitive=False):
        if rules is not None and len(rules) > 0:
            for rule in rules:
                if case_insensitive:
                    self._ci_rules[rule] = anomaly
                else:
                    self._rules[rule] = anomaly

    def feedback(self, data, feedback):
        if data is not None:
            if feedback is True:
                self._events[data] = True
            if feedback is False:
                self._events[data] = False
                
    def clear_rules(self):
        self._rules.clear()
        self._ci_rules.clear()

