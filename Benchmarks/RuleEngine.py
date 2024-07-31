import os
from os.path import exists
from Detectors.RuleEngine.RuleEngine import RuleEngine
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Evaluators.HDFSEvaluator import HDFSEvaluator
from Evaluators.OneToOneEvaluator import OneToOneEvaluator

results = "results.txt"
if os.path.isfile(results):
    os.remove(results)


def debug(msg):
    if msg is not None:
        dbg_log = open(results, "a")
        dbg_log.write(msg + "\n")
        print(msg + "\n")
        dbg_log.close()


ruleEngine = RuleEngine()
ruleEngine.add_keyword_rules(keywords=["failed","exception","error"],case_insensitive=True)
pipeline = EncoderDetectorPipeline(encoders=[RegexReplace()], detectors=[ruleEngine])

# HDFS Benchmarking
log = "../Logs/HDFS/HDFS.log"
evaluator = HDFSEvaluator('../Logs/HDFS/Anomalies.csv')
debug("\nRule Engine (Token) / HDFS Dataset:")

if log is not None and exists(log):
    with open(log) as file:
        for line in file:
            res = pipeline.process(line.strip())
            if res is not None:
                evaluator.evaluate(line.strip(), True)
            else:
                evaluator.evaluate(line.strip(), False)

debug(evaluator.get_result_summary())

# BGL Benchmarking
log = "../Logs/BGL/BGL.log"
evaluator = OneToOneEvaluator()
debug("\nRule Engine (Token) / BGL Dataset:")

if log is not None and exists(log):
    with open(log, encoding="utf-8") as file:
        for line in file:

            line = line.split(" ", 1)
            ground_truth = False
            if line[0] != "-":
                ground_truth = True

            res = pipeline.process(line[1].strip())
            if res is not None:
                evaluator.evaluate(line[1].strip(), True, ground_truth)
            else:
                evaluator.evaluate(line[1].strip(), False, ground_truth)

debug(evaluator.get_result_summary())
