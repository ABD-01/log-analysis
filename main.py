import sys
import re
from datetime import datetime
from tqdm import tqdm
from prettytable import PrettyTable


# log_file_path = "logs/RM_05_07_master.log"
# log_file_path = "logs/OVERNIGHT_MASTER_5JUL7.40"
log_file_path = "logs/log2.txt"

if len(sys.argv) > 1:
    log_file_path = sys.argv[1]


total_lines = open(log_file_path).read().count("\n")


reg_patterns = {
    "falcon": r"FALCON",
    "watchdog": r"WATCHDOG",
    "publish": r"\|AT\+QMTPUBEX=(\d+),(\d+),(\d+),\d+,\"(?P<topic>[^\"]+)\"", # \|AT\+QMTPUBEX=(\d+),(\d+),(\d+),\d+,\"(.+\)"
    "response": r"\+QMTPUBEX:\s((?:\d+,)+)(?P<result>\d)" #\+QMTPUBEX: \d+,(\d+),(\d+)
}
patterns = {k:{"pattern":re.compile(p), "count" : 0} for k,p in reg_patterns.items()}

success_counts = 0
failure_count = 0
topic_counts = {}

start_time = None
end_time = None

updlogs = open("analysedlogs/analysedlogs.txt", "w")

with open(log_file_path, 'r') as logs_file:
    for line_no, line in enumerate(tqdm(logs_file, total=total_lines), start=1):
        
        for k,v in patterns.items():
            match = v["pattern"].search(line)
            if match:
                updlogs.write(f"{line_no: 6d} : {match.string}")
                v["count"] += 1

                if k == "publish":
                    topic = match.groupdict()["topic"].split("/")[-1]
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1

                if k == "response":
                    result = int(match.groupdict()["result"])
                    if result == 0:
                        success_counts += 1
                    else:
                        failure_count += 1
                break
        if not start_time:
            start_time = line[1:20]
        end_time = line[1:20]

updlogs.close()

duration = None
if start_time and end_time:
    start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    duration = divmod((end_datetime - start_datetime).total_seconds(), 60)
    hours, minutes = divmod(duration[0] % 1440, 60)
    dur = f"{int(hours)} hrs, {int(minutes)} mins"

print(f"Logs from {start_time} to {end_time}")
# print(f"Logs Duration: {dur}")
tbl = PrettyTable(field_names=["Value", "Count"])
tbl.add_rows(
    [
        ["Duration", dur],
        ["FALCON", patterns["falcon"]["count"]],
        ["WATCHDOG", patterns["watchdog"]["count"]],
        ["AT+QMTPUBEX", patterns["publish"]["count"]],
    ]
)
for k,v in topic_counts.items():
    tbl.add_row([f"Topic: {k}",v])
tbl.add_rows(
    [
        ["+QMTPUBEX", patterns["response"]["count"]],
        ["Publish Success", success_counts],
        ["Publish Failure", failure_count]
    ]
)
print(tbl)
