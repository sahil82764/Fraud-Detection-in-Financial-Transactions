import logging
from datetime import datetime
import os
import pandas as pd
from fraudTransaction.constant import get_current_time_stamp

logDir = "projectLogs"

def get_log_file_name():
    return f"log_{get_current_time_stamp}.log"

logFileName = get_log_file_name()

os.makedirs(logDir, exist_ok=True)

logFilePath = os.path.join(logDir,logFileName)


logging.basicConfig(filename=logFilePath, filemode="w", format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcname)s()^;%(message)s', level=logging.INFO)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns = ["Timestamp", "Log Level", "line number", "file name", "function name", "message"]
    log_df.columns = columns

    log_df["log message"] = log_df['Timestamp'].astype(str)+":$"+log_df['message']

    return log_df[["log message"]]