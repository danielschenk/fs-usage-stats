#!/usr/bin/env python3

"""Calculate a list of the most IO time-consuming processes based on macOS' fs_usage"""

import argparse
import re


class ParseError(RuntimeError):
    pass


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__)
    parser.add_argument('logfile',
                        help='file containing the output of fs_usage',
                        metavar='PATH')
    parser.add_argument('-n',
                        help='maximum number of processes to show',
                        metavar='NUMBER',
                        type=int,
                        default=10)

    args = parser.parse_args()

    try:
        with open(args.logfile, 'r') as f:
            total_time = 0.0
            entries = {}

            for line in f.readlines():
                try:
                    entry = parse_line(line)
                except ParseError as e:
                    print(e)
                    continue

                time = entry['time']
                process = entry['process']
                total_time += time
                if process in entries:
                    entries[process] += time
                else:
                    entries[process] = time

            print(f'total time: {total_time}')
            for process in sorted(entries, key=lambda k: k[1])[:args.n]:
                time = round(float(entries[process]), 3)
                percentage = round(time * 100 / total_time, 3)
                print(f'{process:40} {time:4.3f} ({percentage:.3f} %)')

    except FileNotFoundError as e:
        parser.error(str(e))


def parse_line(line):
    match = re.search(r'(?P<time>\d+\.\d{6}) (?P<waitflag>[ W]) (?P<process>[\w. ]*\.\d+)', line)
    if not match:
        raise ParseError(f'could not parse line: "{line.strip()}"')

    try:
        time = float(match.group('time'))
    except ValueError as e:
        raise ParseError(e)

    return dict(process=match.group('process'), time=time,
                includes_wait_time=match.group('waitflag') == 'W')


if __name__ == '__main__':
    main()
