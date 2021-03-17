import sys
from datetime import datetime, timedelta, date
#from general_tools.my_email import email
sys.path.append("../utils/general_tools")
from my_email import email
import re

PATH="https://docs.google.com/spreadsheets/d/1rJNa1GHmQOBsny7d0i9iddZ8obq12TTbNqR_AiZsFII/edit#gid=720625117"
SHEET_ID = re.findall("(/d/)([A-Za-z0-9_)]+)", PATH)[0][1]
SHEET_NAME = "Form Responses 1"
#EMAIL_ADDRESSES = ["archibald@groups.io"]
EMAIL_ADDRESSES = ['taylornarchibald@gmail.com']
OFFSET = 1 # 0 assumes a Monday-Sunday week
REMINDER_SUBJ = "Archibald Healthy Lifestyle Challenge: Please report your point total for the week {} through {}"


def get_week(offset=0):
    """ Returns Monday through Sunday by default

    """
    today = date.today()
    start = today - timedelta(days=today.weekday()-offset)
    end = start + timedelta(days=6)
    return start, end

def get_formatted_start_end(offset=0):
    start,end = get_week(offset=offset)
    start = start.strftime('%b %d')
    end = end.strftime('%b %d')
    return start, end

def mail(title, message, addresses=["taylornarchibald@gmail.com"], **kwargs):
    email(addresses, "error@broadlink.com", title, message, useBWserver=False)

def dict_to_str(dictionary, message="Raffle entries:\n", html=True, header=[]):
    ps = message
    if html:
        ps += dict_to_html_table(dictionary, header=header)
    else:
        longest_key = max([len(key) for key in dictionary])
        for k,v in dictionary.items():
            padding = (longest_key + 1 - len(k)) * " "
            ps += f"{padding}{k}: {v}\n"

    return ps

TBL_FMT = '''<table>{}</table>'''
ROW_FMT = lambda n: '<tr>' + '<td>{}</td><td></td>' * n + '</tr>'

def dict_to_html_table(in_dict, n=None, header=[]):
    """
        header (list): list of column names
    """
    if n is None:
        items = next(iter(in_dict.items()))
        # If the value is just a primiative
        if isinstance(items[1], (str,int,float)):
            n = 2
            row_fmt = ROW_FMT(n)
            return TBL_FMT.format(''.join(header + [row_fmt.format(k,v) for k,v in in_dict.items()]))
        else: # if the value is iterable
            n = len(items[1]) + 1
            row_fmt = ROW_FMT(n)
            if header:
                header = [row_fmt.format(*header)]
            if isinstance(items[1], dict):
                return TBL_FMT.format(''.join(header + [row_fmt.format(k,*v.values()) for k,v in in_dict.items()]))
            else:
                return TBL_FMT.format(''.join(header + [row_fmt.format(k,*v) for k,v in in_dict.items()]))


if __name__=='__main__':
    mail()
