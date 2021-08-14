"""
Preferences/Job filters to get relevant jobs for the user
"""
import os, sys
import job_filter


class Profile():
    """ User profile/preferences to filter jobs."""
    def __init__(self) -> None:
        self.filename = '.job-preferences.txt'
        self.home_dir = self.get_home_dir()

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
        positions = job_filter.get_positions()
        locations = job_filter.get_locations()
        job_types = job_filter.get_job_types() 
        experience = job_filter.get_experience()

        self.save_user_preferences(positions, locations, job_types, experience)


    def save_user_preferences(self, positions, locations, job_types, experience):
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
            file.write(convert_to_str(job_types)+'\n')
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
                job_types = lines[2].split(',')
                experience = lines[3].strip()

                sort_by = 'date'
                last_three_days = '3'

                # how to handle all variation of this preferences?

                params = (
                    ('q', positions[0]),
                    ('l', locations[0]),
                    ('jt', job_types[0]),
                    ('explvl', experience),
                    ('sort', sort_by),
                    ('fromage', last_three_days),
                )
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