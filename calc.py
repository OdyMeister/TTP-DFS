import math
import ast
import sys
import numpy as np
from TTP import *
from scipy.stats import beta, betabinom
from sklearn.metrics import r2_score


def adjusted_R2(x, expected, max_diff, a, b):
    pdf = beta.pdf(x, a, b, loc=0, scale=max_diff)
    r2 = r2_score(expected, pdf)
    return r2

def diff_beta_binom_fit(x, expected, max_diff, a, b):
    pdf = betabinom.pmf(x, max_diff, a, b, loc=0)
    score = np.sum((expected - pdf)**2)
    return score

def fit_beta_binom(x, data, max_diff):
    x = list(x)
    best_fit = np.inf
    best_pmf = None
    expected = data / np.sum(data)

    # For loop to rougly find the best fit
    for a in np.arange(0, 10**3, 10):
        for b in np.arange(0, 10**3, 10):
            result = diff_beta_binom_fit(x, expected, max_diff, a, b)
            if result < best_fit:
                best_fit = result
                best_pmf = (a, b)
    
    # Refine the best fit with smaller step sizes
    for step in [10**s for s in range(-2, 5)]:
        currentA, currentB = best_pmf
        adj = step * 10
        for a in np.arange(currentA - adj, currentA + adj, step):
            for b in np.arange(currentB - adj, currentB + adj, step):
                result = diff_beta_binom_fit(x, expected, max_diff, a, b)
                if result < best_fit:
                    best_fit = result
                    best_pmf = (a, b)

    return best_pmf


# Verifies one given schedule
def verify(n, schedule, matchups, count):
    current = []
    prev_round1 = []
    streak = {i: {"home": 0, "away": 0} for i in range(n)}

    # Goes through each matchup in the schedule and checks for violations
    for matchup in schedule:
        # Matchups keeps track of all matchups that have not been used yet, if it is not in matchups, it has been used before
        if matchup not in matchups:
            print("Matchup used multiple times:", matchup)
        else:
            matchups.remove(matchup)

        # Check if a team is playing more than three times in a row at home
        if streak[matchup[0]]["home"] == 3:
            print(f"Home streak violation: {matchup}, Schedule#: {count}")
        streak[matchup[0]]["home"] += 1
        streak[matchup[0]]["away"] = 0

        # Check if a team is playing more than three times in a row on the road
        if streak[matchup[1]]["away"] == 3:
            print("Away streak violation", matchup)
        streak[matchup[1]]["away"] += 1
        streak[matchup[1]]["home"] = 0
        
        if len(current) < n//2:
            current.append(matchup)
        else:
            prev_round1 = current
            current = [matchup]

        for m in current:
            if (matchup[0] in m or matchup[1] in m) and m != matchup:
                print("Same team plays multiple times in one round", current, matchup, schedule)

        if (matchup[1], matchup[0]) in prev_round1:
            print(f"Back-to-back matchup, prev_round: {prev_round1}, current: {current}, schedule#: {count}")


# Calculate the difference between all schedules in a file
def calc_diff(filepath, n):
    with open(filepath, "r") as file:
        schedules = []
        name = filepath.split("\\")[-1].split(".")[0]

        dest = open(f"Differences/Diff {name}.csv", "w")
        dest_reduced = open(f"Differences/Diff Reduced {name}.csv", "w")
        dest_teamless = open(f"Differences/Diff Teamless {name}.csv", "w")

        # Read schedules from file and convert them to a list containing each round in the schedule
        for line in file:
            # Skip empty lines, such as the last line in a file
            if len(line) < 2:
                continue
            matchups = "(" + line.replace(" ", "),(").replace("\n", ")")
            raw_schedule = ast.literal_eval("[" + matchups + "]")
            schedule_chunks = [raw_schedule[i:i+n//2] for i in range(0, len(raw_schedule), n//2)]
            schedules.append(schedule_chunks)
        
        # Calculate the differences between all schedules
        # Both for the 'normal' schedules and the reduced schedules
        for s in range(len(schedules)):
            for c in range(s+1, len(schedules)):
                diff = 0            # Difference in matchups
                reduced_diff = 0    # Difference in matchups, disregarding home/away
                HA_diff = 0         # Difference in home/away assignments, i.e. disregarding the matchups themselves

                for r in range(len(schedules[s])):
                    home_games = np.array(schedules[c][r])[:, 0]
                    away_games = np.array(schedules[c][r])[:, 1]


                    for m in schedules[s][r]:
                        if m not in schedules[c][r]:
                            diff += 1
                        if not (m in schedules[c][r] or (m[1], m[0]) in schedules[c][r]):
                            reduced_diff += 1

                        # Comparing each round to see if each team has the same home/away assignment
                        # The difference is only based on the home/away assignments of each team in each round
                        if m[0] not in home_games:
                            HA_diff += 1
                            
                        if m[1] not in away_games:
                            HA_diff += 1


                dest.write(f"{diff},")
                dest_reduced.write(f"{reduced_diff},")
                dest_teamless.write(f"{HA_diff},")

        print("Differences calculated")

if __name__ == "__main__":
    filepath = sys.argv[1]
    n = int(sys.argv[2])
    calc_diff(filepath, n)
    # calc_uniformity(filepath)
    # sample_schedules(n, filepath, 10000)