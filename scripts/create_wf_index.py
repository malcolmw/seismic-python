import obspy
import os
import pandas as pd

GOOGLE_DRIVE = os.environ['GOOGLE_DRIVE']
WF_DIR       = os.path.join(
    GOOGLE_DRIVE,
    'malcolm.white@usc.edu',
    'data',
    'wfs'
)

columns = ('network', 'station', 'location', 'channel', 'starttime', 'endtime', 'sampling_rate', 'npts', 'path')

df = pd.DataFrame(columns=columns)
for dirpath, dirnames, filenames in os.walk(WF_DIR):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        try:
            st = obspy.read(path, headonly=True)
        except TypeError:
            continue
        for tr in st:
            print(tr)
            df = df.append(
                pd.DataFrame(
                    [
                        [
                            tr.stats.network,
                            tr.stats.station,
                            tr.stats.location,
                            tr.stats.channel,
                            tr.stats.starttime.timestamp,
                            tr.stats.endtime.timestamp,
                            tr.stats.sampling_rate,
                            tr.stats.npts,
                            path
                        ]
                    ],
                    columns=columns
                ),
                ignore_index=True
            )

with pd.HDFStore(os.path.join(WF_DIR, 'wf_index.h5')) as store:
    store['wf_index'] = df
