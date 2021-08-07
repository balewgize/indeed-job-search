"""
Indeed job notifier is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

Author: @balewgize
Date: August, 2013 E.C
"""

import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def basic_search():
    """ Perform basic job search based on postion and location."""
    position = input("What postion you want to apply?\n")
    if position == '':
        print('Please specify the postion you want to apply.')
        sys.exit()
    
    location = input("Where do you want to work?\n")    
    if location == '':
        print('Please specify the location you want to work on.')
        sys.exit()

    params = (
        ('q', position),
        ('l', location),
    )
    response = requests.get('https://www.indeed.com/jobs', params=params)
    return response


def get_job_detail(card):
    """ Extract the Job details for a single job."""
    job_title = card.find('h2', 'jobTitle').contents[-1].text.strip()
    company_name = card.find('span', 'companyName').text.strip()
    company_location = card.find('div', 'companyLocation').contents[0].strip()
    job_summary = card.find('div', 'job-snippet').text.strip()
    posted = card.find('span', 'date').text.strip()
    today = datetime.today().strftime("%Y-%m-%d")
    job_url = f"https://www.indeed.com{card.get('href')}"
    try:
        salary = card.find('span', 'salary-snippet').text.strip()
    except AttributeError:
        salary = ''

    job = [job_title, company_name, company_location, job_summary, posted, today, job_url]
    return job


def extract_page(html):
    """ Extract details for all jobs on a single page."""
    cards = html.find_all('a', 'tapItem')
    job_list = []
    for card in cards:
        job = get_job_detail(card)
        job_list.append(job)

    return job_list



def main():
    print('-'*50)
    print(f'Welcome to Indeed job scraper')
    print("\nWhat type of job search you want to do?\n")
    ch = input("Basic or Advanced (default: basic)\n")

    if ch.lower() == 'advanced':
        pass
    elif ch.lower() == 'basic' or ch == '':
        response = basic_search()
        html = BeautifulSoup(response.content, 'lxml')
        job_list = extract_page(html)
        print(len(job_list))
        print(job_list[0])


if __name__ == '__main__':
    main()