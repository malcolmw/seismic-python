# -*- coding: utf-8 -*-
from seispy.event import Arrival
from seispy.gather import Gather3C
from seispy.trace import Trace
import matplotlib.pyplot as plt
import seispy.signal.detect as alg
from obspy.core import Stream


def zach(T):
    if not (T[0].stats.npts == T[1].stats.npts == T[2].stats.npts):
        return None
    T.detrend(type='linear')
    T.filter(type='bandpass', freqmin=3, freqmax=10)
    dt = T[0].stats.delta
    out = alg.detectS(T[2].data, T[0].data, T[1].data, 3.0, dt, 1.0)
    s1_pick, s2_pick, snr_s1, snr_s2, pol_fltr, S1, S2, K1, K2 = out
    return s1_pick, s2_pick, snr_s1, snr_s2


def main():
    infile = open("/home/shake/malcolcw/data/wfs/detection/shear_input.txt")
    save_dir = "/home/shake/malcolcw/sandbox/shear_test/figures"
    i=1
    for line in infile:
        print i
        trN, trE, trZ = [Trace(f) for f in line.split()[2:]]
        st = Stream([trN.copy(), trE.copy(), trZ.copy()])
        s1_pickZR, s2_pickZR, snr_s1ZR, snr_s2ZR = zach(st)
        lag = None
        if s1_pickZR > 0 and s2_pickZR > 0:
            if snr_s1ZR > snr_s2ZR:
                time = trN.stats.starttime.timestamp + s1_pickZR
                chan = trN.stats.channel
            elif snr_s2ZR > snr_s1ZR:
                time = trE.stats.starttime.timestamp + s2_pickZR
                chan = trE.stats.channel
        elif s1_pickZR > 0:
            time = trN.stats.starttime.timestamp + s1_pickZR
            chan = trN.stats.channel
        elif s2_pickZR > 0:
            time = trE.stats.starttime.timestamp + s2_pickZR
            chan = trE.stats.channel
        if lag is not None:
            arrival = Arrival(trN.stats.station,
                              chan,
                              time,
                              "S")
        else:
            arrival = None
        gather = Gather3C([trZ, trN, trE])
        gather.detrend(type="linear")
        gather.filter(type="bandpass", freqmin=3, freqmax=10)
        detection = gather.detectS()
        if detection is not None and arrival is not None:
            if abs(detection.time.timestamp - arrival.time.timestamp) > 0.01:
                fig = gather.plot(arrivals=[arrival],
                            detections=[detection],
                            #save="%s/example_%04d.png" % (save_dir, i),
                            show=True)
                plt.close()
    
        if i == 500:
            break
        i += 1

if __name__ == "__main__":
    main()