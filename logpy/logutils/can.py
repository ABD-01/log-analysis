from .logabc import BasicLog
from easydict import EasyDict

CanPatterns = EasyDict()
CanPatterns.Event = r"CAN (?P<event>bus-off detected|bus-off cleared|Reinit Done)(?: for CANFD|\.)"

class CanEvent(BasicLog):
    def __init__(self, name, pattern=CanPatterns.Event, **kwargs):
        super(CanEvent, self).__init__(name, pattern, **kwargs)
        self.result_dict.Event = EasyDict()
    
    def update_counts(self, match):
        event = match.group('event')
        self.result_dict.Event[event] = self.result_dict.Event.get(event, 0) + 1
        return 1 # write to out log file