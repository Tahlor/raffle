from utils import mail, get_week, get_formatted_start_end
from generate_winner import *

def send_reminder():
    start,end = get_formatted_start_end(offset=OFFSET-7)
    mail(REMINDER_SUBJ.format(start,end),
         f"This form is due tonight at midnight.\nhttps://forms.gle/Ac4huh4SypawC6mQ8", addresses=EMAIL_ADDRESSES)

if __name__=='__main__':
    send_reminder()
