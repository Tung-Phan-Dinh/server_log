import pandas as pd
import numpy as np
import re
from datetime import datetime

import pandas as pd
import re
from datetime import datetime

class LogTransform:
    def __init__(self, source_path):
        """
        Initialize the LogTransform with source paths.

        :param source_path: Path to the raw log file
        """
        self.source_path = source_path
        self.log_pattern = None

    def read_log_file(self, regex_exp):
        """
        Read and parse the log file based on the defined pattern.

        :param regex_exp: Regex expression of logs
        :return: List of parsed log entries as dictionaries
        """
        # Define the log pattern for parsing
        self.log_pattern = regex_exp

        with open(self.source_path, 'r') as file:
            log_lines = file.readlines()
            parsed_logs = [
                re.match(self.log_pattern, line).groupdict()
                for line in log_lines if re.match(self.log_pattern, line)
            ]
        print(f"Parsed {len(parsed_logs)} log entries.")
        return pd.DataFrame(parsed_logs)

    def transform(self, parsed_logs):
        """
        Transform parsed logs into a structured DataFrame and preprocess the data.

        :param parsed_logs: List of parsed log entries as dictionaries
        :return: Preprocessed DataFrame
        """
        df = parsed_logs
        df['std'] = df['std'].replace({'stdout': 0, 'stderr': 1})
        df = df.drop(['remote_user', 'header'], axis=1)
        df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z"))
        df['method'] = df['method'].replace({'GET': 0, 'POST': 1})
        df['bytes_sent'] = pd.to_numeric(df['bytes_sent'], errors='coerce')
        df['status'] = pd.to_numeric(df['status'], errors='coerce')
        df['day'] = df['datetime'].dt.day
        df['hour'] = df['datetime'].dt.hour
        df['month'] = df['datetime'].dt.month
        return df
# # Example usage
# if __name__ == "__main__":
#     source_path = r"/Users/phamthiphuongthuy/Desktop/Intern/server_log/data/server-log.txt"
#     destination_path = r"/Users/phamthiphuongthuy/Desktop/Intern/server_log/data/parsed_logs.csv"
#     log_pattern= r'^\S+ (?P<std>\S+) \S+ (?P<remote_address>\d+\.\d+\.\d+\.\d+) - (?P<remote_user>[^ ]*) \[(?P<datetime>[^\]]+)\] "(?P<method>\w+) (?P<path>[^\s]+) (?P<header>[^\"]+)" (?P<status>\d+) (?P<bytes_sent>\d+) "(?P<referer>[^\"]*)" "(?P<user_agent>[^\"]*)"'
#     transformer = LogTransform(source_path)
#     df = transformer.read_log_file(log_pattern)
#     df = transformer.transform(df)
#     df.to_csv(destination_path)
