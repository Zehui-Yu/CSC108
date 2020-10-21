""" CSC108 Assignment 3: Club Recommendations - Starter code."""
from typing import List, Tuple, Dict, TextIO


# Sample Data (Used by Doctring examples)

P2F = {'Jesse Katsopolis': ['Danny R Tanner', 'Joey Gladstone',
                            'Rebecca Donaldson-Katsopolis'],
       'Rebecca Donaldson-Katsopolis': ['Kimmy Gibbler'],
       'Stephanie J Tanner': ['Michelle Tanner', 'Kimmy Gibbler'],
       'Danny R Tanner': ['Jesse Katsopolis', 'DJ Tanner-Fuller',
                          'Joey Gladstone']}

P2C = {'Michelle Tanner': ['Comet Club'],
       'Danny R Tanner': ['Parent Council'],
       'Kimmy Gibbler': ['Rock N Rollers', 'Smash Club'],
       'Jesse Katsopolis': ['Parent Council', 'Rock N Rollers'],
       'Joey Gladstone': ['Comics R Us', 'Parent Council']}

P2F2 = {'Kat Wang': ['Sunny Sun', 'Lily Tang', 'Tom Huang'],
        'Owen Sun': ['Leo Li', 'Leo Chen'],
        'Eva Ji': ['Gillian Wu', 'Kevin Wang', 'Andy Fu']}

P2C2 = {'Kat Wang': ['Parent Council', 'Rock N Rollers'],
        'Owen Sun': ['Comet Club'],
        'Leo Li': ['Art and Science', 'Rock N Rollers', 'Smash Club']}

# Helper functions 

def update_dict(key: str, value: str,
                key_to_values: Dict[str, List[str]]) -> None:
    """Update key_to_values with key/value. If key is in key_to_values,
    and value is not already in the list associated with key,
    append value to the list. Otherwise, add the pair key/[value] to
    key_to_values.

    >>> d = {'1': ['a', 'b']}
    >>> update_dict('2', 'c', d)
    >>> d == {'1': ['a', 'b'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    >>> update_dict('1', 'c', d)
    >>> d == {'1': ['a', 'b', 'c'], '2': ['c']}
    True
    """

    if key not in key_to_values:
        key_to_values[key] = []
        
    if value not in key_to_values[key]:
        key_to_values[key].append(value)


# Required functions


def remove_empty_keys(person_to_friends_club: Dict[str, List[str]]) -> Dict:
    
    """Return a new dictionary based on exisiting dictionary but with empty keys
    removed.
    >>> person_to_friends_club = {'Lily':[], 'Tom':[Lily]}
    >>> remove_empty_keys(person_to_friends_club)
    {'Tom':[Lily]}
    >>> person_to_friends_club = {'Kat Wang':
    ['Parent Council', 'Rock N Rollers'], 'Tom':[]}
    {'Kat Wang':['Parent Council', 'Rock N Rollers']}
    """
    delete = []
    for key in person_to_friends_club:
        if person_to_friends_club[key] == []:
            delete.append(key)
    for item in delete:
        person_to_friends_club.pop(item)


def load_profiles(profiles_file: TextIO) -> Tuple[Dict[str, List[str]],
                                                  Dict[str, List[str]]]:
    """Return a two-item tuple containing a "person to friends" dictionary
    and a "person_to_clubs" dictionary with the data from profiles_file.

    NOTE: Functions (including helper functions) that have a parameter of type
          TextIO do not need docstring examples.
    """
    person_to_friends = {}
    person_to_clubs = {}
    start = False
    for line in profiles_file:
        line = line.strip()
        if line == '':
            start = False
        elif start is False and ',' in line:
            name = " ".join(line.split(', ')[:: -1])
            person_to_friends[name] = []
            person_to_clubs[name] = [] 
            start = name
        elif ',' in line:
            name = " ".join(line.split(', ')[:: -1])
            person_to_friends[start].append(name)
            person_to_friends[start].sort()
        else:
            person_to_clubs[start].append(line)
            person_to_clubs[start].sort()
  
    remove_empty_keys(person_to_friends)
    remove_empty_keys(person_to_clubs)

    return (person_to_friends, person_to_clubs)
 

def get_average_club_count(person_to_clubs: Dict[str, List[str]]) -> float:
    """Return the average number of clubs that a person in person_to_clubs
    belongs to.

    >>> get_average_club_count(P2C)
    1.6
    >>> get_average_club_count(P2C2)
    2.0
    """
    if len(person_to_clubs) == 0:
        return float(0)
    else:
        total = 0
        for key in person_to_clubs:
            total = total + len(person_to_clubs[key])
        return total / len(person_to_clubs)


def get_last_to_first(
        person_to_friends: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Return a "last name to first name(s)" dictionary with the people from the
    "person to friends" dictionary person_to_friends.

    >>> get_last_to_first(P2F) == {
    ...    'Katsopolis': ['Jesse'],
    ...    'Tanner': ['Danny R', 'Michelle', 'Stephanie J'],
    ...    'Gladstone': ['Joey'],
    ...    'Donaldson-Katsopolis': ['Rebecca'],
    ...    'Gibbler': ['Kimmy'],
    ...    'Tanner-Fuller': ['DJ']}
    True
    >>> get_last_to_first(P2F2) == {'Wang': ['Kat', 'Kevin'], 
    ...    'Sun': ['Owen', 'Sunny'], 'Tang': ['Lily'], 
    ...    'Huang': ['Tom'], 'Li': ['Leo'], 
    ...    'Chen': ['Leo'], 'Ji': ['Eva'], 
    ...    'Wu': ['Gillian'], 'Fu': ['Andy']}
    True
    """
    name = []
    for key in person_to_friends:
        if key not in name:
            name.append(key)
        for s in person_to_friends[key]:
            if s not in name:
                name.append(s)
    last_name = {}
    for item in name:
        index_of_last = item.rfind(' ')
        first = item[0:index_of_last]
        last = item[index_of_last + 1 :]
        if last not in last_name:
            last_name[last] = [first]
        else:
            last_name[last].append(str(first).strip(','))
    for key in last_name:
        last_name[key].sort()
        
    return last_name


def invert_and_sort(key_to_value: Dict[object, object]) -> Dict[object, list]:
    """Return key_to_value inverted so that each key is a value (for
    non-list values) or an item from an iterable value, and each value
    is a list of the corresponding keys from key_to_value.  The value
    lists in the returned dict are sorted.

    >>> invert_and_sort(P2C) == {
    ...  'Comet Club': ['Michelle Tanner'],
    ...  'Parent Council': ['Danny R Tanner', 'Jesse Katsopolis',
    ...                     'Joey Gladstone'],
    ...  'Rock N Rollers': ['Jesse Katsopolis', 'Kimmy Gibbler'],
    ...  'Comics R Us': ['Joey Gladstone'],
    ...  'Smash Club': ['Kimmy Gibbler']}
    True
    >>> invert_and_sort(P2C2) == {'Parent Council': ['Kat Wang'], 
    ...  'Rock N Rollers': ['Kat Wang', 'Leo Li'], 
    ...  'Comet Club': ['Owen Sun'],'Art and Science': ['Leo Li'], 
    ...  'Smash Club': ['Leo Li']}
    True
    """
    value = []
    for key in key_to_value:
        for item in key_to_value[key]:
            value.append(item) 
    invert = {}
    for item in value:
        invert[item] = []
        for key in key_to_value:
            if item in key_to_value[key]:
                invert[item].append(key)
    for key in invert:
        invert[key].sort()
                
    return invert


def get_clubs_of_friends(person_to_friends: Dict[str, List[str]],
                         person_to_clubs: Dict[str, List[str]],
                         person: str) -> List[str]:
    """Return a list, sorted in alphabetical order, of the clubs in
    person_to_clubs that person's friends from person_to_friends
    belong to, excluding the clubs that person belongs to.  Each club
    appears in the returned list once per each of the person's friends
    who belong to it.

    >>> get_clubs_of_friends(P2F, P2C, 'Danny R Tanner')
    ['Comics R Us', 'Rock N Rollers']
    >>> get_clubs_of_friends(P2F2, P2C2, 'Owen Sun')
    ['Art and Science', 'Rock N Rollers', 'Smash Club']
    """
    if person not in person_to_friends:
        return []
    if person in person_to_friends:
        if person in person_to_clubs:
            own_friends = person_to_friends[person]
            own_club = person_to_clubs[person]
        else:
            own_friends = person_to_friends[person]
            own_club = []
        
    club_of_friends = []
    for friend in own_friends:
        if friend in person_to_clubs:
            for club in person_to_clubs[friend]:
                if club not in own_club:
                    club_of_friends.append(club)
    club_of_friends.sort()            
    return club_of_friends


def find_classmates(person: str, person_to_friends: Dict[str, List[str]],
                    person_to_clubs: Dict[str, List[str]],) ->  List[str]:
    """Return a list of person's classmate in the same club based on the
    "person to friends" dictionary.
    
    >>> find_classmates('Jesse Katsopolis',P2F, P2C)
    ['Danny R Tanner', 'Joey Gladstone', 'Kimmy Gibbler']
    >>> find_classmates('Leo Li', P2F2, P2C2)
    ['Kat Wang']
    """
    classmate = []
    reverse_club = invert_and_sort(person_to_clubs)
    if person in person_to_friends:
        if person in person_to_clubs:
            own_club = person_to_clubs[person]
        else:
            own_club = [] 
    if person not in person_to_friends:
        if person in person_to_clubs:
            own_club = person_to_clubs[person]
    for club in reverse_club:
        if club in own_club:
            for people in reverse_club[club]:
                if people not in person:
                    classmate.append(people) 
    return classmate


def insert_tuple(a_tuple: tuple, los: List[tuple]) -> None:
    """Return a list of tuple by inserting each tuple with order.
    >>> insert_tuple(('a',4), [])
    [('a',4)]
    >>> insert_tuple(('b',5), [('a',4)])
    [(b,5), (a,4)]
    """
    if los == []:
        los.append(a_tuple)
        return 
    else:
        for i in range(len(los)):
            if a_tuple[1] > los[i][1] or \
               (a_tuple[1] == los[i][1] and a_tuple[0] < los[i][0]):
                los.insert(i, a_tuple) 
                return 
        los.insert(len(los), a_tuple)


def recommend_clubs(
        person_to_friends: Dict[str, List[str]],
        person_to_clubs: Dict[str, List[str]],
        person: str,) -> List[Tuple[str, int]]:
    """Return a list of club recommendations for person based on the
    "person to friends" dictionary person_to_friends and the "person
    to clubs" dictionary person_to_clubs using the specified
    recommendation system.

    >>> recommend_clubs(P2F, P2C, 'Stephanie J Tanner',)
    [('Comet Club', 1), ('Rock N Rollers', 1), ('Smash Club', 1)]
    >>> recommend_clubs(P2F2, P2C2, 'Owen Sun',)
    [('Art and Science', 1), ('Rock N Rollers', 1), ('Smash Club', 1)]
    """
    if person not in person_to_friends:
        if person not in person_to_clubs:
            return []
        else:
            own_friends = []
            own_club = person_to_clubs[person]

    if person in person_to_friends:
        if person in person_to_clubs:
            own_friends = person_to_friends[person]
            own_club = person_to_clubs[person]
        else:
            own_friends = person_to_friends[person]
            own_club = []            
    suggest_club = {}
    for friend in own_friends:
        if friend in person_to_clubs:
            for club in person_to_clubs[friend]:
                if club not in own_club:
                    if club not in suggest_club:
                        suggest_club[club] = 1
                    else:
                        suggest_club[club] += 1
    
    classmates = find_classmates(person, person_to_friends, person_to_clubs)
    for people in classmates:
        for club in person_to_clubs[people]:
            if club not in own_club:
                if club not in suggest_club:
                    suggest_club[club] = 1
                else:
                    suggest_club[club] += 1
    
    suggestion = []
    for k in suggest_club:
        suggestion.append((k, suggest_club[k]))
   
    suggest_list = []
    for item in suggestion:
        insert_tuple(item, suggest_list)
    
    return suggest_list
     
            

            
if __name__ == '__main__':
    pass
    # If you add any function calls for testing, put them here.
        # Make sure they are indented, so they are within the if statement body.
        # That includes all calls on print, open, and doctest.
    
        # import doctest
        # doctest.testmod()