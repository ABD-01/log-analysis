from .logabc import BasicLog
from easydict import EasyDict

Network_Patterns = EasyDict()
Network_Patterns.MQTT_Publish = r"AT\+QMTPUBEX=(?P<client_id>\d),(?P<msg_id>\d+),(?P<qos>\d),(?P<retain>\d),\"(?P<topic>.+)\",(?P<msg_lenght>\d+)"
Network_Patterns.MQTT_PubResponse = (r"\+QMTPUBEX: (?P<client_id>\d),(?P<msg_id>\d+),(?P<result>\d)")
Network_Patterns.TCPOpen = r"AT\+QIOPEN=(?P<context_id>\d+),(?P<connect_id>\d+),\"(?P<service_type>\w+)\",\"(?P<ip_address>[^\"]+)\",(?P<remote_port>\d+)"
Network_Patterns.TCPOpenResponse = r"\+QIOPEN: (?P<connect_id>\d+),(?P<err>\d+)"
Network_Patterns.Packets = r"(?P<Gov>\$1,)|(?P<Emergency>\$EPM,)|(?P<Accolade>55AA,)"


class QMTPublish(BasicLog):
    def __init__(
        self,
        name,
        pattern=Network_Patterns.MQTT_Publish,
        topics=[],
    ):
        super(QMTPublish, self).__init__(name, pattern)
        self.topics = topics
        self.result_dict.topic = EasyDict()

    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        # client_id = int(matchdict.clien_id)
        # msg_id = int(matchdict.msg_id)
        # qos = int(matchdict.qos)
        # retain = int(matchdict.retain)
        topic = matchdict.topic.split("/")[-1]
        # msg_len = int(matchdict.msg_lenght)

        if not self.topics or topic in self.topics:
            self.result_dict.topic[topic] = self.result_dict.topic.get(topic, 0) + 1

        return 0


class QMTResponse(BasicLog):
    def __init__(self, name, pattern=Network_Patterns.MQTT_PubResponse):
        super(QMTResponse, self).__init__(name, pattern)
        self.result_dict.QMTsuccess = 0
        self.result_dict.QMTfailure = 0

    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        # client_id = int(matchdict.client_id)
        # msg_id = int(matchdict.msg_id)
        result = int(matchdict.result)

        if result == 0:
            self.result_dict.QMTsuccess += 1
            return 0

        self.result_dict.QMTfailure += 1
        return 1


class QIOpen(BasicLog):
    def __init__(self, name, pattern=Network_Patterns.TCPOpen):
        super(QIOpen, self).__init__(name, pattern)
        self.result_dict.OpenAttempt = EasyDict(
            {f"Id{i}": 0 for i in range(3)}
        )  # HARDCODED as number of tcp connections is known to be 3

    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        # context_id = int(matchdict.context_id)
        connect_id = matchdict.connect_id
        # service_type = matchdict.service_type
        # ip_address = matchdict.ip_address
        # remote_port = int(matchdict.remote_port)

        self.result_dict.OpenAttempt["Id" + str(connect_id)] += 1
        return 0


class QIOpenResponse(BasicLog):
    def __init__(self, name, pattern=Network_Patterns.TCPOpenResponse):
        super(QIOpenResponse, self).__init__(name, pattern)
        self.result_dict.TCPresponse = EasyDict(
            {f"Id{i}": EasyDict(Total=0, Success=0, Failure=0) for i in range(3)}
        )  # HARDCODED as number of tcp connections is known to be 3

    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        connect_id = matchdict.connect_id
        err = int(matchdict.err)

        response = self.result_dict.TCPresponse[f"Id{connect_id}"]
        response.Total += 1
        if err == 0:
            response.Success += 1
        else:
           response.Failure += 1 
        return 0


class QISend(BasicLog):
    def __init__(self, name, pattern=Network_Patterns.Packets):
        super(QISend, self).__init__(name, pattern)
        self.result_dict.PacketsSend = EasyDict(
            {"Gov":0, "Emergency":0, "Accolade":0}
        )
    
    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        if matchdict.Gov:
            self.result_dict.PacketsSend.Gov += 1
        elif matchdict.Emergency:
            self.result_dict.PacketsSend.Emergency += 1
        elif matchdict.Accolade:
            self.result_dict.PacketsSend.Accolade += 1
        
        return 0