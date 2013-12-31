#!python 3
# https://www.codeeval.com/open_challenges/118/
# Your team is moving to a new office. In order to make it feel comfortable on a new place you decided to give the possibility to pick the places where they want to sit. After the team visited the new office, each team member gave you a list of working places that he/she would like to occupy. Your goal is to determine a possibility of making all of your team members feel comfortable according to those lists.

import fileinput, types
from collections import OrderedDict

def solve(preferences_by_person):
    prefs = OrderedDict()
    for person, seats in sorted(preferences_by_person.items(), key=lambda x: len(x[1])):
        prefs[person] = set(seats)
    return solve_inner(prefs, [])

def solve_inner(prefs, seats_assigned):
    if not prefs:
        # no-one left to seat!
        return True

    # Check necessary condition from Hall's marriage theorem
    seats_liked = set()
    for seats in prefs.values():
        seats_liked.update(seats)
    seats_liked.difference_update(seats_assigned)
    if len(seats_liked) < len(prefs):
        return False

    person, seats = prefs.popitem(last=False)

    for seat in seats:
        # try assigning person to seat
        if seat in seats_assigned:
            # seat already taken
            continue
        if solve_inner(prefs, seats_assigned + [seat]):
            return True

    # nothing worked
    return False
        

for line in fileinput.input():
    N, preferences_line = line.split(';', 1)
    N = int(N)
    # format is frustrating to parse, but happens to be Python literal :)
    preferences_by_person = eval("{%s}" % preferences_line)
    assert isinstance(preferences_by_person, dict)
    assert len(preferences_by_person) <= N
    answer = "Yes" if solve(preferences_by_person) else "No"
    print(answer)

