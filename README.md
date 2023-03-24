# sunAndMoon
Script to calculate the date ranges you can catch a solar or lunar rise or set for a location and direction.

Requires astral and tzlocal, both in pip. Find the parameters you need on e.g. suncalc.org

Usage:
```
$ python sunAndMoon.py --help
usage: sunAndMoon.py [-h] --lat LAT --lon LON --year YEAR --astart ASTART --aend AEND

Sun and Moon Set and Rise Calculator

options:
  -h, --help       show this help message and exit
  --lat LAT        Latitude in degrees (default: None)
  --lon LON        Longitude in degrees (default: None)
  --year YEAR      Year (default: None)
  --astart ASTART  Azimuth start in degrees clockwise from North (default: None)
  --aend AEND      Azimuth end in degrees clockwise from North (default: None)
```

For example:
```
python sunAndMoon.py --lat 63.79913 --lon -20.88370 --year 2023 --astart 140 --aend 269
Sun rising from 2023-01-01 to 2023-01-19
Moon setting from 2023-01-14 to 2023-02-06
Moon setting from 2023-02-10 to 2023-03-08
Sun setting from 2023-01-01 to 2023-03-18
Moon rising from 2023-03-13 to 2023-04-06
Moon rising from 2023-04-09 to 2023-06-09
Moon rising from 2023-07-05 to 2023-07-06
Moon setting from 2023-03-09 to 2023-07-09
Moon setting from 2023-08-02 to 2023-08-05
Moon setting from 2023-08-31 to 2023-09-02
Sun rising from 2023-11-24 to 2023-12-31
Sun setting from 2023-09-26 to 2023-12-31
```
