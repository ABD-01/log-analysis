import re
from typing import Any
from easydict import EasyDict
from tabulate import tabulate

class _BasicLog:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = re.compile(pattern)
        self.result_dict = EasyDict({"Count": 0})

    def print_summary(self, table):
        for k,v in self.result_dict.items():
            if isinstance(v, dict):
                for key, val in v.items():
                    if isinstance(val, dict):
                        table.append([k, key, str(tabulate(val.items(), tablefmt="plain"))])
                    else:
                        table.append([k, key, val])
            else:
                table.append([self.name, k, v])

    def __call__(self, line):
        match = self.pattern.search(line)
        if match is None:
            return -1
        self.result_dict.Count += 1
        return self.update_counts(match)
    
    
    def update_counts(self, match):
        raise NotImplementedError

class BasicLog(_BasicLog):
    def __init__(self, name, pattern):
        super(BasicLog, self).__init__(name, pattern)
        # self.result_dict.Count = 0
    
    def update_counts(self, match):
        # self.result_dict.Count +=1
        return 0
    
    def print_summary(self, table):
        return super().print_summary(table)