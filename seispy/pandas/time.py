import numpy as np
import pandas as pd

def ymd_to_dt(df, utc=True):
    return(pd.to_datetime(df["year"].astype(str) + "-"
                             + df["month"].astype(str) + "-"
                             + df["day"].astype(str),
                         utc=utc)\
         + pd.to_timedelta(df["hour"].astype(str) + "H")\
         + pd.to_timedelta(df["minute"].astype(str) + "M")\
         + pd.to_timedelta(df["second"].astype(str) + "S"))

def to_decimal_year(obj):
    """
    Convert input data to decimal year.

    This is a type-checking wrapper, which calls object-type-specific
    functions to do the actual conversion.
    """
    if isinstance(obj, pd.core.series.Series):
        return(_series_to_decimal_year(obj))
    else:
        # TODO: This should at least be extended to handle lists,
        # TODO: tuples, and np.arrays
        raise(NotImplementedError)

def _series_to_decimal_year(series):
    if series.dtype is np.dtype("float64"):
        return(_float64_array_to_decimal_year(series.values))
    elif series.dtype == pd.core.dtypes.dtypes.DatetimeTZDtype(unit="ns",
                                                               tz="UTC"):
        series = _datetime_to_epoch(series)
        return(_float64_array_to_decimal_year(series.values))
    else:
        raise(NotImplementedError)


def _float64_array_to_decimal_year(array):
    """
    Convert array of epoch timestamps (in nanoseconds) to pandas.Series
    of decimal year values.

    Arguments
    =========
    array ::iterable:: an array of epoch timestamps in nanoseconds

    Returns
    =======
    pandas.Series of decimal year values
    """
    time = pd.to_datetime(array, utc=True)
    frac = time - pd.to_datetime(time.year.astype(str) + "-01-01", utc=True)
    year_length = pd.to_datetime((time.year+1).astype(str) + "-01-01", utc=True)\
                - pd.to_datetime(time.year.astype(str) + "-01-01", utc=True)
    dec_yr = time.year + frac.total_seconds()/year_length.total_seconds()
    return(dec_yr)

def _datetime_to_epoch(series):
    epoch_start = pd.to_datetime("1970-01-01 00:00:00", utc=True)
    return(np.asarray((series - epoch_start)/pd.to_timedelta("1ns")))

def to_epoch(series, utc=True):
    r"""Return series as epoch timestamp in nanoseconds.
    
    :param list series: Input series
    :param bool utc: UTC time
    """
    if isinstance(series, str):
        series = [series]
    series = pd.to_datetime(np.asarray(series, dtype=str), utc=utc)
    return(_datetime_to_epoch(series))
