from utils import mail, get_week, get_formatted_start_end
from generate_winner import *

def send_reminder():
    start,end = get_formatted_start_end(offset=OFFSET)
    mail(f"Please respond to the form for the week {start} through {end}",
         "https://forms.gle/Ac4huh4SypawC6mQ8", addresses=EMAIL_ADDRESSES)

if __name__=='__main__':
    send_reminder()