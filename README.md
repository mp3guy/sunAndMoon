# sunAndMoon
Script to calculate the times you can catch a solar or lunar rise or set for a location and direction.

Requires astral, ics and tzlocal, all in pip. Find the parameters you need on e.g. suncalc.org.

All events will be printed to the screen while an iCalendar file, `sun_moon_events.ics`, will be output in the current directory containing all events in a format you can import into e.g. Google Calendar. 

Usage:
```
$ python sunAndMoon.py -h
usage: sunAndMoon.py [-h] --loc LOC --lat LAT --lon LON --year YEAR --astart ASTART --aend AEND

Sun and Moon Set and Rise Calculator

options:
  -h, --help       show this help message and exit
  --loc LOC        Location name (default: None)
  --lat LAT        Latitude in degrees (default: None)
  --lon LON        Longitude in degrees (default: None)
  --year YEAR      Year (default: None)
  --astart ASTART  Azimuth start in degrees clockwise from North (default: None)
  --aend AEND      Azimuth end in degrees clockwise from North (default: None)
```

For example:
```
python sunAndMoon.py --loc Beach --lat 63.79913 --lon -20.88370 --year 2023 --astart 140 --aend 269
Sun rising at 01/01/23 11:10:52
Sun setting at 01/01/23 15:43:24
Sun rising at 02/01/23 11:09:52
Sun setting at 02/01/23 15:45:21
Sun rising at 03/01/23 11:08:46
...
```
