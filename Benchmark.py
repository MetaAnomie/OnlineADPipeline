from Detectors.UniqueEvents.UniqueEvents import UniqueEvents
from EncoderDetectorPipeline import EncoderDetectorPipeline
from Encoders.Drain3.Drain3 import Drain3
from Encoders.RegexReplace.RegexReplace import RegexReplace
from Evaluators.HDFSEvaluator import HDFSEvaluator

pipeline = EncoderDetectorPipeline([RegexReplace(),Drain3()], [UniqueEvents()])
evaluator = HDFSEvaluator("Logs/HDFS/Anomalies.csv")

count = 0
with open("Logs/HDFS/HDFS.log", "r") as file:
    for line in file:
        data = line.strip()
        processed = pipeline.process(data)

        anomaly = False
        if processed is not None and len(processed) > 0:
            anomaly = True
            print(processed.strip())

        evaluator.evaluate(data,anomaly)

        count = count + 1
        if count % 100000 == 0: print("Processed: " + str(count))
print(evaluator.get_result_summary())

