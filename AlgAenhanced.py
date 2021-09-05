############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import math
import os
import sys
import time
import random
from collections import namedtuple, deque
import heapq

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

input_file = "AISearchfile535.txt"

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

algorithm_code = "AS"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the algorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = "Enhanced version of the A* Search algorithm, using the nearest neighbour algorithm for heuristic, with " \
             "2-opt, solution pool, continuation and randomness as enhancements. Also incorporates a variant of " \
             "nearest neighbour to improve the tours stored in each node."

############
############ NOW YOUR CODE SHOULD BEGIN.
############

"""
Enhancements to basic implementation:
- Solutions pool:
    - Random mutation of nodes in solutions pool by given rate
    - 2-opt local search to attempt to optimise nodes before being placed in solutions pool
- Insertion nearest neighbour to improve tours generated within heuristic for selected nodes only
- Random selection of nodes to expand by given rate

        
Solutions found with all enhancements implemented, (all calculated within 50s; can significantly improve most with
longer runtimes):
    - 12: 56
    - 17: 1444
    - 21: 2549
    - 26: 1473
    - 42: 1216
    - 48: 12471
    - 58: 25912
    - 175: 21551
    - 180: 1950
    - 535: 49252
        
"""

# -------------------------------------------- PARAMETERS ------------------------------------------------------------ #

START_TIME = time.time()
TIME_LIMIT = 50


# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------- NODE OBJECT ------------------------------------------------------------ #

# Class for the node, including all attributes and method
class Node:
    def __init__(self, city: int or str, state: list, unvisited: list, path_cost: int or str) -> None:
        self.city = city  # The current city associated with the node
        self.state = state  # Ordered list of cities so far visited, including the current city
        self.unvisited = unvisited  # List of all cities currently unvisited
        self.g_value = path_cost  # Cumulative cost of path so far traversed, is equal to the g-score
        self.h_value = None  # The output of the heuristic function for the current node
        self.f_value = None  # The output of the f(z), where z is the current node
        self.nn = None  # Stored route for the completed nearest neighbour insertion, obtained during h(z)
        self.nn_in_solution_pool = False
        self.first_nn = None

    def __lt__(self, other) -> bool:  # For handling cases when the priority queue has two nodes with the same h_value
        return self.f_value < other.f_value

    def goal(self) -> bool:  # Checks if the node is a goal node - True if there are no more cities unvisited
        return not self.unvisited

    """
    Below is a Heuristic function using insertion nearest neighbour - good for smaller city sets, but too inefficient 
    for larger ones, so I used my basic heuristic instead, but still used insertion nearest neighbour to attempt to 
    improve the tours found by the basic nearest neighbour when a node is selected.
    """
    # def h(self) -> int:  # The holy heuristic function, h(z).
    #     if not self.unvisited:  # If there are no more remaining unvisited
    #         self.h_value = 0  # cities then it is implied that the current
    #         return 0  # state is a goal state, so 0 is returned.
    #     elif self.h_value is not None:
    #         return self.h_value  # Return the h_value if it's been already calculated.
    #
    #     # From here on, undertake an insertion variant of the nearest neighbour algorithm to attain the h_value, and
    #     # store the tour found via it
    #     current_state = deque([city for city in self.state])
    #     self.h_value, self.nn, self.first_nn = insertion(current_state)
    #
    #     return self.h_value

    def h(self) -> int:  # The holy heuristic function, h(z).
        if not self.unvisited:  # If there are no more remaining unvisited
            self.h_value = 0  # cities then it is implied that the current
            return 0  # state is a goal state, so 0 is returned.
        elif self.h_value is not None:
            return self.h_value  # Return the h_value if it's been already calculated.

        # From here on, the nearest neighbour algorithm is undertaken from the current city until a
        # goal node is reached, and the output of this is the heuristic value (h_value).
        current_unvisited = self.unvisited[:]
        current_state = self.state[:]
        current_city = self.city
        current_h_value = 0

        while current_unvisited:
            temp = current_unvisited[0]
            smallest_distance = dist_matrix[current_city][temp]
            for neighbour in current_unvisited:
                if dist_matrix[current_city][neighbour] < smallest_distance:
                    smallest_distance = dist_matrix[current_city][neighbour]
                    temp = neighbour
            current_h_value += smallest_distance
            current_city = temp
            current_state.append(current_city)
            current_unvisited.remove(current_city)

        self.nn = current_state  # The route found by the nearest neighbour completion from this node is stored
        self.h_value = current_h_value + dist_matrix[current_city][current_state[0]]
        return self.h_value

    def f(self) -> int:  # The sacred evaluation function, f(z) = h(z) + g(z).
        self.f_value = self.h() + self.g_value  # As the g_value is simply the path cost up until the current node,
        return self.f_value  # there is no need to make a distinct function for this.

# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------ ENHANCEMENTS ------------------------------------------------------ #


# A namedtuple representing a simplified form of the node class above, containing only the tour length and tour.
SimpleNode = namedtuple('SimpleNode', 'tour_length tour')


# Variant of basic nearest neighbour - I call the it meet-in-the-middle nearest neighbour
def insertion(state: deque) -> tuple:
    # print("iter")
    cost = 0
    first = None
    update_front, update_back = True, True
    while len(state) < num_cities:
        # Find the nearest neighbours of both the first and last city in the state
        if update_front:
            front = [(v, i) for i, v in enumerate(dist_matrix[state[-1]]) if i not in state]
            update_front = False
        if update_back:
            back = [(v, i) for i, v in enumerate(dist_matrix[state[0]]) if i not in state]
            update_back = False
        nearest_front = min(front)
        nearest_back = min(back)
        if nearest_front <= nearest_back:
            # Append to front, increase cost accordingly
            update_front = True
            state.append(nearest_front[1])
            cost += nearest_front[0]
            back.remove((dist_matrix[state[0]][nearest_front[1]], nearest_front[1]))
            if first is None: first = nearest_front[1]
        else:
            # Append to back, increase cost accordingly
            update_back = True
            state.appendleft(nearest_back[1])
            cost += nearest_back[0]
            front.remove((dist_matrix[state[-1]][nearest_back[1]], nearest_back[1]))
            if first is None: first = nearest_front[1]
    cost += dist_matrix[state[-1]][state[0]]
    return cost, list(state), first


def find_tour_cost(tour: list) -> int:
    cost = 0
    for i in range(0, num_cities):
        cost += dist_matrix[tour[i-1]][tour[i]]
    return cost


def two_opt_swap(tour: list, i: int, k: int) -> list:
    new_tour = tour[:]
    new_tour[i:k] = new_tour[k-1:i-1:-1]
    return new_tour


def two_opt(node: SimpleNode) -> SimpleNode:
    # print("breaking free")
    best_length = node.tour_length
    # print(node)
    # print(f"start: {best_length}")
    for i in range(1, num_cities-2):
        for k in range(i+2, num_cities-1):

            new_tour = two_opt_swap(node.tour, i, k)
            new_length = find_tour_cost(new_tour)
            if new_length < best_length:
                node = SimpleNode(new_length, new_tour)
                best_length = node.tour_length
    # print(f"end: {node.tour_length}")
    return node


def mutate(node: SimpleNode) -> SimpleNode:
    tour_length, tour = node.tour_length, node.tour[:]
    a, b = random.randint(0,num_cities), random.randint(0,num_cities)
    tour[a], tour[b] = tour[b], tour[a]
    tour_length = find_tour_cost(tour)
    return SimpleNode(tour_length, tour)


# -------------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------- THE ALGORITHM ------------------------------------------------------ #

def a_star_search() -> (list, int):

    # Safety net for large large numbers of iterations - prevents having too many nodes in memory
    capacity = 500000

    # Construct an a priori node; uses strings '-' for the current_city and path_cost as these don't exist yet.
    initial_node = Node('-', [], list(range(num_cities)), '-')

    # Frontier, now uses heapq, stores tuples of tour lengths and tours, with the smallest at the front.
    frontier = [(0, initial_node)]

    # Initialise the solutions pool, with a size limit
    max_size = 5
    current_victor = SimpleNode(math.inf, [])
    solutions_pool = [current_victor]  # heapq

    # Random (selection of nodes) and mutation rates
    random_rate = 0.05
    mutation_rate = 0.1

    while frontier:

        if random.uniform(0,1) <= random_rate:
            try: tup = frontier.pop(random.randint(1,(len(frontier)-1)))  # play around wit this
            except: tup = heapq.heappop(frontier)
        else: tup = heapq.heappop(frontier)

        current_node = tup[1]

        # Attempt to improve tour using insertion nearest neighbour variant, starting from the node's state
        try:
            new_cost, insertion_nn, _ = insertion(deque([city for city in current_node.state]))
            # print(current_node.h_value, new_cost)
            if new_cost < current_node.f_value:
                tour_cost = new_cost + current_node.g_value  # find_tour_cost(insertion_nn)
                current_node.nn, current_node.f_value = insertion_nn, tour_cost
        except: pass

        # Place the found node in the solutions pool if it fits the criteria, and try to optimise it
        try:
            if not current_node.nn_in_solution_pool:
                if tup[0] <= 2*solutions_pool[-1].tour_length:
                    if len(solutions_pool) == max_size:
                        del solutions_pool[-1]
                    current_simple_node = SimpleNode(current_node.f_value, current_node.nn[:])
                    if current_simple_node not in solutions_pool:
                        heapq.heappush(solutions_pool, current_simple_node)
                        current_victor = min(current_victor, two_opt(current_simple_node))
        except: pass

        # According to the mutation rate, mutate all the node's currently in the solutions pool to potentially improve
        if random.uniform(0,1) <= mutation_rate:
            for i in range(len(solutions_pool)):
                # print("mutation")
                # print(solutions_pool[i].tour_length)
                try: solutions_pool[i] = min(solutions_pool[i], mutate(solutions_pool[i]))
                except: pass
                # print(solutions_pool[i].tour_length)
            current_victor = min(current_victor, solutions_pool[0])

        # Originally, the algorithm would end after the first goal node was reached, but it makes more sense to continue
        if current_node.goal():
            # print(f"Time taken: {time.time() - START_TIME} seconds.")
            continue
            # return current_victor.tour, current_victor.tour_length  #current_node.state, current_node.g_value

        # Obtain the nodes corresponding to the unvisited cities neighbouring the current node's city
        for child in current_node.unvisited:
            if time.time() - START_TIME > TIME_LIMIT:
                # print(f"Time running thin! ({time.time() - START_TIME} seconds have gone by) Returning current best.")
                if not current_victor.tour:
                    if not current_node.state: return new_node.nn, new_node.f_value
                    else: return current_node.state, current_node.f_value
                else: return list(current_victor.tour), current_victor.tour_length

            new_state = current_node.state[:] + [child]
            new_unvisited = current_node.unvisited[:]
            new_unvisited.remove(child)
            try:
                new_path_cost = current_node.g_value + dist_matrix[current_node.city][child]
            except TypeError:  # Will except if the node being examined is the initial node, this has no g_value.
                new_path_cost = 0
            new_node = Node(child, new_state, new_unvisited, new_path_cost)

            if current_node.first_nn == child:
                new_node.nn_in_solution_pool = True

            # If no unvisited cities remain at this point, then incorporate the distance from this node to the initial.
            if new_node.goal():
                new_node.g_value += dist_matrix[new_state[-1]][new_state[0]]

            if len(frontier) < capacity:
                heapq.heappush(frontier, (new_node.f(), new_node))
            else:
                frontier[capacity-5000:] = []
                heapq.heappush(frontier, (new_node.f(), new_node))

    # If, somehow, all nodes have been exhausted:
    return current_victor.tour, current_victor.tour_length


# -------------------------------------------------------------------------------------------------------------------- #

tour, tour_length = a_star_search()


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
















