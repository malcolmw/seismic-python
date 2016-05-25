from obspy.core import UTCDateTime

def verify_time(time):
    if not isinstance(time, UTCDateTime) and\
            not isinstance(time, float) and\
            not isinstance(time, int) and\
            not isinstance(time, str):
        raise TypeError("invalid type for time argument")
    if not isinstance(time, UTCDateTime):
        if isinstance(time, str):
            time = float(time)
        if isinstance(time, int) and time >= 1000000 and time <= 9999999:
            time = UTCDateTime(year=time / 1000, julday=time % 1000)
        elif isinstance(time, float) and time == -1.0:
            time = UTCDateTime(year=3000, julday=365, hour=23, minute=59, second=59)
        else:
            time = UTCDateTime(time)
    return time
