"""
Filter job posts based on different parameters
"""

def get_positions():
    """ Filter by postion."""
    print("\nWhat postion you want to apply for?\n")
    print('Enter one position per line. (type "END" when finished)\n')

    positions = []

    answer = input()
    while answer != "END":            
        if answer != '':
            positions.append(answer)
        answer = input()

    return positions


def get_locations():
    """ Filter by location."""
    print("\nWhere would you like to work?\n")
    print('Enter one location per line. (type "END" when finished)\n') 

    locations = []

    answer = input()
    while answer != "END":            
        if answer != '':
            locations.append(answer)
        answer = input()

    return locations


def get_job_types():
    """ Filter by job type."""
    type_list = ['fulltime', 'contract', 'parttime', 'internship']
    types = ['Full time', 'Contract', 'Part time', 'Internship']
    
    print("\nWhat type of jobs would you like to work on?\n")
    print(*types, sep=', ')
    print('\nEnter one job type per line. (type "END" when finished)\n')
    
    job_types = set()

    answer = input()
    while answer != "END":            
        if answer != '':
            if answer.lower().startswith('full'):
                job_types.add(type_list[0])
            if answer.lower().startswith('cont'):
                job_types.add(type_list[1])
            if answer.lower().startswith('part'):
                job_types.add(type_list[2])
            if answer.lower().startswith('intern'):
                job_types.add(type_list[3])
        answer = input()

    return job_types


def get_experiences():
    """ Filter by experience level."""
    exp_list = ['entry_level', 'mid_level', 'senior_level']
    exps = ['Entry level', 'Mid level', 'Senior level']

    print("\nWhat level of experience(s) do you have?\n")
    print(*exps, sep=', ')
    print("\nEnter your level of experience one per line. (type END when finished)\n")

    experience = set()

    answer = input()
    while answer != "END":            
        if answer != '':
            if answer.lower().startswith('entry'):
                experience.add(exp_list[0])
            if answer.lower().startswith('mid'):
                experience.add(exp_list[1])
            if answer.lower().startswith('senior'):
                experience.add(exp_list[2])
        answer = input()

    return experience