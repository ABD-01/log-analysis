import re
from typing import Any
from easydict import EasyDict
from tabulate import tabulate

class _BasicLog:
    def __init__(self, name, pattern, **kwargs):
        ignore_case = kwargs.get('ignore_case', False)
        self.name = name
        self.pattern = re.compile(pattern, flags=re.IGNORECASE if ignore_case else 0)
        self.result_dict = EasyDict({"Count": 0})

    def print_summary(self, table, se):
        for k,v in self.result_dict.items():
            if isinstance(v, dict):
                flag = 1
                for key, val in v.items():
                    if isinstance(val, dict):
                        # table.append([k, key, str(tabulate(val.items(), tablefmt="plain"))])
                        tbl_str = str(tabulate([(key,k1,v1) for (k1,v1) in val.items() if v1 or se], tablefmt="plain"))
                        if len(tbl_str) > 0 or se:
                            table.append(["", k, tbl_str])
                        flag = 0
                    # else:
                    #     if not val:
                    #         continue
                        # table.append([k, key, val])
                if flag:
                    tbl_str = str(tabulate([i for i in v.items() if i[1] or se], tablefmt="plain"))
                    if len(tbl_str) > 0 or se:
                        table.append(["", k, tbl_str])
            else:
                if v or se:
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
    def __init__(self, name, pattern, **kwargs):
        super(BasicLog, self).__init__(name, pattern, **kwargs)
        # self.result_dict.Count = 0
    
    def update_counts(self, match):
        # self.result_dict.Count +=1
        return 0
    
    def print_summary(self, table, show_empty=False):
        return super().print_summary(table, show_empty)