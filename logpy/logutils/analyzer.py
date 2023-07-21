from datetime import datetime
from os import mkdir
import os.path as osp
from tabulate import tabulate

from .logabc import BasicLog

class LogAnalyzer:
    def __init__(self, args):
        self.log_file_path = args.log_file
        self.logslist = []
        self.ignore_case = args.ignore_case
        self.disable_progresslive = args.disable_progresslive
        self.output = ""
        
        self.total_lines = 0
        self.start_time = None
        self.end_time = None

        if args.out_file:
            self.out_log_file_path = args.out_file
        else:
            if not osp.exists("analysedlogs"):
                mkdir("analysedlogs")
            self.out_log_file_path = "analysedlogs/" + "out_" + str(osp.basename(args.log_file))
        self.out_log_file = open(self.out_log_file_path, "w", encoding='utf-8')

    def add_log_type(self, logtype:BasicLog):
            self.logslist.append(logtype)

    def get_total_lines(self):
        with open(self.log_file_path, 'r') as file:
            self.total_lines= sum(1 for _ in file)
            return self.total_lines
        # return open(self.log_file_path).read().count("\n")

    def analyze(self):
        with open(self.log_file_path, 'r') as logs_file:

            if self.disable_progresslive:
                loader = logs_file
            else:
                from tqdm import tqdm
                loader = tqdm(logs_file, total=self.get_total_lines())

            for line_no, line in enumerate(loader, start=1):
                for logtype in self.logslist:
                    # output = logtype(line, flags = re.I if self.ignore_case else 0)
                    output = logtype(line)

                    if output == 0:
                        break

                    if output == 1:
                        self.out_log_file.write(f"{line_no: 6d} : {line}")
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

    def print_summary(self, show_empty=False):
        print(f"Log File: {self.log_file_path}")
        print(f"Logs from {self.start_time} to {self.end_time}")
        tbl = [["Name", "Value", "Count"]]
        tbl.append(["Duration of Log File", "", self.calculate_duration()])
        for l in self.logslist:
            l.print_summary(tbl, show_empty)

        self.output = str(tabulate(tbl, headers="firstrow", tablefmt='fancy_grid', ))
        self.out_log_file.write(f'\n\n{"="*100}\nSummary:\n')
        self.out_log_file.write(self.output)
        self.out_log_file.close()
        print(self.output)