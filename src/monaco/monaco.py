import datetime
import argparse
import sys
import os
from dataclasses import dataclass


@dataclass
class PilotStats:
    abbreviation: str
    position: int
    name: str
    team: str
    fastest_lap: datetime.timedelta


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def build_report(file):
    pilots = {}
    lap_times = {}
    report = []
    with open(os.path.join(file, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            pilots[abbreviation] = (name, team,)
    with open(os.path.join(file, end))as end_file:
        for line in end_file.read().split("\n"):
            abbreviation = line[:3]
            end_datetime = line[3:]
            lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    with open(os.path.join(file, start)) as start_file:
        for line in start_file.read().split("\n"):
            abbreviation = line[:3]
            start_datetime = line[3:]
            lap_times[abbreviation] -= datetime.datetime.fromisoformat(start_datetime)
    sorted_laps = list(lap_times.items())
    sorted_laps.sort(key=lambda i: i[1])
    for position, abbr_time_tuple in enumerate(sorted_laps, 1):
        abbreviation, lap_time = abbr_time_tuple
        name, team = pilots[abbreviation]
        fastest_lap = lap_time
        report.append(PilotStats(abbreviation, position, name, team, fastest_lap))
    return report
