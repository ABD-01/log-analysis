import os
import re
from datetime import datetime
import argparse
from tqdm import tqdm
from prettytable import PrettyTable


class LogAnalyzer:
    def __init__(self, args):
        self.log_file_path = args.log_file
        self.total_lines = self.get_total_lines
        self.log_types = []
        self.ignore_case = args.ignore_case
        self.start_time = None
        self.end_time = None

        if args.out_file:
            self.out_log_file_path = args.out_file
        else:
            self.out_log_file_path = "analysedlogs/" + "out_" + str(os.path.basename(args.log_file))
        self.out_log_file = open(self.out_log_file_path, "w")

    def add_log_type(self, logtype, *args, **kwargs):
        if logtype == "res":
            self.log_types.append(ResponseType(*args, **kwargs))
        elif logtype == "pub":
            self.log_types.append(PublishType(*args, **kwargs))
        else:
            self.log_types.append(LogType(*args, **kwargs))

    def get_total_lines(self):
        with open(self.log_file_path, 'r') as file:
            return sum(1 for _ in file)
        # return open(self.log_file_path).read().count("\n")

    def analyze(self):
        with open(self.log_file_path, 'r') as logs_file:
            for line_no, line in enumerate(tqdm(logs_file, total=self.total_lines()), start=1):
            # for line_no, line in enumerate(logs_file, start=1):
                self.update_counts(line_no, line)
        self.out_log_file.close()

    def update_counts(self, line_no, line):
        for log_type in self.log_types:
            if self.ignore_case:
                match = log_type.pattern.search(line.upper())
            else:
                match = log_type.pattern.search(line)

            if match:
                log_type.count += 1
                self.out_log_file.write(f"{line_no: 6d} : {match.string}")

                if hasattr(log_type, "update_counts"):
                    log_type.update_counts(match)
                break

        if not self.start_time:
            self.start_time = line[1:20]
        if len(line) > 21:
            self.end_time = line[1:20]

    def calculate_duration(self):
        if self.start_time and self.end_time:
            start_datetime = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(self.end_time, '%Y-%m-%d %H:%M:%S')
            duration = divmod((end_datetime - start_datetime).total_seconds(), 60)
            hours, minutes = divmod(duration[0] % 1440, 60)
            return f"{int(hours)} hrs, {int(minutes)} mins"
        return None

    def print_summary(self):
        print(f"Logs from {self.start_time} to {self.end_time}")
        tbl = PrettyTable(field_names=["Value", "Count"])
        tbl.add_row(["duration", self.calculate_duration()])
        for log_type in self.log_types:
            log_type.print_summary(tbl)

        print(tbl)


class LogType:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = re.compile(pattern)
        self.count = 0
    def print_summary(self, table):
        table.add_row([self.name, self.count])

class PublishType(LogType):
    def __init__(self, name, pattern=r'\|AT\+QMTPUBEX=(\d+),(\d+),(\d+),\d+,\"(?P<topic>[^\"]+)\"', topics=[]):
        super(PublishType, self).__init__(name, pattern)
        self.topics = topics
        self.topic_counts = {}

    def update_counts(self, match):
        topic = match.groupdict()["topic"].split("/")[-1]
        if not self.topics or topic in self.topics:
            self.topic_counts[topic] = self.topic_counts.get(topic, 0) + 1
    
    def print_summary(self, table):
        table.add_row([self.name, self.count])
        if len(self.topic_counts) < 1:
            return
        for k,v in self.topic_counts.items():
            table.add_row([f"Topic: {k}", v])

class ResponseType(LogType):
    def __init__(self, name, pattern):
        super(ResponseType, self).__init__(name, pattern)
        self.success_count = 0
        self.failure_count = 0

    def update_counts(self, match):
        result = int(match.groupdict()["result"])
        if result == 0:
            self.success_count += 1
        else:
            self.failure_count += 1
            print(match.string)
    
    def print_summary(self, table):
        table.add_rows([
            [self.name, self.count],
            ["Publish Success", self.success_count],
            ["Publish Failure", self.failure_count]
        ])


def main(args):
    log_analyzer = LogAnalyzer(args)

    # log_analyzer.add_log_type("log", "falcon", r"FALCON")
    # log_analyzer.add_log_type("log", "watchdog", r"WATCHDOG")
    for kw in args.key_words:
        if args.ignore_case:
            log_analyzer.add_log_type("log", kw, rf"{kw.upper()}")
        else:
            log_analyzer.add_log_type("log", kw, rf"{kw}")
    if args.ignore_case and args.topics:
        args.topics = [t.upper() for t in args.topics]
    log_analyzer.add_log_type("pub", "publish", r'\|AT\+QMTPUBEX=(\d+),(\d+),(\d+),\d+,\"(?P<topic>[^\"]+)\"', args.topics)
    log_analyzer.add_log_type("res", "response", r'\+QMTPUBEX:\s((?:\d+,)+)(?P<result>\d)')

    log_analyzer.analyze()
    log_analyzer.print_summary()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Log Analysis")
    parser.add_argument("-l", "--log_file", type=str, help="Path to log file", default="logs/log2.txt", required=True)
    parser.add_argument("-o", "--out_file", type=str, help="Path to output log file")
    parser.add_argument("-k", "--key_words", nargs='*', default=["FALCON", "WATCHDOG"])
    parser.add_argument("-t", "--topics", nargs='*', default=[])
    parser.add_argument("-c", "--ignore_case", type=int, default=0, choices=[0,1], help="Toggle Match Case")
    args = parser.parse_args()
    main(args)


# sleep timer started
# DIGITAL IGN 0
# detect lag
# (GSM_TX).*(\s)+.*(\s)+.*(SEND OK)