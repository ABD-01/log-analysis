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

MODULE_SUBFUNCTIONS = {
    "network": ["tcp", "mqtt"],
    "sleep": ["ignition", "sleepcycle"]
    }

MODULE_ADDLOG = {
    "network" : {"tcp": add_tcp_logs, "mqtt": add_mqtt_logs},
    "sleep" : {"sleepcycle": add_sleep_logs, "ignition": add_ignition_logs}
}