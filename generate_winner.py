from google_sheets import gsheets2
import re
from utils import *
import random
import warnings
from datetime import datetime, time

PATH="https://docs.google.com/spreadsheets/d/1rJNa1GHmQOBsny7d0i9iddZ8obq12TTbNqR_AiZsFII/edit#gid=720625117"
SHEET_ID = re.findall("(/d/)([A-Za-z0-9_)]+)", PATH)[0][1]
SHEET_NAME = "Form Responses 1"
EMAIL_ADDRESSES = ["taylornarchibald@gmail.com"]
OFFSET = 0

def get_google_sheets():
    new_responses = gsheets2.main(SHEET_ID, SHEET_NAME, r"./google_sheets/credentials_oauth2.json",
                                                       r"./google_sheets/token.pickle")
    return new_responses

def filter_data(data):
    # Get correct days
    # Get last week + 1 day
    _, first_submission_time = get_week(offset=-8+OFFSET) # on the last day of the cycle
    last_possible_submission_time = datetime.now()
    first_submission_time = datetime.combine(first_submission_time, time(0, 0))

    raffle_dict = {}
    # if there are multiple submissions, the most recent on in the valid timeframe is used
    for row in data[1:]:
        date = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S")
        if first_submission_time < date < last_possible_submission_time:
            name = row[2]
            raw = int(row[1])
            if raw >= 50:
                entries = 2
            elif raw >= 40:
                entries = 1
            # elif raw <= 2:
            #     entries = raw
            else:
                entries = 0

            if name in raffle_dict.keys():
                warnings.warn(f"{name} already entered! Old: {raffle_dict[name]} New: {entries}")
            raffle_dict[name] = entries
    return raffle_dict, first_submission_time, last_possible_submission_time

def perform_raffle(raffle_dict):
    return random.choices(list(raffle_dict.keys()), raffle_dict.values(), k=1)[0]

def send_result(winner, post_script=""):
    start,end = get_formatted_start_end()
    message = f"The winner for the week {start}-{end} is {winner}"
    mail(message, f"Congratulations {winner}!"+post_script, addresses=EMAIL_ADDRESSES)
    return message

def main():
    csv = get_google_sheets()
    raffle_dict, begin_submit, end_submit = filter_data(csv)
    print(raffle_dict)

    winner = perform_raffle(raffle_dict)
    ps = f"\n\n Begin entries: {begin_submit.strftime('%m-%d-%Y %H:%M:%S')}\nEnd submission: {end_submit.strftime('%m-%d-%Y %H:%M:%S')}"
    message = send_result(winner, post_script=ps)
    print(message)

if __name__=='__main__':
    main()
