from google_sheets import gsheets2
import re
from utils import *
import random
import warnings
from datetime import datetime, time, timedelta
from generate_winner import *

def remove_seed_from_raffle_dict(raffle_dict):
    for k,v in raffle_dict.items():
        if isinstance(v, dict):
            if "seed" in v:
                del v["seed"]
    return raffle_dict

def main():
    csv = get_google_sheets()
    raffle_dict, begin_submit, end_submit = filter_data(csv)
    raffle_dict = remove_seed_from_raffle_dict(raffle_dict)

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

