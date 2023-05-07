from Encoders.Encoder import Encoder
import re


class RegexReplace(Encoder):

    def __init__(self, enable_defaults=True):
        self._enableDefaultRules = enable_defaults
        self._rules = {}
        self.__loadDefaultRules()

# /mnt/hadoop/dfs/data/current/subdir57/blk_<:NUM:>
# "((?<=[^A-Za-z0-9])|^) ((?=[^A-Za-z0-9])|$)": "<:PATH:>",

    def __loadDefaultRules(self):
        self._default_rules = {
            "((?<=[^A-Za-z0-9])|^)((0?[1-9]|1[012])[-/.](0?[1-9]|[12][0-9]|3[01])[-/.]([1-9]\d\d\d|[0-9]\d))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)((0?[1-9]|[12][0-9]|3[01])[-/.](0?[1-9]|1[012])[-/.]([1-9]\d\d\d|[0-9]\d))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)(([1-9]\d\d\d|[0-9]\d)[-/.](0?[1-9]|1[012])[-/.](0?[1-9]|[12][0-9]|3[01]))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})((?=[^A-Za-z0-9])|$)": "<:IP:>",
            "((?<=[^A-Za-z0-9])|^)(0x[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)": "<:HEX:>",
            "((?<=[^A-Za-z0-9])|^)([\\-\\+]?\\d+)((?=[^A-Za-z0-9])|$)": "<:NUM:>"
        }

    def encode(self, data):
        if data is not None:
            for k, v in self._rules.items():
                data = re.sub(k, v, data)
        if self._enableDefaultRules:
            for k, v in self._default_rules.items():
                data = re.sub(k, v, data)
        return data

    def enable_default_rules(self, enable_defaults=True):
        self._enableDefaultRules = enable_defaults

    def add_replace_rule(self, rule=None, replace=None):
        if rule is not None:
            if replace is None:
                replace = ""
            self._rules[rule] = replace
