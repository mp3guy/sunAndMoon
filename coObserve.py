import argparse
import locale
import tzlocal
import matplotlib.pyplot as plt
from datetime import date, timedelta
from astral import LocationInfo, moon
from ics import Calendar, Event

def azimuth_to_bearing(azimuth):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(azimuth / 45) % 8
    return directions[index]

def find_overlapping_intervals(list1, list2):
    overlapping_intervals = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        start1, end1 = list1[i]
        start2, end2 = list2[j]

        # Check for overlap
        if end1 >= start2 and end2 >= start1:
            overlap_start = max(start1, start2)
            overlap_end = min(end1, end2)
            overlapping_intervals.append((overlap_start, overlap_end))

        # Move to the next interval in the appropriate list
        if end1 < end2:
            i += 1
        else:
            j += 1

    return overlapping_intervals

def get_cycles(obs, startDate, endDate):
    def get_next_rise(date):
        currDate = date
        while True:
            try:
                rise = moon.moonrise(obs, currDate)
                if rise is not None:
                    return currDate, rise
            except:
                currDate += day
                continue
            currDate += day

    def get_next_set(rise):
        currDate = rise.date()
        while True:
            try:
                set = moon.moonset(obs, currDate)
                if set is not None and set > rise:
                    return currDate, set
            except:
                currDate += day
                continue
            currDate += day

    cycles = []
    currDate = startDate
    while currDate < endDate:
        moonPhase = moon.phase(currDate)

        if moonPhase >= 10.5 and moonPhase < 24.5:
            currDate, rise = get_next_rise(currDate)
            currDate, set = get_next_set(rise)
            cycles.append((rise, set))

        currDate += day

    return cycles

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "")

    parser = argparse.ArgumentParser(description="Moon co-observation at two locations calculator",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--loc0", required=True, help="Location 0 name")
    parser.add_argument("--lat0", required=True, help="Latitude 0 in degrees")
    parser.add_argument("--lon0", required=True, help="Longitude 0 in degrees")
    parser.add_argument("--loc1", required=True, help="Location 1 name")
    parser.add_argument("--lat1", required=True, help="Latitude 1 in degrees")
    parser.add_argument("--lon1", required=True, help="Longitude 1 in degrees")
    parser.add_argument("--year", required=True, help="Year")
    parser.add_argument("--minAngle", default=0, help="Minimum elevation angle")
    parser.add_argument("--hourdelta", default=0, help="Hours to go from location 0 to location 1")
    parser.add_argument('-p', action='store_true')

    args = parser.parse_args()

    startDate = date(int(args.year), 1, 1)
    endDate = date(int(args.year) + 1, 1, 1)
    day = timedelta(days=1)
    minute = timedelta(minutes=1)
    offset = timedelta(hours=int(args.hourdelta))

    l0 = LocationInfo('', '', tzlocal.get_localzone_name(), args.lat0, args.lon0)
    l1 = LocationInfo('', '', tzlocal.get_localzone_name(), args.lat1, args.lon1)

    # First, find all the moon rise and set cycles for both locations
    l0Cycles = get_cycles(l0.observer, startDate, endDate)
    l1Cycles = get_cycles(l1.observer, startDate, endDate)
    overlapping = find_overlapping_intervals(l0Cycles, l1Cycles)

    # Create a new calendar
    c = Calendar()

    for start, end in overlapping:
        # Sample the elevations at each location over the overlapping time period
        times = []
        e0 = []
        e1 = []
        t = 0
        curr = start

        while curr < end:
            elevation0 = moon.elevation(l0.observer, curr)
            elevation1 = moon.elevation(l1.observer, curr)

            if elevation0 > 0 and elevation1 > 0:
                times.append(t)
                e0.append(elevation0)
                e1.append(elevation1)

            curr += minute
            t = t + 1

        if len(times) < 1:
            continue

        # Find the midpoint between the two elevation peaks
        bestTime = start + timedelta(minutes=(times[e0.index(max(e0))] + times[e1.index(max(e1))]) / 2)

        loc0Azimuth = moon.azimuth(l0.observer, bestTime)
        loc1Azimuth = moon.azimuth(l1.observer, bestTime)

        loc0Elevation = moon.elevation(l0.observer, bestTime)
        loc1Elevation = moon.elevation(l1.observer, bestTime)

        if loc0Elevation < float(args.minAngle) or loc1Elevation < float(args.minAngle):
            continue

        print(f"Time {args.loc0}: {date.strftime(bestTime, '%x %X')}, Bearing: {azimuth_to_bearing(loc0Azimuth)}, Elevation: {loc0Elevation:.2f}")
        print(f"Time {args.loc1}: {date.strftime(bestTime + offset, '%x %X')}, Bearing: {azimuth_to_bearing(loc1Azimuth)}, Elevation: {loc1Elevation:.2f}")
        print("")

        # Create a new event
        e = Event()

        # Set the event's name and start time
        e.name = f"{args.loc0} {azimuth_to_bearing(loc0Azimuth)} {loc0Elevation:.2f}"
        e.begin = bestTime
        e.location = f"{args.lat0}, {args.lon0}"

        # Add the event to the calendar
        c.events.add(e)

        if args.p:
            plt.plot(times, e0, 'o-', label=f'Elevation {args.loc0}')
            plt.plot(times, e1, 's-', label=f'Elevation {args.loc1}')

            plt.title('Moon Elevation')
            plt.xlabel('Time')
            plt.ylabel('Elevation (Degrees)')
            plt.legend()

            plt.show()

    # Write the calendar to a file
    with open("co-observation.ics", "w") as f:
        f.write(c.serialize())
