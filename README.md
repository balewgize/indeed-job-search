# Indeed Job Search
Automate Job search on www.indeed.com

Indeed job search is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's preference is posted.

It automatically checks for new job posts every Tuesday and Friday at 
06:00 AM if the device is connected to the internet.

If the device has no internet connection at that time, which is inevitable, 
it will check if the device comes online every thirty minutes.

The script can scheduled using cron jobs on Linux and Mac 
<a href="https://www.youtube.com/watch?v=QZJ1drMQz1A"> (Learn more) </a>


Or Windows Task Scheduler on Windows to be executed automatically.


## Requirement
- You need two Gmail account(one for sending, the other receiving)
- You need a Google App password to grant Gmail access to the script
- <a href="https://myaccount.google.com/apppasswords"> Set Google App password for accessing Gmail?</a>

## Usage
- Clone the repository to a directory you want
- Navigate to the indeed-job-search directory and open main.py
- in main() function, put your email address to be notified
- Add cron job task that execute run.py file every Tuesday and Friday
  at your prefered time (in 24 hour format) 
- <a href="https://crontab.guru/"> cron jobs to shchedule tasks in Linux</a>
- For example, the following cron job schedules the script to run every Tuesday and Friday at 05:00 AM (11:00 in 24 hour format)
```
00 11 * * 2,5 /usr/bin/python3 ~/python/projects/indeed-job-search/run.py
```
- You can have the same schedule using Windows Task Scheduler