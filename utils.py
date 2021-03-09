from datetime import datetime, timedelta, date
from general_tools.my_email import email

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

def mail(title, message, addresses=["taylornarchibald@gmail.com"]):
    email(addresses, "error@broadlink.com", title, message, useBWserver=False)


if __name__=='__main__':
    mail()