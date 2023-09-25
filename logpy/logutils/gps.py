from .logabc import BasicLog
from easydict import EasyDict

GPS_Patterns = EasyDict()
GPS_Patterns.FixUnfix = r"EVT GPS (?P<FixUnfix>(?:UN)?FIX)"

class GPS(BasicLog):  # may rename it later when new functionlity is added
    def __init__(self, name, pattern=GPS_Patterns.FixUnfix, **kwargs):
        super(GPS, self).__init__(name, pattern, **kwargs)
        self.result_dict.Status = EasyDict()
    
    def update_counts(self, match):
        matchdict = EasyDict(match.groupdict())
        ## corresponding time at which the Status changed
        self.result_dict.Status[f"{self.result_dict.Count} {matchdict.FixUnfix}"] = match.string[1:20]
        return 1 # write to out log file