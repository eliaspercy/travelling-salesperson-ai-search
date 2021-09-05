############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random
import heapq
from math import inf
from collections import namedtuple

############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r')
    current_char = the_file.read(1)
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string


def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string


def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int


def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers


def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix


def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}
    tariff_dictionary = {}
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)
    location = 0
    EOF = False
    list_of_items = []
    while EOF == False:
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items) / 3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag


############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile012.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"

if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print(
        "*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1)) / 2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1)) / 2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "cmcz82"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Elias"
my_last_name = "Percy"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "AC"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = "This is a standard implementation of the Ant System version of the ACO algorithm, primarily adapted " \
             "from Dorigo & Stutzle 2004."

############
############ NOW YOUR CODE SHOULD BEGIN.
############

"""
    best tours found:
    - 12: 56
    - 17: 1444
    - 21: 2549
    - 26: 1622
    - 42: 1404
    - 48: 12709
    - 58: 25704
    - 175 21915
    - 180: 4600
    - 535: 53356
"""

# -------------------------------------------------- PARAMETERS ------------------------------------------------------ #

"""
NUM_ITERATIONS: Indicates the number of iterations that the algorithm will go through
TIME_LIMIT: The time limit of the algorithm
alpha: Determines the relative influence of the pheromone trail
beta: Determines the relative influence of the heuristic information
rho: The decay constant
num_ants: Indicates how many ants will exist during the algorithm
"""

NUM_ITERATIONS = 1000000
TIME_LIMIT = 50
alpha = 1
beta = 3
rho = 0.1
num_ants = 200

# -------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------------- THE ANT -------------------------------------------------------- #

Ant = namedtuple('Ant', 'tour_length tour')


class ActiveAnt:
    def __init__(self) -> None:
        self.tour_length = 0                            # The ant's tour length
        self.tour = [-1 for _ in range(num_cities+1)]   # The ant's memory, storing (partial) tours
        self.visited = set()                            # Set of visited cities


# -------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------- INITIALISE DATA ----------------------------------------------------- #


def nearest_neighbour_component(city: int, visited: set) -> int:
    """
    :param city: A given city
    :param visited: Set of cities so far visited by the nearest neighbour algorithm
    :return: The nearest unvisited neighbour
    """
    v = inf
    nc = False
    for neighbour in range(0,num_cities):
        if neighbour not in visited and neighbour != city:
            if dist_matrix[city][neighbour] <= v:  # Some city sets contain distances of zero, so >=
                nc = neighbour
                v = dist_matrix[city][neighbour]
    if nc is not False:
        return nc


def nearest_neighbour() -> float:
    """
    :return: The number of ants divided by the length of a tour found via the simple nearest neighbour algorithm \
             (for use as the initial pheromone value)
    """
    visited = set()
    visited.add(0)
    current_city = 0
    cost = 0
    for iteration in range(0,num_cities-1):
        next_city = nearest_neighbour_component(current_city, visited)
        cost += dist_matrix[current_city][next_city]
        visited.add(next_city)
        current_city = next_city
    return num_ants/(cost + dist_matrix[current_city][0])


def heuristic_function(i: int, j: int) -> float:  # Heuristic value, obtained a priori
    """
    :param i: A city, i
    :param j: A neighbouring city to city i, city j
    :return: Inverse of the distance between cities i and j
    """
    if i == j:
        return 0
    try:
        return 1.0 / dist_matrix[i][j]
    except ZeroDivisionError:
        return 2.0


def compute_choice_info(pheromone: list) -> list:
    """
    :param pheromone: Pheromone matrix
    :return: computed choice index
    """
    choice_index = [[None for _ in range(num_cities)] for _ in range(num_cities)]
    for i in range(0,num_cities):
        for j in range(i, num_cities):
            choice_index[i][j] = (pheromone[i][j] ** alpha) * (heuristic_function(i, j) ** beta)

            # Check for symmetry
            if dist_matrix[i][j] == dist_matrix[j][i]: choice_index[j][i] = choice_index[i][j]
            else: choice_index[j][i] = (pheromone[j][i] ** alpha) * (heuristic_function(j, i) ** beta)
    return choice_index


def initialise_data() -> (list, list, list):

    # Pheromone: Matrix consisting of the pheromone value at each city
    pheromone_initial = nearest_neighbour()
    pheromone = [[pheromone_initial for _ in range(num_cities)] for _ in range(num_cities)]

    # choice_info: Combined pheromone and heuristic information in the form of a matrix
    choice_info = compute_choice_info(pheromone)

    # ants: List of all currently living ants
    ants = [ActiveAnt() for _ in range(num_ants)]

    return pheromone, choice_info, ants


# -------------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------- CONSTRUCT SOLUTIONS ------------------------------------------------ #

def choose_best_next(ant: ActiveAnt, i: int, choice_info: list) -> None:
    """
    :param choice_info: Choice info matrix
    :param ant: Ant identifier
    :param i: Counter for construction step
    """
    nc = False
    v = 0.0
    c = ant.tour[i-1]
    for j in range(0,num_cities):
        if j not in ant.visited and j != c:
            if choice_info[c][j] >= v:   # MUST be >= because at some point, after enough iterations, all == 0
                nc = j                  # City with maximal pheromone^alpha * heuristic*beta value
                v = choice_info[c][j]
    if nc is not False:                 # Ensures nc is found (won't be the case if all cities had been visited already)
        ant.tour_length += dist_matrix[c][nc]
        ant.tour[i] = nc
        ant.visited.add(nc)
    else:
        print("Error")  # better to return uber_ant
        sys.exit(1)


def decision_rule(ant: ActiveAnt, i: int, choice_info: list) -> None:
    """
    :param choice_info: Choice info matrix
    :param ant: ant identifier
    :param i: counter for construction step
    """
    c = ant.tour[i-1]
    sum_probabilities = 0.0
    selection_probability = []
    for j in range(0,num_cities):                           # 1. Sum up the weight of the various choices and store in var sum_probabilities
        if j in ant.visited:
            selection_probability.append(0)
        else:
            selection_probability.append(choice_info[c][j])
            sum_probabilities += selection_probability[j]
    loop = True  # Safety net - in case something goes wrong and an already visited city is selected, then retry
    while loop:
        r = random.uniform(0, sum_probabilities)  # 2. Draw a uniformly distributed random number r from given interval
        j = 0
        p = selection_probability[j]
        while p < r:  # 3. Go through the feasible choices until the sum is greater than or equal to r
            j += 1
            p += selection_probability[j]
        if j not in ant.visited:
            loop = False
            ant.tour_length += dist_matrix[c][j]
            ant.tour[i] = j
            ant.visited.add(j)
        else:
            # print("\n\n\nthis happened\n\n\n")  # debug
            pass

    if sum_probabilities == 0.0:                    # 2a. In cases where all nn nearest cities have been visited already
        choose_best_next(ant, i, choice_info)


def construct_solutions(ants: list, choice_info: list) -> (list, list):
    """
    :param ants: List of active ants
    :param choice_info: Choice info matrix
    :return: The list of ants in their new state, the tours of each ant
    """
    tours = []
    for ant in ants:                     # 1. Empty the ants' memories
        ant.tour_length = 0
        ant.visited.clear()
    step = 0
    for ant in ants:                     # 2. Assign a random initial city to each ant
        r = random.randint(0,num_cities-1)
        ant.tour[step] = r
        ant.visited.add(r)
    while step < num_cities-1:           # 3. Construct a complete tour for each ant
        step += 1
        for ant in ants:                 # 3.1. At each construction step, find edge according to rule
            decision_rule(ant, step, choice_info)
    step = 0
    for ant in ants:                     # 4. Move each ant back to the initial city
        nc = ant.tour[0]
        ant.tour_length += dist_matrix[ant.tour[num_cities-1]][nc]
        ant.tour[num_cities] = nc
        heapq.heappush(tours, Ant(ant.tour_length, ant.tour[:]))
        step += 1
    return ants, tours

# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------- UPDATE STATISTICS ------------------------------------------------------ #

def update_statistics(tours: list) -> tuple:    # defo should store the tours as they're made
    """
    :return: A tuple containing the best tour found this round beside its length
    """
    return tours[0]

# -------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------- PHEROMONE UPDATE ----------------------------------------------------- #

def evaporate(pheromone: list) -> list:
    """
    Decrease the value of the pheromone trails on all the arcs (i,j) by a constant factor, rho
    """
    for i in range(0,num_cities):
        for j in range(i,num_cities):
            pheromone[i][j] *= (1 - rho)
            pheromone[j][i] *= (1 - rho)    # Pheromones aren't assumed to be symmetric
    return pheromone


def deposit_pheromone(ant: ActiveAnt, pheromone: list) -> list:  # Add pheromone to arcs belonging to tours constructed by the ants
    """
    Add pheromone to arcs belonging to tours constructed by the ants
    """
    tao_change = 1/ant.tour_length
    for i in range(0,num_cities):
        j = ant.tour[i]
        l = ant.tour[i+1]
        pheromone[j][l] += tao_change
        if dist_matrix[j][l] == dist_matrix[l][j]: pheromone[l][j] = pheromone[j][l]    # Do only if symmetric
    return pheromone


def pheromone_update(ants: list, pheromone: list) -> (list, list):
    pheromone = evaporate(pheromone)
    for ant in ants:
        pheromone = deposit_pheromone(ant, pheromone)
    choice_info = compute_choice_info(pheromone)   # compute the choice info matrix to be used in the next iteration
    return pheromone, choice_info

# -------------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------- THE ALGORITHM ------------------------------------------------------ #

def aco(num_iterations: int, time_limit: float) -> tuple:
    """
    :param time_limit:
    :param num_iterations: Indicates the number of iterations that the algorithm will go through
    :return: The best tour the algorithm finds, alongside its length
    """
    start = time.time()
    uber_ant = Ant(inf, inf)
    pheromone, choice_info, ants = initialise_data()
    for i in range(num_iterations):
        if (time.time() - start > time_limit):
            break
        ants, tours = construct_solutions(ants, choice_info)
        uber_ant = min(uber_ant, update_statistics(tours))
        pheromone, choice_info = pheromone_update(ants, pheromone)
        # print(i, uber_ant.tour_length)
    # print(f"Time taken: {time.time() - start}")
    return uber_ant

# -------------------------------------------------------------------------------------------------------------------- #


tour_length, tour_full = aco(NUM_ITERATIONS, TIME_LIMIT)
tour = tour_full[:num_cities]






############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour',
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(
        len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(
        check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[
                                                               0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name, 'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1, num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")







