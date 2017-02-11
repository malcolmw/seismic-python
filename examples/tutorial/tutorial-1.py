"""
This is a brief tutorial on how to load waveform data and make detections.
"""

import matplotlib.pyplot as plt
import seispy as sp
import obspy
# First we will load data explicitly from waveform file.

trZ = sp.trace.Trace("/home/seismech-00/sjfzdb/continuous_wfs_tmp/borehole"
                     "/ucsb/2016/276/BVDA1.HHZ_00.2016.276.00.00.00")
trN = sp.trace.Trace("/home/seismech-00/sjfzdb/continuous_wfs_tmp/borehole"
                     "/ucsb/2016/276/BVDA1.HHN_00.2016.276.00.00.00")
trE = sp.trace.Trace("/home/seismech-00/sjfzdb/continuous_wfs_tmp/borehole"
                     "/ucsb/2016/276/BVDA1.HHE_00.2016.276.00.00.00")

# Now from these 3 traces, create a 3C gather.
# Make sure vertical component is at the beginning.
gather = sp.gather.Gather3C([trZ, trN, trE])

# We still have all of our usual obspy.stream.Stream behavior.
# gather.plot()

# Now let's make some detections.
# First do some pre-processing.
gather.filter("bandpass", freqmin=1, freqmax=20)
# Calculate the STA/LTA characteristic function from the vertical component.
cft = gather.V.copy()
cft.trigger("recstalta",
            sta=1,
            lta=10)
# For each "P-wave" detection, try to make an S-wave detection
for sample_on, sample_off in obspy.signal.trigger.trigger_onset(cft.data, 6, 2):
    # Calculate trigger on-time
    ton = gather.stats.starttime + sample_on * gather.stats.delta
    # Make a copy of the gather and trim it.
    gather_cp = gather.copy()
    gather_cp.trim(starttime=ton-4.0, endtime=ton+16.0)
    # Now try to detect the S-wave
    detection = gather_cp.detect_swave(ton)
    # If there is an S-wave detection, plot the traces with picks.
    if detection is not None:
        time_P = ton.toordinal() +\
                              ton._get_hours_after_midnight() / 24.
        time_S = detection.time.toordinal() +\
                              detection.time._get_hours_after_midnight() / 24.
        fig = gather_cp.plot(handle=True, equal_scale=False)
        ax = fig.axes[0]
        ax.axvline(time_P, color="r", linewidth=2)
        ax.axvline(time_S, color="b", linewidth=2)
        plt.show()

