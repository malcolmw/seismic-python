# css3.0
## Relations/tables
### achanaux
sta, fchan, aux, chan, lddate
### adoption
snet, sta, time, newsnet, newsta, atype, auth, lddate
### affiliation
net, sta, lddate
### anetsta
anet, fsta, sta, lddate
### arrival
sta, time, arid, jdate, stassid, chanid, chan, iphase, stype, deltim, azimuth, delaz, slow, delslo, ema, rect, amp, per, logat, clip, fm, snr, qual, auth, commid, lddate
### assoc
arid, orid, sta, phase, belief, delta, seaz, esaz, timeres, timedef, azres, azdef, slores, slodef, emares, wgt, vmodel, commid, lddate
### balerlist
dlname, time, endtime, target, connection, q330sn, inp, balersn, balerfirm, baleron, onsecs, htmlinfo, htmlsecs, msdinfo, msdsecs, data_start, data_end, lddate
### balerproc
net, sta, baler14_start, baler14_end, baler44_start, baler44_end, proc_start, proc_end, dmc_start, dmc_end, rt_start, rt_end, completed, lddate
### beam
wfid, azimuth, slo, filter, recipe, algorithm, auth, lddate
### calib_request
sta, chan, time, acktime, hostname, user, auth, pid, dir, dfile, lddate
### calibration
sta, chan, time, endtime, insname, snname, dlname, samprate, segtype, dlsta, dlchan, lead, stream, calib, calper, fc, units, lddate
### centryd
orid, jdate, timecentryd, lat, lon, depth, coterr, claerr, cloerr, cdperr, durat, nslpb, nrlpb, tmnlpb, nsmw, nrmw, tmnmw, dused, auth, commid, lddate
### cluster
gridname, gridid, evid, lddate
### comm
sta, time, endtime, commtype, provider, power, dutycycle, equiptype, lddate
### deployment
vnet, snet, sta, time, endtime, equip_install, equip_remove, cert_time, decert_time, pdcc, sdcc, lddate
### dlcmd_cal
dlname, time, target, model, disposition, execution, error, ssident, inp, dlcalseq, dlcalseqt, hostname, address, pid, user, lddate
### dlevent
dlname, time, dlevtype, dlcomment, lddate
### dmcbull
data_start, data_end, time, nev, nor, nph, dir, dfile, auth, lddate
### dmcfiles
time, comment, dir, dfile, orb, auth, lddate
### emodel
orid, emodelx, emodely, emodelz, emodelt, lddate
### event
evid, evname, prefor, auth, commid, lddate
### fkgrid
sta, refsta, chan, time, endtime, twin, filter, dtime, nt, azimuth, slo, slowd, ppower, semin, semax, ne, snmin, snmax, nn, datatype, dir, dfile, foff, lddate
### fplane
orid, mechid, str1, dip1, rake1, str2, dip2, rake2, taxazm, taxplg, paxazm, paxplg, algorithm, auth, lddate
### gclfield

### gclgdisk

### gregion
grn, grname, lddate
### gridscor

### gridstat
gridname, gridid, pmelrun, sswrodgf, ndgf, sdobs, lddate
### gsnspec
sta, chan, insname, period, fc, pc_1, pc_5, pc_25, pc_50, time, endtime, lddate
### hypocentroid
gridname, gridid, dlat, dlon, depth, hclat, hclon, hcdepth, nass, delta, ztop, zbot, lddate
### instrument
inid, insname, instype, band, digital, samprate, ncalib, ncalper, dir, dfile, rsptype, lddate
### lastid
keyname, keyvalue, lddate
### moment
orid, mexpon, mrr, mtt, mff, mrt, mrf, mtf, mrrerr, mtterr, mfferr, mrterr, mrferr, mtferr, taxval, taxplg, taxazm, paxval, paxplg, paxazm, naxval, naxplg, naxazm, bestdc, str1, dip1, rake1, str2, dip2, rake2, dused, auth, commid, lddate
### mt
mtid, pubid, qmlid, orid, tmpp, tmrp, tmrr, tmrt, tmtp, tmtt, taxlength, taxplg, taxazm, paxlength, paxplg, paxazm, naxlength, naxplg, naxazm, scm, pdc, str1, dip1, rake1, str2, dip2, rake2, drdepth, drtime, drlat, drlon, drmag, drmagt, estatus, rstatus, utime, auth, lddate
### netmag
magid, net, orid, evid, magtype, nsta, magnitude, uncertainty, auth, commid, lddate
### netmw
orid, evid, netmw, ml, sigmamw, netm0, netf0, neteqR, usta, rjsta, quality, auth, commid, lddate
### network
net, netname, nettype, auth, commid, lddate
### origerr
orid, sxx, syy, szz, stt, sxy, sxz, syz, stx, sty, stz, sdobs, smajax, sminax, strike, sdepth, stime, conf, commid, lddate
### origin
lat, lon, depth, time, orid, evid, jdate, nass, ndef, ndp, grn, srn, etype, review, depdp, dtype, mb, mbid, ms, msid, ml, mlid, algorithm, auth, commid, lddate
### pmelruns

### predarr
arid, orid, time, slow, seaz, ema, esaz, dip, lddate
### predmech
arid, orid, mechid, fm, radamp, lddate
### q330_calibration_weblog
email, stastr, time, pid, hostname, comment, lddate
### q330comm
dlsta, time, endtime, inp, ssident, idtag, lat, lon, elev, thr, lddate
### qctests
sta, chan, time, testtype, qcresult, data_start, data_end, samprate, revsamp, revp, dir, dfile, hostname, auth, lddate
### qgrid
qgridname, recipe, qgridtype, time, endtime, minlat, maxlat, minlon, maxlon, qdlat, qdlon, nlat, nlon, qgridfmt, units, maxval, dir, dfile, foff, orid, auth, lddate
### remark
commid, lineno, remark, lddate
### replayed
sta, chan, time, endtime, orb, lddate
### rrdcache
net, sta, chan, rrdvar, time, endtime, dir, dfile, lddate
### rrdgraph
net, sta, rrdvar, rrdgraphname, time, endtime, dir, dfile, lddate
### rsyncbaler
dlsta, net, sta, dfile, time, endtime, dir, status, attempts, msdtime, bandwidth, filebytes, media, fixed, md5, lddate
### schanloc
sta, fchan, loc, chan, lddate
### sensor
sta, chan, time, endtime, inid, chanid, jdate, calratio, calper, tshift, instant, lddate
### site
sta, ondate, offdate, lat, lon, elev, staname, statype, refsta, dnorth, deast, lddate
### sitechan
sta, chan, ondate, chanid, offdate, ctype, edepth, hang, vang, descrip, lddate
### sitephotos
sta, time, siteimagetype, imagename, imagesize, imagedescrip, format, dir, dfile, auth, lddate
### snetsta
snet, fsta, sta, lddate
### specdisc
tagname, sta, chan, time, endtime, phase, arid, rsptype, freqmin, freqmax, nfreq, df, rayleigh, tbp, scalib, twin, nwin, offset, totdur, demean, rsprm, taper, method, spectype, units, specfmt, foff, dir, dfile, auth, lddate
### sregion
srn, srname, lddate
### stabaler
dlsta, time, endtime, net, sta, inp, model, ssident, firm, nreg24, last_reg, nreboot, last_reboot, lddate
### stage
sta, chan, time, endtime, stageid, ssident, gnom, iunits, ounits, gcalib, gtype, izero, decifac, samprate, leadfac, dir, dfile, lddate
### stamag
magid, sta, arid, orid, evid, phase, magtype, magnitude, uncertainty, auth, commid, lddate
### stamw
sta, chamw, orid, evid, mw, m0, f0, eqR, distmw, rotaz, quality, timePmw, Pmw, timeSmw, Smw, segtype, auth, commid, lddate
### stassoc
stassid, sta, etype, review, location, dist, azimuth, lat, lon, depth, time, imb, ims, iml, auth, commid, lddate
### stgrid
sta, refsta, chan, time, endtime, twin, filter, azimuth, smin, smax, ns, dtime, nt, datatype, dir, dfile, foff, lddate
### wfdisc
sta, chan, time, wfid, chanid, jdate, endtime, nsamp, samprate, calib, calper, instype, segtype, datatype, clip, dir, dfile, foff, commid, lddate
### wfedit
sta, chan, edid, time, endtime, probtype, edittype, auth, commid, lddate
### wfmeas
sta, chan, meastype, filter, time, endtime, tmeas, twin, val1, val2, units1, units2, arid, auth, lddate
### wfoffset
sta, chan, time, endtime, valoffset, lddate
### wfparam
sta, chan, orid, filter, time, endtime, ml, dista, seaz, PGA, PGV, PSA03, PSA10, PSA30, Arias, Housner, arid, auth, lddate
### wfrms
sta, chan, time, twin, filter, fc, arid, stype, segtype, rms, lddate
### wfsrb
sta, chan, time, wfid, chanid, jdate, endtime, nsamp, samprate, calib, calper, instype, segtype, datatype, clip, Szone, Scoll, Sobj, foff, commid, lddate
### wftag
tagname, tagid, wfid, lddate
### wftape
sta, chan, time, wfid, chanid, jdate, endtime, nsamp, samprate, calib, calper, instype, segtype, datatype, clip, dir, dfile, volname, tapefile, tapeblock, commid, lddate
### wftar
sta, chan, time, wfid, chanid, jdate, endtime, nsamp, samprate, calib, calper, instype, segtype, datatype, clip, dir, dfile, foff, tapename, fileno, tfile, tfoff, commid, lddate
## Attributes/fields
field|dtype|format|null|width
---|---|---|---|---
algorithm|str|%-15s|-|15
amp|float|%10.1f|-1.0|10
anet|str|%-9s|-|9
arid|int|%8ld|-1|8
auth|str|%-15s|-|15
aux|str|%-8s|-|8
azdef|str|%-1s|-|1
azimuth|float|%7.2f|-1.0|7
azres|float|%7.1f|-999.0|7
band|str|%-1s|-|1
belief|float|%4.2f|9.99|4
bestdc|float|%5.2f|-9.99|5
calib|float|%16.9g|0.0|16
calper|float|%16.6f|-1.0|16
calratio|float|%16.6f|1.0|16
cdperr|float|%5.1f|-99.9|5
chan|str|%-8s|-|8
chanid|int|%8ld|-1|8
claerr|float|%5.1f|-99.9|5
clip|str|%-1s|-|1
cloerr|float|%5.1f|-99.9|5
commid|int|%8ld|-1|8
conf|float|%5.3f|0.0|5
coterr|float|%5.1f|-99.9|5
ctype|str|%-4s|-|4
datatype|str|%-2s|-|2
deast|float|%9.4f|0.0|9
decifac|int|%8ld|-1|8
delaz|float|%7.2f|-1.0|7
delslo|float|%7.2f|-1.0|7
delta|float|%8.3f|-1.0|8
deltim|float|%6.3f|-1.0|6
demean|str|%-1s|-|1
depdp|float|%9.4f|-999.0|9
depth|float|%9.4f|-999.0|9
descrip|str|%-50s|-|50
df|float|%15.6lg|-1.0|15
dfile|str|%-32s|-|32
digital|str|%-1s|-|1
dip|float|%5.1f|-99.9|5
dip1|float|%5.1f|999.9|5
dip2|float|%5.1f|999.9|5
dir|str|%-64s|-|64
dist|float|%7.2f|-1.0|7
dlchan|str|%s|-|16
dlname|str|%s|-|32
dlsta|str|%s|-|16
dnorth|float|%9.4f|0.0|9
drdepth|float|%9.4f|-999.0|9
drlat|float|%9.4f|-999.0|9
drlon|float|%9.4f|-999.0|9
drmag|float|%7.2f|-99.99|7
drmagt|str|%-6s|-|6
drtime|float|%17.5f|9999999999.999|17
dtime|float|%9.2f|0.0|9
dtype|str|%-1s|-|1
durat|float|%5.1f|-99.9|5
dused|str|%-10s|-|10
edepth|float|%9.4f|-9.9999|9
edid|int|%8ld|-1|8
edittype|str|%-8s|-|8
elev|float|%9.4f|-999.0|9
ema|float|%7.2f|-1.0|7
emares|float|%7.1f|-999.0|7
emodelt|float|%15.6lg|-1.0|15
emodelx|float|%15.6lg|-1.0|15
emodely|float|%15.6lg|-1.0|15
emodelz|float|%15.6lg|-1.0|15
endtime|float|%17.5f|9999999999.999|17
esaz|float|%7.2f|-999.0|7
estatus|str|%-12s|-|12
etype|str|%-2s|-|2
evid|int|%8ld|-1|8
evname|str|%-15s|-|15
fc|float|%11.6f|-1.0|11
fchan|str|%-8s|-|8
fileno|int|%6ld|-1|6
filter|str|%-30s|-|30
fm|str|%-2s|-|2
foff|int|%10ld|0|10
freqmax|float|%15.6lg|-1.0|15
freqmin|float|%15.6lg|-1.0|15
fsta|str|%-6s|-|6
gcalib|float|%10.6f|0.0|10
gnom|float|%10.5g|0.0|10
grn|int|%8ld|-1|8
grname|str|%-40s|-|40
gtype|str|%-20s|-|20
hang|float|%6.1f|-999.9|6
imb|float|%7.2f|-999.0|7
iml|float|%7.2f|-999.0|7
ims|float|%7.2f|-999.0|7
inid|int|%8ld|-1|8
insname|str|%-50s|-|50
instant|str|%-1s|-|1
instype|str|%-6s|-|6
iphase|str|%-8s|-|8
iunits|str|%-16s|-|16
izero|int|%8ld|0|8
jdate|int|%8ld|-1|8
keyname|str|%-15s|-|15
keyvalue|int|%8ld|-1|8
lat|float|%9.4f|-999.0|9
lddate|float|%17.5f|-9999999999.999|17
lead|str|%s|-|4
leadfac|float|%11.7f|0.0|11
lineno|int|%8ld|-1|8
loc|str|%-8s|-|8
location|str|%-32s|-|32
logat|float|%7.2f|-999.0|7
lon|float|%9.4f|-999.0|9
magid|int|%8ld|-1|8
magnitude|float|%7.2f|-99.99|7
magtype|str|%-6s|-|6
mb|float|%7.2f|-999.0|7
mbid|int|%8ld|-1|8
meastype|str|%-10s|-|10
mechid|int|%8ld|-1|8
method|str|%-12s|-|12
mexpon|int|%3ld|-99|3
mff|float|%5.2f|99.99|5
mfferr|float|%5.2f|-9.99|5
ml|float|%7.2f|-999.0|7
mlid|int|%8ld|-1|8
mrf|float|%5.2f|99.99|5
mrferr|float|%5.2f|-9.99|5
mrr|float|%5.2f|99.99|5
mrrerr|float|%5.2f|-9.99|5
mrt|float|%5.2f|99.99|5
mrterr|float|%5.2f|-9.99|5
ms|float|%7.2f|-999.0|7
msid|int|%8ld|-1|8
mtf|float|%5.2f|99.99|5
mtferr|float|%5.2f|-9.99|5
mtid|int|%8ld|-1|8
mtt|float|%5.2f|99.99|5
mtterr|float|%5.2f|-9.99|5
nass|int|%4ld|-1|4
naxazm|float|%5.1f|-99.9|5
naxlength|float|%12.5e|-9.99999e+99|12
naxplg|float|%5.1f|-99.9|5
naxval|float|%5.2f|99.99|5
ncalib|float|%16.6f|-99.999999|16
ncalper|float|%16.6f|-1.0|16
ndef|int|%4ld|-1|4
ndp|int|%4ld|-1|4
ne|int|%8ld|-1|8
net|str|%-8s|-|8
netname|str|%-80s|-|80
nettype|str|%-4s|-|4
nfreq|int|%8ld|-1|8
nn|int|%8ld|-1|8
nrlpb|int|%3ld|-99|3
nrmw|int|%3ld|-99|3
ns|int|%8ld|-1|8
nsamp|int|%8ld|-1|8
nslpb|int|%3ld|-99|3
nsmw|int|%3ld|-99|3
nsta|int|%8ld|-1|8
nt|int|%8ld|-1|8
nwin|int|%6ld|-1|6
offdate|int|%8ld|-1|8
offset|float|%6.2f|-1.0|6
ondate|int|%8ld|-1|8
orid|int|%8ld|-1|8
original_endtime|float|%17.5f|9999999999.999|17
original_samprate|float|%11.7f|-1.0|11
original_time|float|%17.5f|-9999999999.999|17
ounits|str|%-16s|-|16
paxazm|float|%5.1f|999.9|5
paxlength|float|%12.5e|-9.99999e+99|12
paxplg|float|%5.1f|999.9|5
paxval|float|%5.2f|99.99|5
pdc|float|%6.2f|-999.0|6
per|float|%7.2f|-1.0|7
phase|str|%-8s|-|8
ppower|float|%7.4f|-1.0|7
prefor|int|%8ld|-1|8
probtype|str|%-8s|-|8
pubid|str|%-80s|-|80
qmlid|str|%-80s|-|80
qual|str|%-1s|-|1
radamp|float|%10.7f|-1.0|10
rake1|float|%6.1f|9999.9|6
rake2|float|%6.1f|9999.9|6
rayleigh|float|%15.6lg|-1.0|15
recipe|str|%-15s|-|15
rect|float|%7.3f|-1.0|7
refsta|str|%-6s|-|6
remark|str|%-80s|-|80
review|str|%-4s|-|4
rms|float|%13.6e|-9e+99|13
rsprm|str|%-1s|-|1
rsptype|str|%-6s|-|6
rstatus|str|%-12s|-|12
samprate|float|%11.7f|-1.0|11
scalib|float|%15.6lg|0.0|15
scm|float|%12.5e|-9.99999e+99|12
sdepth|float|%9.4f|-1.0|9
sdobs|float|%9.4f|-1.0|9
seaz|float|%7.2f|-999.0|7
segtype|str|%-1s|-|1
semax|float|%7.4f|-9.9999|7
semin|float|%7.4f|-9.9999|7
slo|float|%7.4f|-1.0|7
slodef|str|%-1s|-|1
slores|float|%7.2f|-999.0|7
slow|float|%7.2f|-1.0|7
slowd|float|%7.4f|-1.0|7
smajax|float|%9.4f|-1.0|9
smax|float|%7.4f|-9.9999|7
smin|float|%7.4f|-9.9999|7
sminax|float|%9.4f|-1.0|9
snet|str|%-8s|-|8
snmax|float|%7.4f|-9.9999|7
snmin|float|%7.4f|-9.9999|7
snname|str|%s|-|32
snr|float|%10.5g|-1.0|10
specfmt|str|%-12s|-|12
spectype|str|%-8s|-|8
srn|int|%8ld|-1|8
srname|str|%-40s|-|40
ssident|str|%-16s|-|16
sta|str|%-6s|-|6
stageid|int|%8ld|-1|8
staname|str|%-50s|-|50
stassid|int|%8ld|-1|8
statype|str|%-4s|-|4
stime|float|%8.2f|-1.0|8
str1|float|%5.1f|999.9|5
str2|float|%5.1f|999.9|5
stream|int|%8ld|-1|8
strike|float|%6.2f|-1.0|6
stt|float|%15.4f|-999999999.9999|15
stx|float|%15.4f|-999999999.9999|15
sty|float|%15.4f|-999999999.9999|15
stype|str|%-1s|-|1
stz|float|%15.4f|-999999999.9999|15
sxx|float|%15.4f|-999999999.9999|15
sxy|float|%15.4f|-999999999.9999|15
sxz|float|%15.4f|-999999999.9999|15
syy|float|%15.4f|-999999999.9999|15
syz|float|%15.4f|-999999999.9999|15
szz|float|%15.4f|-999999999.9999|15
tagid|int|%8ld|-1|8
tagname|str|%-8s|-|8
tapeblock|int|%5ld|-1|5
tapefile|int|%5ld|-1|5
tapename|str|%-20s|-|20
taper|str|%-12s|-|12
taxazm|float|%5.1f|999.9|5
taxlength|float|%12.5e|-9.99999e+99|12
taxplg|float|%5.1f|999.9|5
taxval|float|%6.2f|99.99|6
tbp|float|%10.1f|-1.0|10
tfile|str|%-64s|-|64
tfoff|int|%10ld|0|10
time|float|%17.5f|-9999999999.999|17
timecentryd|float|%15.3f|-9999999999.999|15
timedef|str|%-1s|-|1
timeres|float|%8.3f|-999.0|8
tmeas|float|%17.5f|-9999999999.999|17
tmnlpb|float|%5.1f|-99.9|5
tmnmw|float|%5.1f|-99.9|5
tmpp|float|%12.5e|-9.99999e+99|12
tmrp|float|%12.5e|-9.99999e+99|12
tmrr|float|%12.5e|-9.99999e+99|12
tmrt|float|%12.5e|-9.99999e+99|12
tmtp|float|%12.5e|-9.99999e+99|12
tmtt|float|%12.5e|-9.99999e+99|12
totdur|float|%12.2f|-1.0|12
tshift|float|%6.2f|0.0|6
twin|float|%9.2f|0.0|9
uncertainty|float|%7.2f|-1.0|7
units|str|%-12s|-|12
units1|str|%-12s|-|12
units2|str|%-12s|-|12
utime|float|%17.5f|9999999999.999|17
val1|float|%12.3f|-9999999.999|12
val2|float|%12.3f|-9999999.999|12
vang|float|%6.1f|-999.9|6
vmodel|str|%-15s|-|15
volname|str|%-6s|-|6
wfid|int|%8ld|-1|8
wgt|float|%6.3f|-1.0|6
newsta|str|%-6s|-|6
atype|str|%-50s|-|50
connection|str|%16s|-|16
target|str|%16s|-|16
inp|str|%-50s|-|50
q330sn|str|%-16s|-|16
balersn|str|%-6s|-|6
balerfirm|str|%-10s|-|10
baleron|str|%-3s|-|3
htmlinfo|str|%-3s|-|3
msdinfo|str|%-3s|-|3
onsecs|int|%6ld|-1|6
htmlsecs|int|%6ld|-1|6
msdsecs|int|%6ld|-1|6
data_start|float|%17.5f|-9999999999.999|17
data_end|float|%17.5f|9999999999.999|17
baler14_end|str|%-30s|-|30
baler14_start|str|%-30s|-|30
baler44_end|str|%-30s|-|30
baler44_start|str|%-30s|-|30
completed|float|%17.5f|-9999999999.999|17
dmc_end|float|%17.5f|9999999999.999|17
dmc_start|float|%17.5f|-9999999999.999|17
proc_end|float|%17.5f|9999999999.999|17
proc_start|float|%17.5f|-9999999999.999|17
rt_end|float|%17.5f|9999999999.999|17
rt_start|float|%17.5f|-9999999999.999|17
user|str|%16s|-|16
hostname|str|%-25s|-|25
gridname|str|%-15s|-|15
gridid|int|%8d|-1|8
provider|str|%-30s|-|30
power|str|%-30s|-|30
dutycycle|str|%-8s|-|8
equiptype|str|%-30s|-|30
cert_time|float|%17.5f|-9999999999.999|17
decert_time|float|%17.5f|9999999999.999|17
equip_install|float|%17.5f|-9999999999.999|17
equip_remove|float|%17.5f|9999999999.999|17
pdcc|str|%-15s|-|15
sdcc|str|%-15s|-|15
model|str|%-15s|-|15
disposition|str|%16s|-|16
execution|str|%-100s|-|100
error|str|%-100s|-|100
dlcalseq|str|%-30s|-|30
dlcalseqt|str|%-30s|-|30
address|str|%s|-|32
pid|int|%6d|-1|6
dlcomment|str|%s|-|180
nor|int|%8d|-1|8
nph|int|%8d|-1|8
orb|str|%50s|-|50
fieldname|str|%-15s|-|15
dimensions|int|%3d|0|3
nv|int|%4d|-1|4
radius|float|%10.3f|-1.0|10
dx1nom|float|%7.2lf|-1.0|7
dx2nom|float|%7.2lf|-1.0|7
dx3nom|float|%7.2lf|-1.0|7
azimuth_y|float|%7.2lf|-1.0|7
n1|int|%4d|-1|4
n2|int|%4d|-1|4
n3|int|%4d|-1|4
xlow|float|%10.3lf|-99999.999|10
xhigh|float|%10.3lf|-99999.999|10
ylow|float|%10.3lf|-99999.999|10
yhigh|float|%10.3lf|-99999.999|10
zlow|float|%10.3lf|-99999.999|10
zhigh|float|%10.3lf|-99999.999|10
i0|int|%4d|-1|4
j0|int|%4d|-1|4
k0|int|%4d|-1|4
cdefined|str|%-1s|-|1
geodefined|str|%-1s|-|1
pmelrun|str|%-5s|-|5
tsc|float|%10.3lf|-999.0|10
tscref|float|%10.3lf|-999.0|10
tscbias|float|%10.3lf|-999.0|10
sswrodgf|float|%15.6lg|-999.0|15
ndgf|int|%4d|-1|4
period|float|%12.3f|-89999999999.0|12
pc_1|float|%12.3f|-999.0|12
pc_5|float|%12.3f|-999.0|12
pc_25|float|%12.3f|-999.0|12
pc_50|float|%12.3f|-999.0|12
dlat|float|%15.9lf|-999.0|15
dlon|float|%15.9lf|-999.0|15
hclat|float|%15.9lf|-999.0|15
hclon|float|%15.9lf|-999.0|15
hcdepth|float|%9.4lf|-999.0|9
ztop|float|%9.4lf|-999.0|9
zbot|float|%9.4lf|-999.0|9
sigmamw|float|%7.2f|-999.0|7
netm0|float|%9.3e|-999.0|9
netf0|float|%7.2f|-999.0|7
neteqR|float|%7.2f|-999.0|7
quality|float|%7.2f|-999.0|7
usta|int|%8d|-1|8
rjsta|int|%8d|-1|8
vmodel3d|str|%-15s|-|15
email|str|%128s|-|128
stastr|str|%50s|-|50
comment|str|%s|-|180
thr|int|%8ld|-1|8
qcresult|str|%-32s|-|32
revsamp|int|%16d|-1|16
revp|float|%7.4f|-1.0|7
qdlon|float|%12.6lf|-999.0|12
qgridname|str|%-30s|-|30
minlat|float|%9.4lf|-999.0|9
maxlat|float|%9.4lf|-999.0|9
minlon|float|%9.4lf|-999.0|9
maxlon|float|%9.4lf|-999.0|9
maxval|float|%12.3f|-9999999.0|12
nlat|int|%10d|-1|10
nlon|int|%10d|-1|10
qgridfmt|str|%-10s|-|10
qgridtype|str|%-20s|-|20
replay_time|float|%17.5f|-9999999999.999|17
fixed|str|%1s|-|1
filebytes|int|%10ld|-1|10
attempts|int|%4d|0|4
md5|str|%-32s|-|32
status|str|%-15s|-|15
bandwidth|float|%6.1f|0.0|6
msdtime|float|%17.5f|-9999999999.999|17
imagedescrip|str|%-64s|-|64
format|str|%-10s|-|10
imagename|str|%-64s|-|64
imagesize|str|%-25s|-|25
siteimagetype|str|%-20s|-|20
firm|str|%-30s|-|30
nreg24|int|%6ld|-1|6
last_reg|float|%17.5f|9999999999.999|17
nreboot|int|%6ld|-1|6
last_reboot|float|%17.5f|9999999999.999|17
m0|float|%9.3e|-999.0|9
f0|float|%7.2f|-999.0|7
eqR|float|%7.2f|-999.0|7
distmw|float|%7.2f|-999.0|7
rotaz|float|%7.2f|-999.0|7
chamw|str|%-8s|-|8
Pmw|str|%-4s|-|4
Smw|str|%-4s|-|4
timePmw|float|%17.5f|-9999999999.999|17
timeSmw|float|%17.5f|-9999999999.999|17
PGV|float|%15.6f|-999.0|15
PSA03|float|%15.6f|-999.0|15
PSA10|float|%15.6f|-999.0|15
PSA30|float|%15.6f|-999.0|15
Arias|float|%15.6f|-999.0|15
Housner|float|%15.6f|-999.0|15
dista|float|%7.2f|-1.0|7
Scoll|str|%-256s|-|256
Sobj|str|%-64s|-|64
Szone|str|%-30s|-|30