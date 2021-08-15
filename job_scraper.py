"""
Scrape job post from https://www.indeed.com
"""

import requests
import time, random
from datetime import datetime
from bs4 import BeautifulSoup


class IndeedJobScraper():
    """ Indeed job scraper.

    Scrape job posts from www.indeed.com based on user preferences

    returns:
        list of jobs
    """
    def __init__(self):
        self.url = 'https://www.indeed.com/jobs'
        self.data = {
            'Job Title': [],
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

    def get_job_detail(cself, card):
        """ Extract the Job details for a single job."""
        title_con = card.find('h2', 'jobTitle').contents[-1]
        job_title = title_con.text.strip()

        company_con = card.find('span', 'companyName')
        company = company_con.text.strip()

        location_con = card.find('div', 'companyLocation')
        location = location_con.contents[0].strip()

        posted = card.find('span', 'date').text.strip()
        today = datetime.today().strftime("%Y-%m-%d")

        summary = card.find('div', 'job-snippet').text.strip()
        job_url = f"https://www.indeed.com{card.get('href')}"

        try:
            salary = card.find('span', 'salary-snippet').text.strip()
        except AttributeError:
            salary = 'N/A'

        # job = {
        #     'job_title': job_title,
        #     'company': company,
        #     'location': location,
        #     'salary': salary,
        #     'posted': posted,
        #     'extracted': today,
        #     'job_summary': job_summary,
        #     'job_url': job_url
        # }
        return [job_title, company, location, salary, posted, today, summary, job_url]

    def extract_page(self, html):
        """ Extract details for all jobs on a single page."""
        cards = html.find_all('a', 'tapItem')
        # job_list = []

        for card in cards:
            job = self.get_job_detail(card)
            for column, value in zip(self.data.keys(), job):
                self.data[column].append(value)
            # job_list.append(job)

    def extract_all_pages(self, current_page):
        """ Extract next result pages from the current page."""

        while True:
            next_page = current_page.find('a', {'aria-label': 'Next'})
            try:
                next_url = f"https://www.indeed.com{next_page.get('href')}"
            except AttributeError:
                # we reach the end of all job posts (no next button)
                break

            response = requests.get(next_url)
            current_page = BeautifulSoup(response.content, 'lxml')
            self.extract_page(current_page)

            time.sleep(random.randint(6, 10))

        return self.data