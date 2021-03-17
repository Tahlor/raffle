import sys
from google_sheets import gsheets2
import re
from utils import *
import random
import warnings
from datetime import datetime, time, timedelta
from collections import Counter


def get_google_sheets():
    new_responses = gsheets2.main(SHEET_ID, SHEET_NAME, r"./google_sheets/credentials_oauth2.json",
                                                       r"./google_sheets/token.pickle")
    return new_responses

def filter_data(data):
    # Get correct days
    # Get last week + 1 day
    _, first_submission_time = get_week(offset=-7+OFFSET) # midnight on the last day of the cycle, (which is 24 hours before the cycle ends)
    first_submission_time = datetime.combine(first_submission_time, time(0, 0))
    last_possible_submission_time = min(datetime.now(),first_submission_time + timedelta(days=3))
    raffle_dict = {}
    # if there are multiple submissions, the most recent on in the valid timeframe is used
    print(data)
    for row in data[1:]:
        date = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
        if first_submission_time < date < last_possible_submission_time:
            name = row[2]
            raw = int(row[1])
            entries = raw

            if name in raffle_dict.keys():
                warnings.warn(f"{name} already entered! Old: {raffle_dict[name]} New: {entries}")
            # Add 0 random seed
            if len(row) < 4:
                row.append(0)
            raffle_dict[name] = {"entries":entries, "seed":int(row[3])}
    return raffle_dict, first_submission_time, last_possible_submission_time

def perform_raffle(raffle_dict):
    keys = list(raffle_dict.keys())
    values = [raffle_dict[key]["entries"] for key in raffle_dict.keys()]
    random_seeds = sum([raffle_dict[key]["seed"] for key in raffle_dict.keys()])
    tickets = sum(values)
    DATE = int(datetime.combine(datetime.today(), time.min).timestamp())
    seed = ( tickets * DATE + random_seeds ) % sys.maxsize
    #seed = random.randrange(sys.maxsize) + sum([item[1] for item in raffle_dict.items()])
    rng = random.Random(seed)
    seed_text = f"Tickets: {tickets}, Seeds: {random_seeds}, Date: {DATE}\n"
    seed_text+= f"( {tickets}*{DATE} + {random_seeds} ) % {sys.maxsize} = {seed} \n"
    choices = rng.choices(keys, values, k=10000)
    simulated_choices = Counter(choices)
    return choices[0], simulated_choices, seed, seed_text

def send_result(winner, post_script=""):
    start,end = get_formatted_start_end(offset=OFFSET-7)
    message = f"Healthy Lifestyle Challenge: The winner for the week {start}-{end} is {winner}"
    mail(message, f"Congratulations {winner}!"+post_script, addresses=EMAIL_ADDRESSES)
    return message

def main():
    csv = get_google_sheets()
    raffle_dict, begin_submit, end_submit = filter_data(csv)
    print(raffle_dict)
    if raffle_dict:
        winner, simulated_choices, seed, seed_text = perform_raffle(raffle_dict)
    else:
        winner = "OOPS! There were no eligble entries!"
    ps = f"\n\nBegin entries: {begin_submit.strftime('%m-%d-%Y %H:%M:%S')}\nEnd submission: {end_submit.strftime('%m-%d-%Y %H:%M:%S')}\n\n"
    ps += dict_to_str(raffle_dict,  header=["Name","Entries","Random Seed"])
    ps += dict_to_str(simulated_choices, "\n10,000 Simulations\n")
    ps += f"\n{seed_text}\n"
    ps += f"""
import random, sys
raffle_dict = {raffle_dict}
rng = random.Random({seed})
choice = rng.choices(list(raffle_dict.keys()), raffle_dict.values(), k=1)[0]
print(choice)

            """

    message = send_result(winner, post_script=ps)
    print(message)

if __name__=='__main__':
    main()
