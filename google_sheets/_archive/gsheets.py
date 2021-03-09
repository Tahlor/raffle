import re, urllib
import requests


def create_agent():
    s = requests.Session()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    s.headers.update({'user-agent': user_agent})
    return s


class Spreadsheet(object):
    def __init__(self, key):
        super(Spreadsheet, self).__init__()
        self.key = key

class Client(object):
    def __init__(self, email, password):
        super(Client, self).__init__()
        self.email = email
        self.password = password
        self.agent = create_agent()

    def _get_auth_token(self, email, password, source, service):
        url = "https://www.google.com/accounts/ClientLogin"
        params = {
            "Email": email, "Passwd": password,
            "service": service,
            "accountType": "HOSTED_OR_GOOGLE",
            "source": source
        }
        req = self.agent.post(url, params)
        return re.findall(r"Auth=(.*)", self.agent.get(req).content)[0]

    def get_auth_token(self):
        source = type(self).__name__
        return self._get_auth_token(self.email, self.password, source, service="wise")

    def download(self, spreadsheet, gid=0, format="csv"):
        url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
        headers = {
            "Authorization": "GoogleLogin auth=" + self.get_auth_token(),
            "GData-Version": "3.0"
        }
        req = self.agent.get(url_format % (spreadsheet.key, format, gid), headers=headers)
        return req.source

if __name__ == "__main__":
    import getpass
    import csv

    email = "taylornarchibald@gmail.com" # (your email here)
    password = getpass.getpass()
    spreadsheet_id = "" # (spreadsheet id here)

    # Create client and spreadsheet objects
    gs = Client(email, password)
    ss = Spreadsheet(spreadsheet_id)

    # Request a file-like object containing the spreadsheet's contents
    csv_file = gs.download(ss)

    # Parse as CSV and print the rows
    for row in csv.reader(csv_file):
        print(", ".join(row))