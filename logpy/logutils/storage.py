from easydict import EasyDict
from .logabc import BasicLog
import pandas as pd
import os.path as osp
from os import makedirs


StoragePatters = EasyDict()
StoragePatters.AIS140 = r"Insert \[3:/AIS140/Primary/\d+/\d+/\d+/(?P<id>\d+)]\sin\s(?P<time>\d+)\sms"
StoragePatters.CVP = r"File 3:/History/TMLCVP/PVT/\d+/\d+/\d+/(?P<id>\d+)\s\[TMLCVP Insert for \d+B data took (?P<time>\d+) ms.\]"



class Storage(BasicLog):
    def __init__(self, name, pattern, **kwargs):
        super(Storage, self).__init__(name, pattern, **kwargs)
        self.log_file_path = kwargs.get("log_file_path", None)
        self.dfList = []

    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        self.dfList.append([int(matchdict.id), float(matchdict.time)])
        if self.name == "CVP":
            return 1 # write to file
    
    def makedirs(self, log_file_path, name): 
        if log_file_path is None:
            return name
        input_directory, basename = osp.split(log_file_path)
        out_file_path = osp.join(input_directory, "storagelogs", basename + '_' + name + ".csv")
        makedirs(osp.join(input_directory, "storagelogs"), exist_ok=True)
        return out_file_path

    def save_to_csv(self):
        # save pd to csv
        out_file_path = self.makedirs(self.log_file_path, self.name)
        self.df = pd.DataFrame(self.dfList, columns=['id', 'time'])
        self.df.to_csv(out_file_path, index=False)

    def print_summary(self, table, show_empty=False):
        # Minor Chnages before parent method is called
        self.save_to_csv()
        self.result_dict.summary = EasyDict()
        summary = self.result_dict.summary
        summary.average = self.df.time.mean()
        summary.median = self.df.time.median()
        summary.min = self.df.time.min()
        summary.max = self.df.time.max()
        # now call the super print summary
        return super().print_summary(table, show_empty)

def AIS140(name, pattern=StoragePatters.AIS140, **kwargs):
    return Storage(name, pattern, **kwargs)


def CVP(name, pattern=StoragePatters.CVP, **kwargs):
    return Storage(name, pattern, **kwargs)