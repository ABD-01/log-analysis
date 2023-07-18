import re
from datetime import datetime
from tqdm import tqdm
from prettytable import PrettyTable


class LogAnalyzer:
    def _init_(self, log_file_path):
        self.log_file_path = log_file_path
        self.total_lines = None
        self.pattern_counts = {}

    def analyze(self):
        self.total_lines = self.get_total_lines()
        self.process_log_file()

    def get_total_lines(self):
        with open(self.log_file_path, 'r') as file:
            return sum(1 for _ in file)

    def process_log_file(self):
        with open(self.log_file_path, 'r') as logs_file:
            for line_no, line in enumerate(tqdm(logs_file, total=self.total_lines), start=1):
                self.update_pattern_counts(line)

    def update_pattern_counts(self, line):
        raise NotImplementedError()


class FalconLogAnalyzer(LogAnalyzer):
    def _init_(self, log_file_path):
        super()._init_(log_file_path)
        self.pattern_counts = {
            "falcon": 0,
            "watchdog": 0
        }

    def update_pattern_counts(self, line):
        for pattern, regex in self.pattern_counts.items():
            if re.search(pattern, line):
                self.pattern_counts[pattern] += 1


class PublishLogAnalyzer(LogAnalyzer):
    def _init_(self, log_file_path):
        super()._init_(log_file_path)
        self.pattern_counts = {
            "publish": 0
        }
        self.topic_counts = {}

    def update_pattern_counts(self, line):
        if re.search("publish", line):
            self.pattern_counts["publish"] += 1
            topic_match = re.search(r'\"(.+?)\"', line)
            if topic_match:
                topic = topic_match.group(1)
                self.topic_counts[topic] = self.topic_counts.get(topic, 0) + 1


class ResponseLogAnalyzer(LogAnalyzer):
    def _init_(self, log_file_path):
        super()._init_(log_file_path)
        self.pattern_counts = {
            "response": 0
        }
        self.success_count = 0
        self.failure_count = 0

    def update_pattern_counts(self, line):
        if re.search("response", line):
            self.pattern_counts["response"] += 1
            result_match = re.search(r"\+QMTPUBEX: \d+,(\d+),(\d+)", line)
            if result_match:
                result = int(result_match.group(2))
                if result == 0:
                    self.success_count += 1
                else:
                    self.failure_count += 1


# Usage example:
log_file_path = "log.txt"

analyzers = [
    FalconLogAnalyzer(log_file_path),
    PublishLogAnalyzer(log_file_path),
    ResponseLogAnalyzer(log_file_path)
]

for analyzer in analyzers:
    analyzer.analyze()

    print(f"Log File: {log_file_path}")
    print("Pattern Counts:")
    for pattern, count in analyzer.pattern_counts.items():
        print(f"{pattern}: {count}")

    if isinstance(analyzer, PublishLogAnalyzer):
        print("Topic Counts:")
        for topic, count in analyzer.topic_counts.items():
            print(f"{topic}: {count}")

    if isinstance(analyzer, ResponseLogAnalyzer):
        print(f"Success Count: {analyzer.success_count}")
        print(f"Failure Count: {analyzer.failure_count}")

    print("\n")