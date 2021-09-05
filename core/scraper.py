"""
Scrape job post from https://www.indeed.com
"""

import requests
import time, random
from datetime import datetime
from bs4 import BeautifulSoup


class Scraper():
    """ Indeed job scraper class.

    Scrape job posts from www.indeed.com based on user preference and return
    details about the jobs including: Job title, position, company, location,
    salary(if any), post date, job summary, and job url.
    """
    def __init__(self):
        self.url = 'https://www.indeed.com/jobs'
        self.data = {
            'Job Title': [],
            'Position': [],
            'Company': [],
            'Location': [],
            'Salary': [],
            'Posted': [],
            'Extracted': [],
            'Summary': [],
            'Job URL': [],
        }

    def search_jobs(self, preferences):
        """ Search jobs based on user preference."""
        headers = {
            'user-agent': 'Mozilla/5.0',
        }
        response = requests.get(self.url, headers=headers, params=preferences)
        return response

    def get_job_detail(self, card, position):
        """ Extract the Job details for a single job."""
        title_con = card.find('h2', 'jobTitle').contents[-1]
        job_title = title_con.text.strip()

        company_con = card.find('span', 'companyName')
        company = company_con.text.strip()

        location_con = card.find('div', 'companyLocation')
        if len(location_con.contents) == 1:
            location = location_con.text.strip()
        elif len(location_con) > 1:
            location = location_con.contents[0].strip()
        else:
            location = ''


        posted = card.find('span', 'date').text.strip()
        today = datetime.today().strftime("%Y-%m-%d")

        summary = card.find('div', 'job-snippet').text.strip()
        job_url = f"https://www.indeed.com{card.get('href')}"

        try:
            salary = card.find('span', 'salary-snippet').text.strip()
        except AttributeError:
            salary = 'N/A'

        return [job_title, position, company, location, salary, posted, today, summary, job_url]

    def extract_page(self, html, position):
        """ Extract details for all jobs on a single page."""
        cards = html.find_all('a', 'tapItem')

        for card in cards:
            job = self.get_job_detail(card, position)
            for column, value in zip(self.data.keys(), job):
                self.data[column].append(value)

    def extract_all_pages(self, first_page, position):
        """ Extract all result pages appeared."""
        self.extract_page(first_page, position)
        current_page = first_page
        
        while True:
            next_page = current_page.find('a', {'aria-label': 'Next'})
            try:
                next_url = f"https://www.indeed.com{next_page.get('href')}"
            except AttributeError:
                # we reach the end of all job posts (no next button)
                break

            response = requests.get(next_url)
            current_page = BeautifulSoup(response.content, 'lxml')
            self.extract_page(current_page, position)

            time.sleep(random.randint(6, 10))

        return self.data