"""
Preferences/Job filters to get relevant jobs for the user
"""
import os, sys
import itertools

import filter


class Profile():
    """ User profile/preference to filter jobs."""
    def __init__(self):
        self.filename = '.job-preference.txt'
        self.home_dir = self.get_home_dir()

    def welcome(self):
        """ Show welcome message."""
        msg = 'Indeed Job Search'
        print(f"{'-'*50}\n{'Welcome!':^50}\n{msg:^50}\n{'-'*50}")
        print("""
        I use your job preference to search for jobs
        relevant to you.

        When I found relevant jobs, I immediately
        send you an email notification to enable
        you apply before a deadline.

        Lastly, I will search for jobs every
        Tuesday and Friday (You can adjust it to whatever
        you want). 

        No need of manually checking the website. 

        Now job searching on indeed.com is automated.
        """)
        print('-'*50, '\n')

    def get_home_dir(self):
        """ Get the home directory of the user."""
        if os.name == 'nt':  
            # windows OS
            return os.path.expanduser('~\\')
        else:
            # Unix-like OS
            return os.path.expanduser('~/')

    def get_user_preferences(self):
        """ Get the user preference to save for later use."""
        self.welcome()
        positions = filter.get_positions()
        locations = filter.get_locations()
        experience = filter.get_experience()

        self.save_user_preferences(positions, locations, experience)


    def save_user_preferences(self, positions, locations, experience):
        """ Save user preferences for later use."""
        def convert_to_str(iterable):
            """ Conver an iterable to comma separated string."""
            line = ''
            for item in iterable:
                line += item + ','
            return line[:-1]

        full_path = os.path.join(self.home_dir, self.filename)
    
        with open(full_path, 'w') as file:
            file.write(convert_to_str(positions)+'\n')
            file.write(convert_to_str(locations)+'\n')
            file.write(experience + '\n')


    def read_user_preferences(self):
        """ Read preferences of the user if it has been saved."""
        full_path = os.path.join(self.home_dir, self.filename)
        
        if os.path.exists(full_path):
            with open(full_path) as file:
                lines = file.readlines()
                lines = list(map(lambda x: x.replace('\n', ''), lines))
                positions = lines[0].split(',')
                locations = lines[1].split(',')
                experience = [lines[2].strip()]

                p = [positions, locations, experience]
                prefs = list(itertools.product(*p))
                short = ('q', 'l', 'explvl')
                params = [tuple(zip(short, param)) for param in prefs]

                return params
        else:
            ch = input('Would you like to set your job preference now? [Y/N]: ')
            if ch.lower() == 'y' or ch.lower() == 'yes':
                self.get_user_preferences()
                print('\nYour job preferences has been saved.')
                print('You can now run the script again to search for jobs matching your preferences.')
                sys.exit()
            else:
                print('Thank you!.')
                sys.exit()