import os
import time


def follow_file(input_file, from_end=True):
    if from_end:
        input_file.seek(0, os.SEEK_END)
    if input_file is not None:
        while True:
            line = input_file.readline()
            if not line:
                time.sleep(1)
                continue
            yield line
