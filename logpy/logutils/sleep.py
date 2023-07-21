from datetime import datetime
from .logabc import BasicLog
from easydict import EasyDict

SleepPatterns = EasyDict()
SleepPatterns.Suspend = r"synchronized suspend ok"
SleepPatterns.Active = r"all tasks active"
SleepPatterns.SleepCycle = r"sleep timer started"
SleepPatterns.IGN = r"IGN (?P<status>\d)"


def Suspend(name, pattern=SleepPatterns.Suspend, **kwargs):
    return BasicLog(name, pattern, **kwargs)

def Active(name, pattern=SleepPatterns.Active, **kwargs):
    return BasicLog(name, pattern, **kwargs)

def SleepCycle(name, pattern=SleepPatterns.SleepCycle, **kwargs):
    return BasicLog(name, pattern, **kwargs)


class Ignition(BasicLog):
    def __init__(self, name, pattern=SleepPatterns.IGN, **kwargs):
        super(Ignition, self).__init__(name, pattern, **kwargs)
        self.result_dict.IGN = EasyDict(
            {'IGN_ON1': EasyDict(start=None),    #{ 'IGN_ON1': EasyDict(start=None, duration=None),
             'IGN_OFF1': EasyDict(start=None)}  # 'IGN_OFF1': EasyDict(start=None, duration=None)}
        )
        self.previous_status = -1
        self.on_counter = 1
        self.off_counter = 1
    
    # def time_difference(self, start_time, end_time):
    #     if start_time is None:
    #         return '0'
    #     start_time = datetime.strp(start_time,"%d %B %H:%M")
    #     duration = end_time - start_time
    #     hours = duration.seconds // 3600
    #     minutes = (duration.seconds % 3600) // 60
    #     return f"{hours}hrs {minutes}mins"
    
    def update_counts(self, match):
        status = int(match.group('status'))
        start_time = datetime.strptime(match.string[1:20], '%Y-%m-%d %H:%M:%S')

        if status == self.previous_status:
            return 0
        
        self.previous_status = status
        self.result_dict.IGN[f"IGN_OFF{self.off_counter}"] = self.result_dict.IGN.get(f"IGN_OFF{self.off_counter}",  EasyDict(start=None))
        self.result_dict.IGN[f"IGN_ON{self.on_counter}"] = self.result_dict.IGN.get(f"IGN_ON{self.on_counter}",  EasyDict(start=None)) 

        IgnOff = self.result_dict.IGN[f"IGN_OFF{self.off_counter}"]
        IgnOn = self.result_dict.IGN[f"IGN_ON{self.on_counter}"]

        if status == 0:
            IgnOff.start = start_time.strftime("%d %B %H:%M:%S") 
            # IgnOn.duration = self.time_difference(IgnOn.start, start_time)
            self.off_counter += 1
        elif status == 1:
            IgnOn.start = start_time.strftime("%d %B %H:%M:%S")
            # IgnOff.duration = self.time_difference(IgnOff.start, start_time)
            self.on_counter += 1
            
        return 1

