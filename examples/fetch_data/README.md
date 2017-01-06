# Tutorial
##fetch\_data
####usage: fetch\_data database configuration\_file

fetch\_data is a easy-to-use command line program to retrieve event-segmented
waveform data from the Array Network Facility (UCSD, Frank Vernon) data
archives. Type fetch\_data -h to get help.

fetch\_data is configured using a configuration file. The user should only need
to edit the configuration file and command line arguments to retrieve the data
desired.

###Example configuration file
####fetch\_data.cfg
```python
[General]
rsync_server = rsync://eqinfo.ucsd.edu/ANZA_waveforms
n_threads = 1
start_lead = 0
end_lag = 120
output_format = MSEED
stations = PFO, RA[01][1-9], C.*
channels = HNZ, HNE, BH.*
```

####configuration parameters
rsync\_server: This shouldn't need to change.
n\_threads: Number of data fetching threads. Testing shows that the rsync
server at UCSD cannot handle requests from more than 8 threads. Try running
with a few threads but be careful using too many, you might not get all the
data you want.
start\_lead: Number of seconds before origin time to fetch.
end\_lag: Number of seconds after origin time to fetch.
output\_format: Output data format (eg. MSEED, SAC or any format understood, by
[obspy.core.Stream.write()](http://docs.obspy.org/packages/autogen/obspy.core.stream.Stream.write.html#obspy.core.stream.Stream.write).
stations: Comma separated list of stations to retrieve data for.
Whitespace and wildcards are ok.
channels: Comma separated list of channels to retrieve data for.
Whitespace and wildcards are ok.

###Example command
This example command, using the configuration file above will retrieve 2
minutes of data following each event. Data from station PFO, the entire RA
array and any station with station code starting with C will be retrieved.
Only data from channels HNZ, HNE and all BH channels will be retrieved. A
directory tree of $YEAR/$EVID will be created in the working directory
and output data saved in these subdirectories with filenames like
$STA.$CHAN.$EVID.

```bash
-bash-4.3$ fetch\_data ~/projects/SJFZ/dbs/1.0/2015/SJFZ\_2015 fetch\_data.cfg 
starting processing thread #1
Copying data for 2015/001
receiving file list ... 
41 files to consider
2015/
2015/001/
2015/001/CPE.BHE.2015.001.00.00.00
      3,575,808 100%   30.72MB/s    0:00:00 (xfr#1, to-chk=38/41)
2015/001/CPE.BHN.2015.001.00.00.00
      3,555,328 100%   23.38MB/s    0:00:00 (xfr#2, to-chk=37/41)
2015/001/CPE.BHZ.2015.001.00.00.00
      3,768,320 100%   20.30MB/s    0:00:00 (xfr#3, to-chk=36/41)
2015/001/CPE.HNE.2015.001.00.00.00
      5,509,120 100%   23.45MB/s    0:00:00 (xfr#4, to-chk=35/41)
2015/001/CPE.HNZ.2015.001.00.00.00
      9,433,088 100%   29.59MB/s    0:00:00 (xfr#5, to-chk=34/41)
2015/001/CRY.BHE.2015.001.00.00.00
      2,785,280 100%    8.10MB/s    0:00:00 (xfr#6, to-chk=33/41)
2015/001/CRY.BHN.2015.001.00.00.00
      2,670,592 100%    7.26MB/s    0:00:00 (xfr#7, to-chk=32/41)
2015/001/CRY.BHZ.2015.001.00.00.00
      2,850,816 100%    7.25MB/s    0:00:00 (xfr#8, to-chk=31/41)
2015/001/CRY.HNE.2015.001.00.00.00
      5,832,704 100%   13.09MB/s    0:00:00 (xfr#9, to-chk=30/41)
2015/001/CRY.HNZ.2015.001.00.00.00
      6,012,928 100%   12.05MB/s    0:00:00 (xfr#10, to-chk=29/41)
2015/001/PFO.BHE.2015.001.00.00.00
      2,736,128 100%    5.23MB/s    0:00:00 (xfr#11, to-chk=28/41)
2015/001/PFO.BHN.2015.001.00.00.00
      2,768,896 100%    5.05MB/s    0:00:00 (xfr#12, to-chk=27/41)
2015/001/PFO.BHZ.2015.001.00.00.00
      2,740,224 100%    4.79MB/s    0:00:00 (xfr#13, to-chk=26/41)
2015/001/PFO.HNE.2015.001.00.00.00
      5,898,240 100%    9.44MB/s    0:00:00 (xfr#14, to-chk=25/41)
2015/001/PFO.HNZ.2015.001.00.00.00
      5,603,328 100%    8.30MB/s    0:00:00 (xfr#15, to-chk=24/41)
2015/001/RA01.HNE.2015.001.00.00.00
     13,021,184 100%   16.45MB/s    0:00:00 (xfr#16, to-chk=23/41)
2015/001/RA01.HNZ.2015.001.00.00.00
     13,025,280 100%   14.36MB/s    0:00:00 (xfr#17, to-chk=22/41)
2015/001/RA02.HNE.2015.001.00.00.00
     13,205,504 100%   12.88MB/s    0:00:00 (xfr#18, to-chk=21/41)
2015/001/RA02.HNZ.2015.001.00.00.00
     13,488,128 100%   11.78MB/s    0:00:01 (xfr#19, to-chk=20/41)
2015/001/RA03.HNE.2015.001.00.00.00
     13,139,968 100%   61.13MB/s    0:00:00 (xfr#20, to-chk=19/41)
2015/001/RA03.HNZ.2015.001.00.00.00
     13,205,504 100%   39.73MB/s    0:00:00 (xfr#21, to-chk=18/41)
2015/001/RA04.HNE.2015.001.00.00.00
     13,357,056 100%   29.56MB/s    0:00:00 (xfr#22, to-chk=17/41)
2015/001/RA04.HNZ.2015.001.00.00.00
     13,635,584 100%   23.77MB/s    0:00:00 (xfr#23, to-chk=16/41)
2015/001/RA05.HNE.2015.001.00.00.00
     13,418,496 100%   19.36MB/s    0:00:00 (xfr#24, to-chk=15/41)
2015/001/RA05.HNZ.2015.001.00.00.00
     13,692,928 100%   16.78MB/s    0:00:00 (xfr#25, to-chk=14/41)
2015/001/RA06.HNE.2015.001.00.00.00
     12,763,136 100%   13.74MB/s    0:00:00 (xfr#26, to-chk=13/41)
2015/001/RA06.HNZ.2015.001.00.00.00
     13,496,320 100%   12.87MB/s    0:00:01 (xfr#27, to-chk=12/41)
2015/001/RA07.HNE.2015.001.00.00.00
     12,492,800 100%  110.32MB/s    0:00:00 (xfr#28, to-chk=11/41)
2015/001/RA07.HNZ.2015.001.00.00.00
     12,791,808 100%   56.22MB/s    0:00:00 (xfr#29, to-chk=10/41)
2015/001/RA08.HNE.2015.001.00.00.00
     12,824,576 100%   37.52MB/s    0:00:00 (xfr#30, to-chk=9/41)
2015/001/RA08.HNZ.2015.001.00.00.00
     13,213,696 100%   28.71MB/s    0:00:00 (xfr#31, to-chk=8/41)
2015/001/RA09.HNE.2015.001.00.00.00
     13,225,984 100%   22.89MB/s    0:00:00 (xfr#32, to-chk=7/41)
2015/001/RA09.HNZ.2015.001.00.00.00
     13,914,112 100%   19.81MB/s    0:00:00 (xfr#33, to-chk=6/41)
2015/001/RA11.HNE.2015.001.00.00.00
     17,047,552 100%   19.95MB/s    0:00:00 (xfr#34, to-chk=5/41)
2015/001/RA11.HNZ.2015.001.00.00.00
     13,381,632 100%   13.75MB/s    0:00:00 (xfr#35, to-chk=4/41)
2015/001/RA12.HNE.2015.001.00.00.00
     13,332,480 100%   12.20MB/s    0:00:01 (xfr#36, to-chk=3/41)
2015/001/RA12.HNZ.2015.001.00.00.00
     13,676,544 100%   82.03MB/s    0:00:00 (xfr#37, to-chk=2/41)
2015/001/i4.CRN.HNE.2015001\_0+
      9,527,296 100%   37.86MB/s    0:00:00 (xfr#38, to-chk=1/41)
2015/001/i4.CRN.HNZ.2015001\_0+
     11,767,808 100%   33.01MB/s    0:00:00 (xfr#39, to-chk=0/41)
Data retrieved for 2015/001
origin: 120070 33.3637 243.1422 11.8659 2015-01-01T00:36:27.680380Z dbgrassoc:local
Writing file CPE.BHE.120070
Writing file CPE.BHN.120070
Writing file CPE.BHZ.120070
Writing file CPE.HNE.120070
Writing file CPE.HNZ.120070
Writing file CRY.BHE.120070
Writing file CRY.BHN.120070
Writing file CRY.BHZ.120070
Writing file CRY.HNE.120070
Writing file CRY.HNZ.120070
Writing file PFO.BHE.120070
Writing file PFO.BHN.120070
Writing file PFO.BHZ.120070
Writing file PFO.HNE.120070
Writing file PFO.HNZ.120070
Writing file RA01.HNE.120070
Writing file RA01.HNZ.120070
Writing file RA02.HNE.120070
Writing file RA02.HNZ.120070
Writing file RA03.HNE.120070
Writing file RA03.HNZ.120070
Writing file RA04.HNE.120070
Writing file RA04.HNZ.120070
Writing file RA05.HNE.120070
Writing file RA05.HNZ.120070
Writing file RA06.HNE.120070
Writing file RA06.HNZ.120070
Writing file RA07.HNE.120070
Writing file RA07.HNZ.120070
Writing file RA08.HNE.120070
Writing file RA08.HNZ.120070
Writing file RA09.HNE.120070
Writing file RA09.HNZ.120070
Writing file RA11.HNE.120070
Writing file RA11.HNZ.120070
Writing file RA12.HNE.120070
Writing file RA12.HNZ.120070
Writing file CRN.HNE.120070
Writing file CRN.HNZ.120070
origin: 120071 33.3652 243.6583 11.3647 2015-01-01T01:33:56.686120Z dbgrassoc:local
Writing file CPE.BHE.120071
Writing file CPE.BHN.120071
Writing file CPE.BHZ.120071
Writing file CPE.HNE.120071
Writing file CPE.HNZ.120071
Writing file CRY.BHE.120071
Writing file CRY.BHN.120071
Writing file CRY.BHZ.120071
Writing file CRY.HNE.120071
Writing file CRY.HNZ.120071
Writing file PFO.BHE.120071
Writing file PFO.BHN.120071
Writing file PFO.BHZ.120071
Writing file PFO.HNE.120071
Writing file PFO.HNZ.120071
Writing file RA01.HNE.120071
Writing file RA01.HNZ.120071
Writing file RA02.HNE.120071
Writing file RA02.HNZ.120071
Writing file RA03.HNE.120071
Writing file RA03.HNZ.120071
Writing file RA04.HNE.120071
Writing file RA04.HNZ.120071
Writing file RA05.HNE.120071
Writing file RA05.HNZ.120071
Writing file RA06.HNE.120071
Writing file RA06.HNZ.120071
Writing file RA07.HNE.120071
Writing file RA07.HNZ.120071
Writing file RA08.HNE.120071
Writing file RA08.HNZ.120071
Writing file RA09.HNE.120071
Writing file RA09.HNZ.120071
Writing file RA11.HNE.120071
Writing file RA11.HNZ.120071
Writing file RA12.HNE.120071
Writing file RA12.HNZ.120071
Writing file CRN.HNE.120071
Writing file CRN.HNZ.120071
```
