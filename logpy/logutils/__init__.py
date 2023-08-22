from .analyzer import LogAnalyzer

from .logabc import BasicLog
from .network import (
    Network_Patterns,
    QIOpen,
    QIOpenResponse,
    QISend,
    QMTPublish,
    QMTResponse,
)
from .sleep import (
    SleepPatterns,
    Suspend,
    Active,
    SleepCycle,
    Ignition,
)

from .storage import (
    AIS140,
    CVP
)

def add_tcp_logs(la:LogAnalyzer, p):
    la.add_log_type(QIOpen("TCP Port Open", ignore_case=p.ignore_case))
    la.add_log_type(QIOpenResponse("TCP Conn. Response", ignore_case=p.ignore_case))
    la.add_log_type(QISend("TCP Packets", ignore_case=p.ignore_case))

def add_mqtt_logs(la: LogAnalyzer, p):
    la.add_log_type(QMTPublish("MQTT Publish", topics=p.topics, ignore_case=p.ignore_case))
    la.add_log_type(QMTResponse("MQTT Response", ignore_case=p.ignore_case))

def add_sleep_logs(la: LogAnalyzer, p):
    la.add_log_type(Suspend("Going to Sleep", ignore_case=p.ignore_case))
    la.add_log_type(Active("Waking Up", ignore_case=p.ignore_case))
    la.add_log_type(SleepCycle("Sleep Timer Started", ignore_case=p.ignore_case))

def add_ignition_logs(la: LogAnalyzer, p):
    la.add_log_type(Ignition("Ignition", ignore_case=p.ignore_case))

def add_ais_storage_logs(la: LogAnalyzer, p):
    la.add_log_type(AIS140("AIS140", ignore_case=p.ignore_case, log_file_path=p.log_file))
def add_cvp_storage_logs(la: LogAnalyzer, p):
    la.add_log_type(CVP("CVP", ignore_case=p.ignore_case, log_file_path=p.log_file))

MODULE_SUBFUNCTIONS = {
    "network": ["tcp", "mqtt"],
    "sleep": ["ignition", "sleepcycle"],
    "storage": ["ais140", "cvp"]
    }

MODULE_ADDLOG = {
    "network" : {"tcp": add_tcp_logs, "mqtt": add_mqtt_logs},
    "sleep" : {"sleepcycle": add_sleep_logs, "ignition": add_ignition_logs},
    "storage": {"ais140": add_ais_storage_logs, "cvp": add_cvp_storage_logs}
}