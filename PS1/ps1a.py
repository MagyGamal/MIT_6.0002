###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:Magy Gamal
# Collaborators:engineer mubarak,youssef mohamed
# Time:
from ps1_partition import get_partitions
import time
#================================
# Part A: Transporting Space Cows
#================================
# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    inFile = open(filename, 'r')
    cows_dict={}
    for line in inFile:
        name,weight=line.split(",")
        cows_dict[name]=weight.strip()
    return cows_dict   
#print(load_cows("ps1_cow_data.txt"))
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:
    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows
    Does not mutate the given dictionary of cows.
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
   """
    trip_limit=0
    transported_cows=[]
    cows_list=[]
    cows_copy=sorted(cows.items(), key=lambda x: x[1] , reverse=True)
    for i in cows_copy:
        if int(i[1]) <= limit:
            trip_limit+=int(i[1])
            if trip_limit<=limit:
                cows_list.append(i[0])
            else:
                transported_cows.append(cows_list)
                cows_list=[]
                trip_limit=0
                trip_limit+=int(i[1])
                cows_list.append(i[0])
    transported_cows.append(cows_list)        
    return transported_cows
print("greedy result=",greedy_cow_transport(load_cows("ps1_cow_data.txt"),limit=10))
# Problem 3 
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    transported_cows=[]
    trip_limit=0
    s=limit
    for x in get_partitions(cows):
        valid=True
        for y in x:
            for z in y:
                trip_limit += int(cows[z])
            if trip_limit>limit:
                valid=False
            trip_limit=0
        if valid ==True:
            transported_cows.append(x)
    for e in transported_cows:
        if len(e)<s:
            s=len(e)
    for l in transported_cows:
        if len(l)==s:
            return l
print("brute_force result=",brute_force_cow_transport(load_cows("ps1_cow_data.txt"),limit=10))   
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    g=greedy_cow_transport(load_cows("ps1_cow_data.txt"),limit=10)
    end = time.time()
    diff=end-start
    print("time taken by greedy=",diff)
    g=greedy_cow_transport(load_cows("ps1_cow_data.txt"),limit=10)
    print("number of trips by greedy=",len(g))
    start = time.time()
    b=brute_force_cow_transport(load_cows("ps1_cow_data.txt"),limit=10)
    end = time.time()
    diff=end-start
    print("time taken by brute=",diff)
    print("number of trips by brute=",len(b))
    return None
print(compare_cow_transport_algorithms())