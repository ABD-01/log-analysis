from utils.args import Parser
from utils.logutils import LogAnalyzer
from utils.logutils import BasicLog, QMTPublish, QMTResponse, QIOpen, QIOpenResponse, QISend, Ignition, Active, SleepCycle, Suspend

def main(args):
    log_analyzer = LogAnalyzer(args)

    if args.all:
        args.tcp = True
        args.mqtt = True

    if args.module == "networks" or args.all:
        if args.tcp:
            log_analyzer.add_log_type(QIOpen("TCP Port Open"))
            log_analyzer.add_log_type(QIOpenResponse("TCP Conn. Response"))
            log_analyzer.add_log_type(QISend("TCP Packets"))
        
        if args.mqtt:
            log_analyzer.add_log_type(QMTPublish("MQTT Publish"))
            log_analyzer.add_log_type(QMTResponse("MQTT Response"))
    
    if args.module == "sleep" or args.all:
        log_analyzer.add_log_type(Suspend("Going to Sleep"))
        log_analyzer.add_log_type(Active("Waking Up"))
        log_analyzer.add_log_type(SleepCycle("Sleep Timer Started"))
        log_analyzer.add_log_type(Ignition("Ignition"))

    for kw in args.key_words:
        log_analyzer.add_log_type(BasicLog(kw, kw))


    log_analyzer.analyze()
    log_analyzer.print_summary()



if __name__ == '__main__':
    parser = Parser()
    args = parser.parse_args()
    main(args)