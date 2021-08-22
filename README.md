# Indeed Job Search
Automate Job search on www.indeed.com

Indeed job search is a python script that automates job searching on
indeed.com. It sends notification email to the user when a new job 
matching the user's preference is posted.

It automatically checks for new job posts every Tuesday and Friday at 
06:00 AM if the device is connected to the internet.

If the device has no internet connection at that time, which is inevitable, 
it will check if the device comes online every ten minutes.

The script can be scheduled using cron jobs on Linux and Mac 
<a href="https://www.youtube.com/watch?v=QZJ1drMQz1A"> (Learn more) </a>


Or Windows Task Scheduler on Windows to be executed automatically.


## Requirement
- You need two Gmail account(one for sending, the other for receiving emails)
- You need a Google App password to grant Gmail access to the script for sending emails
- Set up Google App password for accessing Gmail <a href="https://myaccount.google.com/apppasswords"> here </a>

## Usage
- Clone the repository to a directory you want
- Navigate to indeed-job-search directory and open main.py
- in main() function, put your email address to be notified
- now simply execute run.py from your Terminal (or schedule it)
- when the script asks you gmail address and Google App password, enter the gmail address you want to use for sending emails and the app pasword you set up in your Google account.
- Finally, dont' forget to enter your job preference as per the instruction given

BONUS:
- Add cron job task that execute run.py file every Tuesday and Friday
  at your prefered time (in 24 hour format) <a href="https://crontab.guru/">(Learn more)</a>
- For example, the following cron job schedules the script to run every Tuesday and Friday at 05:00 AM (11:00 in 24 hour format) on Linux/Mac (this is what I personally use)
```
00 11 * * 2,5 /usr/bin/python3 /path/to/indeed-job-search/run.py
```
- You can have the same schedule using Windows Task Scheduler(If you are on windows).