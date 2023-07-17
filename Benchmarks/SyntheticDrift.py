from os.path import exists

from Detectors.DeepLog.DeepLog import DeepLog
from Detectors.RuleEngine.RuleEngine import RuleEngine
from Detectors.UniqueEvents.UniqueEvents import UniqueEvents
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.Drain3.Drain3 import Drain3
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Evaluators.OneToOneEvaluator import OneToOneEvaluator

def execute_benchmark(log, evalutor, pipeline):
    evaluator.reset()
    if log is not None and exists(log):
        with open(log) as file:
            for line in file:
                res = pipeline.process(line.strip())
                if res is not None:
                    evaluator.evaluate(line.strip(), True)
                else:
                    evaluator.evaluate(line.strip(), False)
    print(evaluator.get_result_summary())

evaluator = OneToOneEvaluator('../Logs/SyntheticDrift/Anomalies.csv')
log = '../Logs/SyntheticDrift/Control.log'

ruleEngine = RuleEngine()
ruleEngine.add_keyword_rules(keywords=["failed","exception","error"],case_insensitive=True)
pipeline = EncoderDetectorPipeline(encoders=[RegexReplace()], detectors=[ruleEngine])
print("\nEvaluate: Rule Engine | Control Sample:\n")
execute_benchmark(log, evaluator, pipeline)

print("\nEvaluate: Unique Event Detector | Control Sample:\n")
ued = UniqueEvents(training_records=40)
pipeline = EncoderDetectorPipeline(encoders=[RegexReplace(),Drain3(encode_to_indices=True)], detectors=[ued])
execute_benchmark(log, evaluator, pipeline)

print("\nEvaluate: LSTM | Control Sample:\n")
deeplog = DeepLog(training_records=40)
pipeline = EncoderDetectorPipeline(encoders=[RegexReplace(),Drain3(encode_to_indices=True)], detectors=[deeplog])
execute_benchmark(log, evaluator, pipeline)
