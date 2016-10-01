from copy import deepcopy

import numpy as np

import algorithm as alg

class Picker (object):
    """
    Phase picker base class
    """
    def __init__(self, meta=None):
        self.p = None
        self.meta = meta
        self.cft = None

    def pick(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def sec_to_samp(self, time, fs):
        return int(time*fs)

    def win_idx(self, t, npts, dura, fs):
        """
        Calculates start and stop indices of a window around t
        't' is the time in seconds from start of 'trace' to window around
        'npts' is the length of the trace in samples
        'dura' is in seconds from t (midpoint) to start/end of window
        """
        time = self.sec_to_samp(t, fs)

        start = time - self.sec_to_samp(dura, fs)
        stop = time + self.sec_to_samp(dura, fs)
        if start < 0:
            start = 0
        if start >= npts:
            raise ValueError("Start value in win_idx larger than npts")
        if stop >= npts:
            stop = npts - 1
        return (start, stop)

class PPicker (Picker):
    """
    P-wave arrival picker (Ross & Ben-Zion 2014, GJI)
    """
    def __init__(self, meta=None):
        super(self.__class__, self).__init__(meta=meta)

    def first_motion(self, v_trace):
        """
        Determines the first motion polarity from vertical trace
        v_trace is an ObsPy vertical trace
        """
        if self.p is None:
            raise ValueError("P pick must first be made")
        idx = self.sec_to_samp(self.p, v_trace.stats.sampling_rate)
        if v_trace.data[idx] >= 0:
            return 'U'
        else:
            return 'D'

    def pick(self, tr, dt, dur_min=1.5, peak_min=0, sta=1, lta=10, on=5,
             off=1.0, get_cft=False):
        """
        'tr' is a numpy array containing the seismogram of interest
        'dur_min' is the minimum duration for trigger window
        'peak_min' is the minimum SNR value allowed for the peak STA/LTA
        'sta': short term average window length in seconds
        'lta': long term average window length in seconds
        'on': STA/LTA value for trigger window to turn on
        'off': STA/LTA value for trigger window to turn off
        """
        # Calculate characteristic function
        picks = []
        fs = 1.0/dt
        cft = deepcopy(tr)
        if tr.size/fs <= lta:
            return None, None

        cft = alg.stalta(tr, int(sta*fs), int(lta*fs))
        if get_cft:
            self.cft = cft
        triggers = triggerOnset(cft, on, off)
        triggers = stitch_trigs(triggers, 2.0, 1/fs)
        for on_t, off_t in triggers:
            if off_t <= on_t:
                continue
            if (off_t - on_t)/fs < dur_min:
                continue
            MAX = np.max(cft[on_t:off_t])
            idx = np.argmax(cft[on_t:off_t])
            if MAX >= peak_min:
                picks.append((on_t, MAX))

        # Take the largest peak value
        if not picks:
            return None, None
        else:
            p_pick = max(picks, key=lambda x: x[1])[0]
            SNR = max(picks, key=lambda x: x[1])[1]
        self.p = p_pick/fs
        return self.p, SNR


    def resid(self, trace, origin_time):
        dt = super(PPicker, self).resid(trace, origin_time, 'Pg')
        return dt

#-------------------------------------------------------------
class SPicker (Picker):
    """
    S-wave arrival picker (Ross & Ben-Zion 2014, GJI)
    """
    def __init__(self, meta=None):
        self.filter = None
        super(SPicker, self).__init__(meta=meta)

    def polarize_traces(self, N, E, Z, dt, wlen):
        """
        Calculate P & S polarization filters from rectilinearity and
        apparent incidence angle.
        Inputs:
        [N, E, Z]:= Numpy arrays for each trace
        wlen: A sliding window length in seconds for rolling cov mat
        Outputs:
        p_filt: p polarization filter
        s_filt: s polarization filter
        """
        CZ = np.ascontiguousarray(Z, dtype=np.float32)
        CE = np.ascontiguousarray(E, dtype=np.float32)
        CN = np.ascontiguousarray(N, dtype=np.float32)
        r, phi = alg.cov_filter(CZ, CN, CE, int(wlen/dt))

        s = r*(1-phi)
        N = N * s
        E = E * s
        return N, E

    def pick(self, tr, dt, p_pick=-1, dur_min=1.0, peak_min=0, sta=1, lta=10,
             on=5, off=1, get_cft=False, k_len=5, k_buf=0.3):
        """
        'tr' is an ObsPy Trace object containing the trace of interest
            This generally should be a horizontal or Q/T trace.
        'p_pick': Use provided p_pick to calculate optional S pick quality
        'dur_min' is the minimum duration for trigger window
        'peak_min' is the minimum SNR value allowed for the peak STA/LTA
        'sta': short term average window length in seconds
        'lta': long term average window length in seconds
        'on': STA/LTA value for trigger window to turn on
        'off': STA/LTA value for trigger window to turn off
        'k_len': Kurtosis sliding-window length
        'k_buf': Kurtosis sliding-window buffer
        """
        # Calculate STA/LTA, run trigger mech to find window w/ largest peak
        picks = []
        fs = 1.0/dt
        k_nsamp = int(k_len*fs)
        if tr.size/fs <= lta:
            return None, None
        nsta = int(sta*fs)
        nlta = int(lta*fs)
        cft = alg.snr(tr, nsta, nlta, 3.0, 2.0)
        #cft = alg.stalta(tr, nsta, nlta)
        if get_cft:
            self.cftS = cft
        #   self.cftS = moving_average(cft, int(nsta/2))

        triggers = triggerOnset(cft, on, off)
        #triggers = stitch_trigs(triggers, 3.0, 1/fs)
        max_on = 0
        max_off = 0
        best = 0
        for on_t, off_t in triggers:
            if off_t <= on_t:
                continue
            if (off_t - on_t)/fs < dur_min:
                continue
            MAX = np.max(cft[on_t:off_t])
            idx = np.argmax(cft[on_t:off_t])
            if MAX >= peak_min:
                if MAX > best:
                    best = MAX
                    max_on = on_t
                    max_off = off_t
                picks.append((on_t+idx, MAX, on_t, off_t))

        # Write cft to picker
        if get_cft:
            tmp_cft = alg.pai_k(tr, int(k_len*fs))
            tmp_cft[:int((k_len+k_buf)*fs)] = 0
            self.cftK = tmp_cft

        # Take the largest peak value
        if not picks:
            if p_pick != -1:
                return None, None
            else:
                return None, None
        else:
            s_pick = max(picks, key=lambda x: x[1])[0]
            SNR = max(picks, key=lambda x: x[1])[1]

        # Check for whether multiple large peaks exist in trigger window
        """
        tmp_cft = moving_average(cft[max_on-nsta:max_off+nsta], int(nsta/2))
        maxima = argrelmax(tmp_cft, order=1)[0] + max_on - nsta
        tall_max = []
        for idx in maxima:
            if cft[idx] >= 0.6*SNR:
                tall_max.append(idx)
        if tall_max:
            s_pick = tall_max[-1]
        """
        # If P pick does exist, use S-P time to determine allowance
        if p_pick == -1:
            t_sp = 0.5
        else:
            t_sp = (s_pick)/fs - p_pick
        if t_sp <= 0:
            return None, SNR
        if t_sp > 4.0:
            t_sp = 4.0

        start0, stop0 = self.win_idx(s_pick/fs, tr.size, 0.5*t_sp, fs)
        cft = alg.pai_k(tr, k_nsamp)
        cft = np.diff(cft)
        if (stop0 - start0) < 2:
            return None, SNR
        s_pick = np.argmax(cft[start0:stop0]) + start0

        return s_pick/fs, SNR
