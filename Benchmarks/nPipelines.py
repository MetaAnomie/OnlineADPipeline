import os
from Evaluators.OneToOneEvaluator import OneToOneEvaluator
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.Drain3.Drain3 import Drain3
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Detectors.UniqueEvents.UniqueEvents import UniqueEvents

results = "results.txt"
if os.path.isfile(results):
    os.remove(results)


def debug(msg):
    if msg is not None:
        dbg_log = open(results, "a")
        dbg_log.write(msg + "\n")
        print(msg + "\n")
        dbg_log.close()


cycle_period = 20

# Single Pipeline ---->

pipeline = EncoderDetectorPipeline(
    encoders=[RegexReplace(),Drain3(encode_to_indices=True, sim_th=0.8, training_records=cycle_period)],
    detectors=[UniqueEvents(training_records=cycle_period)])
evaluator = OneToOneEvaluator('../Logs/SyntheticDrift/Anomalies.csv')

debug("-- Single Pipeline --");
with open("../Logs/SyntheticDrift/all.log") as file:
    for line in file:
        res = pipeline.process(line.strip())
        if res is not None:
            evaluator.evaluate(line.strip(), True)
        else:
            evaluator.evaluate(line.strip(), False)

debug(evaluator.get_result_summary())

# Dual Pipeline ---->

evaluator.reset()
pipeline_1 = EncoderDetectorPipeline(
    encoders=[RegexReplace(),Drain3(encode_to_indices=True, sim_th=0.8, training_records=cycle_period)],
    detectors=[UniqueEvents(training_records=cycle_period)])
pipeline_2 = EncoderDetectorPipeline(
    encoders=[RegexReplace(),Drain3(encode_to_indices=True, sim_th=0.8, training_records=cycle_period)],
    detectors=[UniqueEvents(training_records=cycle_period)])

debug("-- Dual Pipeline --");
with open("../Logs/SyntheticDrift/all.log") as file:

    line_num = 0
    active_pipeline = 1

    for line in file:
        line_num += 1

        if line_num != 0 and line_num % cycle_period == 1:
            if active_pipeline == 1:
                pipeline_1.retrain(cycle_period)
                active_pipeline = 2
            else:
                pipeline_2.retrain(cycle_period)
                active_pipeline = 1

        res1 = pipeline_1.process(line.strip())
        res2 = pipeline_2.process(line.strip())

        if res1 is None and res2 is None:
            evaluator.evaluate(line.strip(), False)
        else:
            evaluator.evaluate(line.strip(), True)

    debug(evaluator.get_result_summary())
