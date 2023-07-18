import re

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
    
    def print_summary(self, table):
        table.add_rows([
            [self.name, self.count],
            ["Publish Success", self.success_count],
            ["Publish Failure", self.failure_count]
        ])
