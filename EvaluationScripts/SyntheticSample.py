from os.path import exists

from Detectors.DeepLog.DeepLog import DeepLog
from Detectors.RuleEngine.RuleEngine import RuleEngine
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.Drain3.Drain3 import Drain3
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Evaluators.OneToOneEvaluator import OneToOneEvaluator

regexReplace = RegexReplace()
ruleEngine = RuleEngine()
ruleEngine.add_keyword_rules(keywords=["failed","exception","error"],case_insensitive=True)

pipeline = EncoderDetectorPipeline(encoders=[regexReplace], detectors=[ruleEngine])
evaluator = OneToOneEvaluator('../Logs/SyntheticSample/Anomalies.csv')
log = '../Logs/SyntheticSample/SyntheticSample.log'

print("\nEvaluate Rule Engine on Synthetic Sample:\n")

if log is not None and exists(log):
    with open(log) as file:
        for line in file:
            res = pipeline.process(line.strip())
            if res is not None and len(res) > 0:
                evaluator.evaluate(line.strip(),True)
            else:
                evaluator.evaluate(line.strip(),False)

print(evaluator.get_result_summary())

print("\nEvaluate LSTM on Synthetic Sample:\n")

deeplog = DeepLog(training_records=1000)
pipeline = EncoderDetectorPipeline(encoders=[Drain3(encode_to_indices=True)], detectors=[deeplog])
if log is not None and exists(log):
    with open(log) as file:
        for line in file:
            res = pipeline.process(line.strip())
            if res is not None and len(res) > 0:
                evaluator.evaluate(line.strip(),True)
            else:
                evaluator.evaluate(line.strip(),False)

#print(evaluator.get_result_summary())