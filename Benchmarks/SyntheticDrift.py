import os
from os.path import exists
from Detectors.DeepLog.DeepLog import DeepLog
from Detectors.RuleEngine.RuleEngine import RuleEngine
from Detectors.UniqueEvents.UniqueEvents import UniqueEvents
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.Drain3.Drain3 import Drain3
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Evaluators.OneToOneEvaluator import OneToOneEvaluator

path = "../Logs/SyntheticDrift/"
results = "results.txt"
if os.path.isfile(results):
    os.remove(results)

logs = ["Control.log",
        "New.log",
        "AlteredParameter.log",
        "AlteredTemplate.log",
        "Removed.log",
        "Sequence.log",
        "Timing.log"]

def debug(msg):
    if msg is not None:
        file = open(results, "a")
        file.write(msg + "\n")
        print(msg + "\n")
        file.close()

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
    debug(evaluator.get_result_summary())

evaluator = OneToOneEvaluator(path + 'Anomalies.csv')

for log in logs:
    log_path = path + log

    debug("\n" + log + " | Rule Engine (Token):")
    ruleEngine = RuleEngine()
    ruleEngine.add_keyword_rules(keywords=["failed","exception","error"],case_insensitive=True)
    pipeline = EncoderDetectorPipeline(encoders=[RegexReplace()], detectors=[ruleEngine])
    execute_benchmark(log_path, evaluator, pipeline)

    debug("\n" + log + " | Unique Event Detector:")
    ued = UniqueEvents(training_records=40)
    pipeline = EncoderDetectorPipeline(encoders=[RegexReplace(),Drain3(encode_to_indices=True ,sim_th=0.6)], detectors=[ued])
    execute_benchmark(log_path, evaluator, pipeline)

    debug("\n" + log + " | LSTM:")
    deeplog = DeepLog(training_records=40,epochs=5000)
    pipeline = EncoderDetectorPipeline(encoders=[RegexReplace(),Drain3(encode_to_indices=True,sim_th=0.6)], detectors=[deeplog])
    execute_benchmark(log_path, evaluator, pipeline)
