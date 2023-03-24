import argparse
import tzlocal
import sys

from datetime import date, timedelta
from astral import LocationInfo, sun, moon

if __name__ == "__main__":
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

    firstSunRise = None
    firstSunSet = None
    firstMoonRise = None
    firstMoonSet = None

    def capture(first, body, eventAngle, event):
        if eventAngle >= astart and eventAngle <= aend and currDate + day != endDate:
            if first is None:
                first = currDate
        elif first is not None:
            print(f"{body} {event} from {first} to {currDate}")
            first = None
        return first

    def moonCapture(eventFunc, first, eventName):
        event = None
        try:
            event = eventFunc(l.observer, currDate)
        except:
            pass
        if event is not None:
            first = capture(first, "Moon", moon.azimuth(l.observer, event), eventName)
        return first

    while currDate < endDate:
        try:
            s = sun.sun(l.observer, date=currDate)
            firstSunRise = capture(firstSunRise, "Sun", sun.azimuth(l.observer, dateandtime=s["sunrise"]), "rising")
            firstSunSet = capture(firstSunSet, "Sun", sun.azimuth(l.observer, dateandtime=s["sunset"]), "setting")
        except:
            pass

        moonPhase = moon.phase(currDate)

        if moonPhase >= 14 and moonPhase < 21:
            firstMoonRise = moonCapture(moon.moonrise, firstMoonRise, "rising")
            firstMoonSet = moonCapture(moon.moonset, firstMoonSet, "setting")

        currDate += day

