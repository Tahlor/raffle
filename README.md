# Raffler!

Have your friends fill out a form designating how many tickets they've earned. Each week this system will email the group who the lucky winner is! 


## Google Sheets API
You'll need to set up a Project with Google and get a Google Sheets API. This script requires read permissions only.


## Scripts
There are 3 scripts: one that sends a soliciation email, another for a reminder, and the last to designate the winner. All of the parameters are just globals in the `utils.py' script.

Parameters:

* Day offsets -- assumed the raffle is weekly, how many days from Sunday does it start/end; only forms received during the specified window are counted
* Penalties -- experimental; if you want to fiddle with penalizing recent winners
* Random seed -- So the person running the script can't choose a random seed to guarantee they win. Basically everyone submits a random number (except the person running the script), which is combined to generate the seed. The code to reproduce this result is included in the email.
* Simulation -- the raffle is performed hypothetically many times so users can verify their tickets were counted appropriately

## Cron
These can be easily scheduled in cron. Just type `crontab -e' to get started. Here is an example where reminders are sent on Tuesday and the raffle is performed on Wednesday.

    00 6  * * 2 cd /home/pi/Projects/raffle && python3 send_reminder.py >> ./cron_reminder.log 2>&1
    00 6  * * 3 cd /home/pi/Projects/raffle && python3 generate_winner.py >> ./cron_winner.log 2>&1
    30 20 * * 2 cd /home/pi/Projects/raffle && python3 final_reminder.py >> ./cron_reminder.log 2>&1



