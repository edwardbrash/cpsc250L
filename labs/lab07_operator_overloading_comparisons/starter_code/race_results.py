# Lab 7: Race Results
#
# This program should work after you complete TimeDuration.

from time_duration import TimeDuration


def main():
    times = [
        TimeDuration(0, 42, 15),
        TimeDuration(0, 39, 58),
        TimeDuration(0, 44, 3),
        TimeDuration(0, 41, 20),
        TimeDuration(0, 39, 58),
    ]

    print("Original race times:")
    for time in times:
        print(time)

    print()
    print("Sorted race times:")
    sorted_times = sorted(times)

    for time in sorted_times:
        print(time)

    print()
    print("Fastest time:", sorted_times[0])
    print("Slowest time:", sorted_times[-1])

    print()
    print("Equality test:")
    print(times[1], "==", times[4], "?", times[1] == times[4])


main()
