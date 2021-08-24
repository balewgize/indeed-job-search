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


def get_experience():
    """ Filter by experience level."""
    print('-'*50)
    exp_list = ['entry_level', 'mid_level', 'senior_level']
    exps = ['Entry level', 'Mid level', 'Senior level']

    print("\nWhat level of experience(s) do you have?\n")
    print(*exps, sep=', ')
    print("\nEnter your level of experience: ")

    experience = ''

    answer = input()            
    if answer != '':
        if answer.lower().startswith('entry'):
            experience = exp_list[0]
        elif answer.lower().startswith('mid'):
            experience = exp_list[1]
        elif answer.lower().startswith('senior'):
            experience = exp_list[2]
        else:
            print('\nYou don\'t provide a correct experience level.\n')
            get_experience()
    else:
        print('\nExperience can\'t be empty.\n')
        get_experience()

    return experience