from Encoders.Encoder import Encoder
import re


class RegexReplace(Encoder):

    def __init__(self, enable_standard_rules=True, enable_datetime_rules=True):
        self._rules = {}
        self._enableStandardRules = enable_standard_rules
        self._enableDatetimeRules = enable_datetime_rules
        self.__loadDateTimeRules()
        self.__loadStandardRules()

    def __loadDateTimeRules(self):
        self._datetime_rules = {
            "((?<=[^A-Za-z0-9])|^)(([1-9]\d\d\d|[0-9]\d)[-/.](0?[1-9]|1[012])[-/.](0?[1-9]|[12][0-9]|3[01]))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)((0?[1-9]|1[012])[-/.](0?[1-9]|[12][0-9]|3[01])[-/.]([1-9]\d\d\d|[0-9]\d))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)((0?[1-9]|[12][0-9]|3[01])[-/.](0?[1-9]|1[012])[-/.]([1-9]\d\d\d|[0-9]\d))((?=[^A-Za-z0-9])|$)": "<:DATE:>",
            "((?<=[^A-Za-z0-9])|^)([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9].[0-9]{1,9}((?=[^A-Za-z0-9])|$)": "<:TIME:>",
            "((?<=[^A-Za-z0-9])|^)([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?((?=[^A-Za-z0-9])|$)": "<:TIME:>",
            "((?<=[^A-Za-z0-9])|^)(MON|[Mm]on|TUE|[Tt]ue|WED|[Ww]ed|THU|[Tt]hu|THUR|[Tt]hur|FRI|[Ff]ri|SAT|[Ss]at|SUN|[Ss]un)((?=[^A-Za-z0-9])|$)": "<:DOW:>",
            "((?<=[^A-Za-z0-9])|^)([Jj]an(uary)?|[Ff]eb(ruary)?|[Mm]ar(ch)?|[Aa]pr(il)?|[Mm]ay|[Jj]un(e)?|[Jk]ul(y)?|[Aa]ug(ust)?|[Ss]ep(tember)?|[Oo]ct(ober)?|([Nn]ov|[Dd]ec)(ember)?)((?=[^A-Za-z0-9])|$)": "<:MON:>"
      }

    def __loadStandardRules(self):
        self._standard_rules = {
            "((?<=[^A-Za-z0-9])|^)(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(:[0-9]{0,4}[1-9])?((?=[^A-Za-z0-9])|$)": "<:IP:>",
            "((?<=[^A-Za-z0-9])|^)(0x[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)": "<:HEX:>",
            "((?<=[^A-Za-z0-9])|^)([\\-\\+]?\\d+)((?=[^A-Za-z0-9])|$)": "<:NUM:>",
            "((?<=[^A-Za-z0-9])|^)[0-9]+([Ss]|[Ss]ec|[Ss]ecs|[Ss]econd|[Ss]econds|SEC|SECOND|SECONDS)((?=[^A-Za-z0-9])|$)": "<:SEC:>",
            "((?<=[^A-Za-z0-9])|^)[0-9]+([Nn],[Nn]ano|[Nn]anos|[Nn]anosecond|[Nn]anoseconds|NANO|NANOS|NANOSECOND|NANOSECONDS)((?=[^A-Za-z0-9])|$)": "<:NANO:>",
            "((?<=[^A-Za-z0-9])|^)[0-9]+([Mm],[Mm]ili|[Mm]ilis|[Mm]ilisecond|[Mm]iliseconds|MILI|MILIS|MILISECOND|MILISECONDS)((?=[^A-Za-z0-9])|$)": "<:MILI:>"
            # TODO: Add URLs, Domains, Java Parameters
        }

    def encode(self, data):
        if data is not None:
            for k, v in self._rules.items():
                data = re.sub(k, v, data)
        if self._enableDatetimeRules:
            for k, v in self._datetime_rules.items():
                data = re.sub(k, v, data)
        if self._enableStandardRules:
            for k, v in self._standard_rules.items():
                data = re.sub(k, v, data)
        return data

    def enable_datetime_rules(self, enable_datetime_rules=True):
        self._enableDatetimeRules = enable_datetime_rules

    def enable_standard_rules(self, enable_standard_rules=True):
        self._enableStandardRules = enable_standard_rules

    def add_replace_rule(self, rule=None, replace=None):
        if rule is not None:
            if replace is None:
                replace = ""
            self._rules[rule] = replace
    
    def reset_replace_rules(self):
        self._rules.clear()
