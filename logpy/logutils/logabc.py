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
        # se is show_empty
        nCol1 = False # means name in column 1, set to true when 1st time name in columnn 1 is printed
        for k,v in self.result_dict.items():
            if isinstance(v, dict):
                flag = 1 # this for nested dictionary within the value
                for key, val in v.items():
                    if isinstance(val, dict):
                        # table.append([k, key, str(tabulate(val.items(), tablefmt="plain"))])
                        tbl_str = str(tabulate([(key,k1,v1) for (k1,v1) in val.items() if v1 or se], tablefmt="plain"))
                        if len(tbl_str) > 0 or se:
                            table.append(["" if nCol1 else self.name, k, tbl_str])
                            nCol1 = True
                        flag = 0
                    # else:
                    #     if not val:
                    #         continue
                        # table.append([k, key, val])
                if flag:
                    tbl_str = str(tabulate([i for i in v.items() if i[1] or se], tablefmt="plain"))
                    if len(tbl_str) > 0 or se:
                        table.append(["" if nCol1 else self.name, k, tbl_str])
                        nCol1 = True
            else:
                if v or se:
                    table.append(["" if nCol1 else self.name, k, v])
                    nCol1 = True

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
        self.writeToFile = kwargs.get("writeToFile", 0)
    
    def update_counts(self, match):
        """
        Update the counts based on the given match.

        Args:
            match (str): The match to update the counts with.

        Returns:
            int: 1 if want to write to file, else 0.
        """
        return self.writeToFile
    
    def print_summary(self, table, show_empty=False):
        return super().print_summary(table, show_empty)