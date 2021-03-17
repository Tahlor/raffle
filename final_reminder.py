from google_sheets import gsheets2
import re
from utils import *
import random
import warnings
from datetime import datetime, time, timedelta
from generate_winner import *

def perform_raffle(raffle_dict):
    return random.choices(list(raffle_dict.keys()), raffle_dict.values(), k=1)[0]

def main():
    csv = get_google_sheets()
    raffle_dict, begin_submit, end_submit = filter_data(csv)
    print(raffle_dict)

    start,end = get_formatted_start_end(offset=OFFSET-7)
    subj = "RE: " + REMINDER_SUBJ.format(start,end)

    message = "Last call! The current totals are: \n"
    message = dict_to_str(raffle_dict, message, header=["Name","Entries","Random Seed"])

    message += "\nReporting form: https://forms.gle/Ac4huh4SypawC6mQ8"
    print(message)
    mail(subj, message, addresses=EMAIL_ADDRESSES)

if __name__=='__main__':
    main()

