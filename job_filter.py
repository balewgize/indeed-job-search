"""
Filter job posts based on different parameters
"""

def get_positions():
    """ Filter by postion."""
    print('-'*50)
    print("\nWhat postion you want to apply for?\n")
    print('Enter one position per line. (type "END" when finished)\n')

    positions = []

    answer = input()
    while answer.lower() != "end":           
        if answer != '':
            positions.append(f'"{answer}"')
        answer = input()

    return positions


def get_locations():
    """ Filter by location."""
    print('-'*50)
    print("\nWhere would you like to work?\n")
    print('Enter one location per line. (type "END" when finished)\n') 

    locations = []

    answer = input()
    while answer.lower() != "end":            
        if answer != '':
            locations.append(answer)
        answer = input()

    return locations


def get_job_types():
    """ Filter by job type."""
    print('-'*50)
    type_list = ['fulltime', 'contract', 'parttime', 'internship']
    types = ['Full time', 'Contract', 'Part time', 'Internship']

    print("\nWhat type of jobs would you like to work on?\n")
    print(*types, sep=', ')
    print('\nEnter one job type per line. (type "END" when finished)\n')
    
    job_types = []

    answer = input()
    while answer.lower() != "end":           
        if answer != '':
            if answer.lower().startswith('full'):
                job_types.append(type_list[0])
            if answer.lower().startswith('cont'):
                job_types.append(type_list[1])
            if answer.lower().startswith('part'):
                job_types.append(type_list[2])
            if answer.lower().startswith('intern'):
                job_types.append(type_list[3])
        answer = input()

    return job_types


def get_experiences():
    """ Filter by experience level."""
    print('-'*50)
    exp_list = ['entry_level', 'mid_level', 'senior_level']
    exps = ['Entry level', 'Mid level', 'Senior level']

    print("\nWhat level of experience(s) do you have?\n")
    print(*exps, sep=', ')
    print("\nEnter your level of experience one per line. (type END when finished)\n")

    experience = []

    answer = input()
    while answer.lower() != "end":            
        if answer != '':
            if answer.lower().startswith('entry'):
                experience.append(exp_list[0])
            if answer.lower().startswith('mid'):
                experience.append(exp_list[1])
            if answer.lower().startswith('senior'):
                experience.append(exp_list[2])
        answer = input()

    return experience