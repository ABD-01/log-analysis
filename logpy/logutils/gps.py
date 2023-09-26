from .logabc import BasicLog
from easydict import EasyDict

GPS_Patterns = EasyDict()
GPS_Patterns.FixUnfix = r"EVT GPS (?P<FixUnfix>(?:UN)?FIX)"

# may rename it later when new functionlity is added
def GPS(name, pattern=GPS_Patterns.FixUnfix, **kwargs):
    kwargs["writeToFile"] = 1
    return BasicLog(name, pattern, **kwargs)