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

added_note = "Enhanced implementation of ACO with nearest neighbour lists, ranks, enforced diversity via mutation, " \
             "stagnation detection (which leads to 2-opt local search and pheromone trail smoothing) and various " \
             "nuanced additions (see comments in code)."

############
############ NOW YOUR CODE SHOULD BEGIN.
############


"""
Ranks - Each ant deposits an amount of pheromone that decreases with its "rank"
- Ranks are given according to tour lengths (i.e. the greater the tour length, the smaller the rank)
- Only the best w (6) ants in a given iteration, and the uber_ant, deposit pheromone
- Alg. updates: tours replaced with sorted_ants, which contains a list of ant objects sorted by tour_length rather than
    a tuple (this alone had no apparent affect on time complexity, as tour_lengths were sorted all the same).

    best tours so far: 
    defaults: a = 1, beta = 2, rho = 0.1    (* = assumed to be optimal)
    - 12: 56 *
    - 17: 1444 *
    - 21: 2549 * - reached almost immediately and NEVER improves on it, so likely the best tour (considering small no cities)
    - 26: 1475, 1476 (mutation and 2-opt, 55s), 1483, (mutation and 2-opt), 1600, 1609
    - 42: 1196 (mutation, 2-opt, beta=2), 1201, (b=3), 1221, 1240 (mutation, 2-opt), 1277, 1274 (beta=10), 1293, 1301 (20000 its - beta=5; only nn)
    - 48: 12150 (all, 6 hrs, 214224 iterations, 250 ants), 12150 (with mutation and 2-opt), 12166 (with mutation), 12168 (mutation, 2-opt), 12175, 12177 (with mutation), 12195 (all enhances, 200 ants, 25 secs), 12213, 12218
    - 58: 25395, 25395 (same but 1hr), 25395 (mutation and 2-opt, found quickest), 25395 (with mutation), 25395 (with mutation, beta=3) 25405 (with mutation), 25564, 25404
        -observations: 25395 is the best i've found, definitely comes down to rank putting onto right direction but mainly
            mutation and 2_opt to break out of stagnation (usually stagnates for a while around 25650--)
    - 175: 21424 (all enhancements, 1hr), 21464 (2925 its, 600s, 50 ants), 21493 (mutation, beta=5), 21545 (two-opt and mutation), 21742 (mutation, 409 its), 21565 in 55s with 500 ants
    - 180: 1950 * (mutation, 2-opt) | PRIOR TO FIXING HEURISTIC: 4470 (mutation, beta=5), 4480 (with mutation), 4580
    - 535: 48652 (ran overnight), 48779, 48816, 48998 (beta=10, alpha=2, 55s, 49168 (beta=5, rho=0.5), 49394 (beta=15), 49657 (beta=10, mut, 2-opt), 50892 (55s, beta=5), 51778 (1hr, beta=2), 52872 (55s, mutation)
    
    
    ##### BEST TOURS, AND CORRESPONDING PARAMETERS + NUM ITERATIONS #####
    
    - 12: 56; pretty much any parameters will do, always finds almost immediately
    - 17: 1444; same as above - finds almost instantly and never improves
    - 21: 2549; with alpha=1 and beta=2, same as above - finds almost instantly and never improves
    - 26: 1475; alpha=1, beta=2, rho=0.2, num_ants=50: typically stagnates between 1500 and 1510 for a few thousand 
                iterations, before jumping out and then stagnating at 1483 for very long. Usually gets or 1475 to 1476
                after about 10000 iterations (with the aforementioned parameters)
    - 42: 1196; alpha=1, beta=3, rho=0.2, num_ants=250: typically stagnates between 1210 and 1230 for several hundred 
                iterations after 200 iterations. By 1000 iterations it drops below 1210 (often with the help of 2-opt or 
                mutation), and after about 1000 more it will jump down to 1196
    - 48: 12150; alpha = 1, beta = 2, rho = 0.1, num_ants = 50; found between 6100 and 6200 iterations. Didn't improve
                 after several 10s of thousands of iterations.
    - 58: 25395; alpha=2, beta=1, rho=0.2, num_ants=250; strangely, the colony stagnates on 2643 for a very very long 
                 time with beta values higher than 1, but with the parameters mention here, the algorithm finds a tour
                 of 25395 very quickly (what often happens is it finds a tour of 25538 in about 200 iterations, 
                 stagnates on that for a while before 2-opting the tour of 25538, reducing it to 25395). It never 
                 improves in 25395 after very many iterations.          
    - 175: 21424; alpha=1, beta=5, rho=0.2, num_ants=250; A usual situation would be the algorithm finds a tour of about
                  21450 in roughly 300 iterations, and gradually decreases the tour from then on over the course of
                  about a thousand iterations (generally stagnates on 21433 before jumping down to 21424, or something
                  close to that)  
    - 180: 1950; alpha=1, beta=5, rho=0.2, num_ants=250; with these parameters, 1950 is found quite quickly (always 
                 within 100 iterations), and it's generally found quickly with other parameters too. It also didn't 
                 require 2-opt to reach, but the other enhancements, particularly rank and mutation, helped reach this.
                 After running for several 10s of thousands more iterations, it never improves on 1950.
    - 535: 48652; alpha = 1, beta = 13, rho = 0.1, num_ants = 250; found after 2-opt was applied to a tour of 48653, 
                  which was found after approximately 1800 iterations. For this city in particular, setting beta to a 
                  relatively high value significantly improves the rate at which good tours are found, and also appears
                  to improve the best tour found (I never observed it get close to 48652 with any beta lower than 5).
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
alpha = 1   # with some exceptions, higher alpha, lower beta is better for smaller city sets - and vice versa
beta = 3
rho = 0.1
num_ants = 200

# -------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------------- THE ANT -------------------------------------------------------- #

Ant = namedtuple('Ant', 'tour_length tour')


class ActiveAnt:
    def __init__(self, tour_length: float = 0) -> None:
        self.tour_length = tour_length  # The ant's tour length
        self.tour = [-1 for _ in range(num_cities)]  # The ant's memory, storing (partial) tours
        self.visited = set()  # Set of cities indicating if visited


# -------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------- INITIALISE DATA ----------------------------------------------------- #

def nearest_neighbours_list(i: int, nn: int) -> list:
    """
    :param i: A city, i
    :param nn: A (small) integer - the nearest neighbour range
    :return: A list of the nn nearest neighbours to city i in nondecreasing order
    """
    neighbours = [j for j in range(num_cities) if j != i]
    distances = [dist_matrix[i][j] for j in range(num_cities) if j != i]
    nearest = [city for _, city in sorted(zip(distances, neighbours))]
    return nearest[:nn]


def nearest_neighbour_component(city: int, visited: set, nn_list: list) -> int:
    """
    :param city: A given city
    :param visited: Set of cities so far visited by the nearest neighbour algorithm
    :return: The nearest unvisited neighbour
    """
    for neighbour in nn_list[city]:
        if neighbour not in visited:
            return neighbour

    # If nearest unvisited city not in nn_list, have to go thru entire thing!
    v = inf
    nc = False
    for neighbour in range(0, num_cities):
        if neighbour not in visited:
            if dist_matrix[city][neighbour] <= v:  # Some city sets contain distances of zero, so >=
                nc = neighbour
                v = dist_matrix[city][neighbour]
    if nc is not False:
        return nc


def nearest_neighbour(w: int, nn_list: list) -> float:  # For obtaining the initial pheromone value
    """
    :return: The calculated initial pheromone value
    """
    visited = set()
    visited.add(0)
    current_city = 0
    cost = 0
    for iteration in range(0, num_cities - 1):
        next_city = nearest_neighbour_component(current_city, visited, nn_list)
        cost += dist_matrix[current_city][next_city]
        visited.add(next_city)
        current_city = next_city
    return (0.5 * w * (w - 1)) / (rho * cost)


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


def compute_choice_info(pheromone: list, choice_info: list) -> list:
    """
    :return: computed choice index
    """
    for i in range(0, num_cities):
        for j in range(i, num_cities):
            choice_info[i][j] = (pheromone[i][j] ** alpha) * (heuristic_function(i, j) ** beta)

            # Check for symmetry
            if dist_matrix[i][j] == dist_matrix[j][i]: choice_info[j][i] = choice_info[i][j]
            else: choice_info[j][i] = (pheromone[j][i] ** alpha) * (heuristic_function(j, i) ** beta)
    return choice_info


def initialise_data(w: int, nn: int) -> (list, list, list, list):
    """
    :param w: Rank parameter
    :param nn: Nearest neighbour list range
    :return:
    """

    # nn_list (CONST): Matrix with nearest neighbour lists of depth nn
    nn_list = [nearest_neighbours_list(i, nn) for i in range(0, num_cities)]

    # Pheromone: Matrix consisting of the pheromone value at each city
    initial_pheromone = nearest_neighbour(w, nn_list)
    pheromone = [[initial_pheromone for _ in range(num_cities)] for _ in range(num_cities)]

    # choice_info: Combined pheromone and heuristic information in the form of a matrix
    choice_info = [[None for _ in range(num_cities)] for _ in range(num_cities)]
    choice_info = compute_choice_info(pheromone, choice_info)

    # ants: List of all currently living ants
    ants = [ActiveAnt() for _ in range(num_ants)]

    return initial_pheromone, pheromone, choice_info, ants, nn_list


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
    c = ant.tour[i - 1]
    for j in range(0, num_cities):
        if j not in ant.visited and j != c:
            if choice_info[c][j] >= v:
                nc = j  # City with maximal pheromone^alpha * heuristic*beta value
                v = choice_info[c][j]
    if nc is not False and nc != c:  # Ensures nc is found (won't be the case if all cities had been visited already)
        ant.tour_length += dist_matrix[c][nc]
        ant.tour[i] = nc
        ant.visited.add(nc)
    else:
        print("Error")  # edit so that it returns uber ant in the case of failure
        sys.exit(1)


# analogous to the roulette wheel selection procedure
def neighbour_list_decision_rule(ant: ActiveAnt, i: int, choice_info: list, nn: int, nn_list: list) -> None:
    """
    :param choice_info: Choice info matrix
    :param ant: ant identifier
    :param i: counter for construction step
    """
    c = ant.tour[i - 1]
    sum_probabilities = 0.0
    selection_probability = []
    for j in range(0, nn):  # 1. Sum up the weight of the various choices and store in var sum_probabilities
        if nn_list[c][j] in ant.visited:
            selection_probability.append(0)
        else:
            selection_probability.append(choice_info[c][nn_list[c][j]])
            sum_probabilities += selection_probability[j]
    if sum_probabilities == 0.0:  # 2a. Handle cases where all nn nearest cities have been visited already
        choose_best_next(ant, i, choice_info)
    else:
        loop = True  # Safety net - in case something goes wrong and an already visited city is selected, then retry
        while loop:
            r = random.uniform(0, sum_probabilities)  # 2b. Draw a uniformly distributed random number r from given interval
            j = 0
            p = selection_probability[j]
            while p < r:  # 3. Go through the feasible choices until the sum is greater than or equal to r
                j += 1
                p += selection_probability[j]
            nc = nn_list[c][j]
            if nc not in ant.visited:
                loop = False
                ant.tour_length += dist_matrix[c][nc]
                ant.tour[i] = nc
                ant.visited.add(nc)
            else:
                # print("\n\n\nthis happened\n\n\n")  # debug
                pass


def construct_solutions(ants: list, choice_info: list, nn: int, nn_list: list) -> (list, list):
    """
    :param ants: List of active ants
    :param choice_info: Choice info matrix
    :return: The list of ants in their new state, the tours of each ant
    """
    ant_heap = []
    for ant in ants:  # 1. Empty the ants' memories
        ant.tour_length = 0
        ant.visited.clear()
    step = 0
    for ant in ants:  # 2. Assign a random initial city to each ant
        r = random.randint(0, num_cities - 1)
        ant.tour[step] = r
        ant.visited.add(r)
    while step < num_cities - 1:  # 3. Construct a complete tour for each ant
        step += 1
        for ant in ants:  # 3.1. At each construction step, find edge according to rule
            neighbour_list_decision_rule(ant, step, choice_info, nn, nn_list)
    for ant in ants:  # 4. Move each ant back to the initial city
        nc = ant.tour[0]
        ant.tour_length += dist_matrix[ant.tour[num_cities - 1]][nc]
        heapq.heappush(ant_heap, Ant(ant.tour_length, ant.tour[:]))
    return ants, ant_heap


# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------- UPDATE STATISTICS ------------------------------------------------------ #

def update_statistics(sorted_ants: list) -> Ant:
    """
    :return: A tuple containing the best tour found this round beside its length
    """
    return sorted_ants[0]


# -------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------- PHEROMONE UPDATE ----------------------------------------------------- #

def evaporate(pheromone: list) -> list:
    """
    Decrease the value of the pheromone trails on all the arcs (i,j) by a constant factor, rho
    """
    for i in range(0, num_cities):
        for j in range(i, num_cities):
            pheromone[i][j] *= (1 - rho)
            pheromone[j][i] *= (1 - rho)    # Pheromones aren't assumed to be symmetric
    return pheromone


def deposit_pheromone(ant: Ant, pheromone: list, uber_ant: Ant, e: float, rank: int) -> list:
    """
    Add pheromone to arcs belonging to tours constructed by the ants
    :param ant: Ant identifier
    :param pheromone: Pheromone matrix
    :param uber_ant: The best-so-far ant, represented as a tuple containing its tour length and corresponding tour; used for the elitism enhancement
    :param e: Elitism parameter
    :param rank: Rank of the ant
    """
    tao_change = 1.0 / ant.tour_length
    elite_addition = e / uber_ant.tour_length
    for i in range(0, num_cities):
        j = ant.tour[i - 1]
        l = ant.tour[i]
        pheromone[j][l] += rank * tao_change + elite_addition
        if dist_matrix[j][l] == dist_matrix[l][j]: pheromone[l][j] = pheromone[j][l]    # Do only if symmetric
    return pheromone


def pheromone_update(ants: list, pheromone: list, choice_info: list, uber_ant: Ant, e: float) -> (list, list):
    """
    :param ants: List of active ants
    :param pheromone: Pheromone matrix
    :param uber_ant: The best-so-far ant, represented as a tuple containing its tour length and corresponding tour; used for the elitism enhancement
    :param e: Elitism parameter (equals the number of cities)
    :return:
    """
    pheromone = evaporate(pheromone)
    rank = len(ants)
    pheromone = deposit_pheromone(uber_ant, pheromone, uber_ant, 0, rank)
    for ant in ants:
        pheromone = deposit_pheromone(ant, pheromone, uber_ant, e, rank)
        rank -= 1  # iter best and uber have the same rank, elitism for iter best only
        e = 0
    choice_info = compute_choice_info(pheromone, choice_info)
    return pheromone, choice_info


# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------- ENHANCEMENTS ----------------------------------------------------- #

def find_tour_cost(tour: list) -> int:
    cost = 0
    for i in range(0, num_cities):
        cost += dist_matrix[tour[i - 1]][tour[i]]
    return cost


def two_opt_swap(tour: list, i: int, k: int) -> list:
    new_tour = tour[:]
    new_tour[i:k] = new_tour[k - 1:i - 1:-1]
    return new_tour


# Optimise the local minimum
def two_opt(ant_heap: list) -> Ant:
    # print("breaking free")
    best_ant = Ant(ant_heap[0].tour_length, ant_heap[0].tour)
    best_length = best_ant.tour_length
    # print(f"start: {best_length}")
    for ant in ant_heap:
        for i in range(1, num_cities - 2):
            for k in range(i + 2, num_cities - 1):
                new_tour = two_opt_swap(ant.tour, i, k)
                new_length = find_tour_cost(new_tour)
                if new_length < best_length:
                    best_ant = Ant(new_length, new_tour)
                    best_length = best_ant.tour_length
    # print(f"end: {best_ant.tour_length}")
    return best_ant


def mutate(ant: Ant) -> Ant:
    tour = ant.tour
    a, b = random.randint(0, num_cities - 1), random.randint(0, num_cities - 1)
    tour[a], tour[b] = tour[b], tour[a]
    cost = find_tour_cost(tour)
    return Ant(cost, tour)


def mutation(ant_heap: list, mutation_rate: float):
    for i in range(len(ant_heap)):
        if i == 0:  # do not mutate the best ant
            pass
        else:
            r = random.uniform(0, 1)
            if r <= mutation_rate:
                mutated = mutate(ant_heap.pop(i))
                heapq.heappush(ant_heap, mutated)
    return ant_heap


# Calculate the diversity of the colony, and enforce diversity if it's too low
def diversity_calculator(ant_heap):
    # The diversity between the fitness of the ants in the population is measured by calculating the Euclidean Distance
    num = ant_heap[len(ant_heap) // 2].tour_length - ant_heap[0].tour_length
    den = ant_heap[-1].tour_length - ant_heap[0].tour_length
    try:
        ed = num / den
    except ZeroDivisionError:
        ed = 1
    # If ED is high, most of the ants are not biased towards the current best ant. Therefore, ED gives a description \
    # for the population variation and the lack of similarity between ants.
    return True if ed > 0.6 else False


# Reinitialise the pheromone matrix upon
def pheromone_trail_smoothing(pheromone: list, pts: float, initial_pheromone: float):  # ENHANCEMENT
    # print("reinit")
    for i in range(0, num_cities):
        for j in range(i, num_cities):
            pheromone[i][j] += pts * (initial_pheromone - pheromone[i][j])
            pheromone[j][i] += pts * (initial_pheromone - pheromone[j][i])
    return pheromone


# Detect and combat stagnations (also updates the uber ant if necessary)
def stagnation_detection(ib_ant: Ant, uber_ant: Ant, stagnation_detector: Ant,
                         stagnation_var: int, stagnation_limit: int) -> (Ant, Ant, int, bool):
    stagnated = False
    if ib_ant < uber_ant:
        stagnation_detector = Ant(ib_ant.tour_length, ib_ant.tour[:])
        uber_ant = Ant(ib_ant.tour_length, ib_ant.tour[:])
        stagnation_var = 0
    elif ib_ant < stagnation_detector:
        stagnation_detector = Ant(ib_ant.tour_length, ib_ant.tour[:])
        stagnation_var = 0
    else:
        stagnation_var += 1
        if stagnation_var == stagnation_limit//2:  # if stagnation is halfway reached, 2-opt just the current uber_ant
            # print("half")
            opt_ant = two_opt([uber_ant])
            if opt_ant.tour_length < uber_ant.tour_length:
                uber_ant = Ant(opt_ant.tour_length, opt_ant.tour[:])
                stagnation_detector = Ant(opt_ant.tour_length, opt_ant.tour[:])
        if stagnation_var > stagnation_limit:
            stagnation_var = 0
            stagnation_detector = Ant(inf, [])
            stagnated = True
    return uber_ant, stagnation_detector, stagnation_var, stagnated


# Implemented when I was constructing max-min; decided to keep since it can be used in other ways
def ant_deposit_selector(iter: int) -> bool:
    if iter <= 25:
        return True
    elif 25 < iter <= 75:
        return False if iter % 5 == 0 else True
    elif 75 < iter <= 125:
        return False if iter % 3 == 0 else True
    elif 125 < iter <= 250:
        return False if iter % 2 == 0 else True
    else:
        return False


# -------------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------- THE ALGORITHM ------------------------------------------------------ #


def aco(num_iterations: int, time_limit: float) -> tuple:
    """
    :param time_limit: Maximum time the algorithm can run for
    :param num_iterations: Indicates the maximum number of iterations that the algorithm can run through
    :return: The best tour the algorithm finds, alongside its length
    """
    iteration = 0
    start = time.time()
    e = 0  # num_cities  # Elitism parameter
    nn = min(15, num_cities - 1)
    w = 6  # No. of ants allowed to drop pheromone
    pts = 1  # pheromone smoothing parameter
    mutation_rate = 1
    uber_ant = Ant(inf, [])
    stagnation_detector = Ant(inf, [])
    stagnation_var = 0
    stagnation_limit = 150
    initial_pheromone, pheromone, choice_info, ants, nn_list = initialise_data(w, nn)
    for i in range(num_iterations):
        iteration += 1

        if (time.time() - start > time_limit):
            break
        ants, ant_heap = construct_solutions(ants, choice_info, nn, nn_list)

        # Check for diversity, then enforce diversity
        diverse = diversity_calculator(ant_heap)
        if not diverse:
            # print("mutation")
            ant_heap = mutation(ant_heap, mutation_rate)

        # get the iteration best ant
        ib_ant = update_statistics(ant_heap)

        # Find the overall-best ant (whose properties the uber_ant will inherit)
        uber_ant, stagnation_detector, \
        stagnation_var, stagnated = stagnation_detection(ib_ant, uber_ant, stagnation_detector,
                                                         stagnation_var, stagnation_limit)
        if stagnated:
            opt_ant = two_opt([uber_ant] + ant_heap[:w])
            if opt_ant.tour_length < uber_ant.tour_length:
                uber_ant = Ant(opt_ant.tour_length, opt_ant.tour[:])
            pheromone = pheromone_trail_smoothing(pheromone, pts, initial_pheromone)

        pheromone, choice_info = pheromone_update(ant_heap[:w], pheromone, choice_info, uber_ant, e)
        # if i % 100 == 0: print(i, uber_ant.tour_length, stagnation_detector.tour_length)
    # print(f"Time taken: {time.time() - start}; iterations: {iteration}")
    return uber_ant.tour_length, uber_ant.tour


# -------------------------------------------------------------------------------------------------------------------- #

tour_length, tour = aco(NUM_ITERATIONS, TIME_LIMIT)

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







