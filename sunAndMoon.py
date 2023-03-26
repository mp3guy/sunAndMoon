import argparse
import locale
import tzlocal
import sys

from datetime import date, timedelta
from astral import LocationInfo, sun, moon

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "")

    parser = argparse.ArgumentParser(description="Sun and Moon Set and Rise Calculator",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--lat", required=True, help="Latitude in degrees")
    parser.add_argument("--lon", required=True, help="Longitude in degrees")
    parser.add_argument("--year", required=True, help="Year")
    parser.add_argument("--astart", required=True, help="Azimuth start in degrees clockwise from North")
    parser.add_argument("--aend", required=True, help="Azimuth end in degrees clockwise from North")
    args = parser.parse_args()

    astart = int(args.astart)
    aend = int(args.aend)

    if aend <= astart:
        print(f"astart >= aend")
        sys.exit(1)

    currDate = date(int(args.year), 1, 1)
    endDate = date(int(args.year) + 1, 1, 1)
    day = timedelta(days=1)

    l = LocationInfo('', '', tzlocal.get_localzone_name(), args.lat, args.lon)

    def capture(body, eventAngle, event, time):
        if eventAngle >= astart and eventAngle <= aend:
            print(f"{body} {event} at {date.strftime(time, '%x %X')}")

    def moonCapture(eventFunc, eventName):
        time = None
        try:
            time = eventFunc(l.observer, currDate)
        except:
            pass
        if time is not None:
            capture("Moon", moon.azimuth(l.observer, time), eventName, time)

    while currDate < endDate:
        try:
            s = sun.sun(l.observer, date=currDate)
            capture("Sun", sun.azimuth(l.observer, dateandtime=s["sunrise"]), "rising", s["sunrise"])
            capture("Sun", sun.azimuth(l.observer, dateandtime=s["sunset"]), "setting", s["sunset"])
        except:
            pass

        moonPhase = moon.phase(currDate)

        if moonPhase >= 14 and moonPhase < 21:
            moonCapture(moon.moonrise, "rising")
            moonCapture(moon.moonset, "setting")

        currDate += day

