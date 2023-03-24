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
Sun rising at 2023-01-01 11:10:52.291667+00:00
Sun setting at 2023-01-01 15:43:24.781064+00:00
Sun rising at 2023-01-02 11:09:52.887888+00:00
Sun setting at 2023-01-02 15:45:21.801333+00:00
Sun rising at 2023-01-03 11:08:46.460986+00:00
Sun setting at 2023-01-03 15:47:25.151194+00:00
Sun rising at 2023-01-04 11:07:33.249902+00:00
Sun setting at 2023-01-04 15:49:34.532214+00:00
Sun rising at 2023-01-05 11:06:13.499515+00:00
```
