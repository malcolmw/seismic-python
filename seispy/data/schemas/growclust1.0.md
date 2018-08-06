# growclust1.0
## Relations/tables
### catalog
year, month, day, hour, minute, second, eID, latR, lonR, depR, mag, qID, cID, nbranch, qnpair, qndiffP, qndiffS, rmsP, rmsS, eh, ez, et, latC, lonC, depC
## Attributes/fields
field|dtype|format|null|width
---|---|---|---|---
year|int|%4d|-999|4
month|int|%02d|-9|2
day|int|%02d|-9|2
hour|int|%03d|-99|3
minute|int|%03d|-99|3
second|float|%6.3f|-9.999|6
eID|int|%10d|-999999999|10
latR|float|%9.5f|-99.99999|9
lonR|float|%10.5f|-999.99999|10
depR|float|%7.3f|-99.999|7
mag|float|%5.2f|-9.99|5
qID|int|%7d|-999999|7
cID|int|%7d|-999999|7
nbranch|int|%7d|-999999|7
qnpair|int|%5d|-9999|5
qndiffP|int|%5d|-9999|5
qndiffS|int|%5d|-9999|5
rmsP|float|%5.2f|-9.99|5
rmsS|float|%5.2f|-9.99|5
eh|float|%7.3f|-99.999|7
ez|float|%7.3f|-99.999|7
et|float|%7.3f|-99.999|7
latC|float|%11.5f|-9999.99999|11
lonC|float|%10.5f|-999.99999|10
depC|float|%7.3f|-99.999|7