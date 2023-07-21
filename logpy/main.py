import warnings
from .utils import Parser
from .logutils import LogAnalyzer
from .logutils import (
    BasicLog,
    QMTPublish,
    QMTResponse,
    QIOpen,
    QIOpenResponse,
    QISend,
    Ignition,
    Active,
    SleepCycle,
    Suspend,
)

def add_tcp_logs(la:LogAnalyzer, p):
    la.add_log_type(QIOpen("TCP Port Open", ignore_case=p.ignore_case))
    la.add_log_type(QIOpenResponse("TCP Conn. Response", ignore_case=p.ignore_case))
    la.add_log_type(QISend("TCP Packets", ignore_case=p.ignore_case))

def add_mqtt_logs(la: LogAnalyzer, p):
    la.add_log_type(QMTPublish("MQTT Publish", topics=p.topics, ignore_case=p.ignore_case))
    la.add_log_type(QMTResponse("MQTT Response", ignore_case=p.ignore_case))


def main():
    parser = Parser()
    p = parser.parse_args()

    log_analyzer = LogAnalyzer(p)

    if p.all:
        p.tcp = True
        p.mqtt = True

    if p.module == "network" or p.all:
        if p.tcp:
            add_tcp_logs(log_analyzer, p)

        if p.mqtt:
            add_mqtt_logs(log_analyzer, p)
        
        if not any(vars(p)[flag] for flag in ["tcp", "mqtt"]):
           add_tcp_logs(log_analyzer, p)
           add_mqtt_logs(log_analyzer, p)

    if p.module == "sleep" or p.all:
        log_analyzer.add_log_type(Suspend("Going to Sleep", ignore_case=p.ignore_case))
        log_analyzer.add_log_type(Active("Waking Up", ignore_case=p.ignore_case))
        log_analyzer.add_log_type(SleepCycle("Sleep Timer Started", ignore_case=p.ignore_case))
        log_analyzer.add_log_type(Ignition("Ignition", ignore_case=p.ignore_case))

    for kw in p.keywords:
        log_analyzer.add_log_type(BasicLog(kw, kw, ignore_case=p.ignore_case))
    
    if p.regex:
        warning_msg = "Warning: --regex argument is not implemented yet. It will be added in a future update."
        warnings.warn(warning_msg, category=FutureWarning)

    log_analyzer.analyze()
    log_analyzer.print_summary()


if __name__ == "__main__":
    parser = Parser()
    args = parser.parse_args()
    main(args)
