import numpy as np


allocation_table = []  # This will be given to us as input

# number of processes
m_processes = len(allocation_table)  # n * m matrix for defining the maximum demand of each process

# number of resources
n_resources = len(allocation_table[0])  # n * m matrix for defining the number of allocated resources

available = []  # vector of length m

max_demand = []  # Maximum demand of each process


allocation = []  # WILL BE GIVEN TO US, HOLDS THE # OF RESOURCES ALREADY AQUIRED BY EACH PROCESS
# (start state)

# Todo: make these arrays the correct size
needed = []  # int[processCount][resourcesCount];
completionArray = []


# Are these arrays initlized with the right sizes? ^^, or does it change as the code goes on
# we need to change that, they are all started with size = 10, and they are all the same as
# ArrayList behind the scenes in Java

# def checkNeed(available, needed):
# hashtag for comment
def methodName(args_variables_are_snake_case, args_passed_in, args_no_type_definition,
               args_can_have_defaults=1):
    pass
    # pass means implement it later
    # indent and start


# 1.	Using Banker’s algorithm, answer the following questions:-
# i)	What is the available vector?
# Everything initially in the Max column.


# max needed for processes individually
maxArray = np.array([
    [0, 0, 1, 2],
    [1, 7, 5, 0],
    [2, 3, 5, 6],
    [0, 6, 5, 2],
    [0, 6, 5, 6]
])

three_resources_max = [10, 5, 7]

allocaArray = np.array([
    [0, 0, 1, 2],
    [1, 0, 0, 0],
    [1, 3, 5, 4],
    [0, 6, 3, 2],
    [0, 0, 1, 4]
])

needTable = maxArray - allocaArray

# def getNeedArray(_maxArray, _allocaArray):
#     needVectors = []
#     for i in len(_allocaArray):
#         availabilityVector[i] = 0
#         for j in len(_maxArray):
#             availabilityVector[i] -= availabilityVector[i][j]
#     
#     
#     needArray = []
#     availabilityVector = []
#     
#     
#     
#     #set the a
#     for i in len(_maxArray):
#         availabilityVector[i] = _maxArray[i] - availabilityVector[i]
#         
#     for i in len(_allocaArray):
#         availabilityVector[i] = 0
#         for j in len(_maxArray):
#             availabilityVector[i] += availabilityVector[i][j]
#     for i in len(needArray):
#         
#     return availabilityVector, 
# 
# 
# 
# def calcAvailableVec
# 
# def checkNeed(available, needed): #is this a boolean? no, method
#     for i in range(len(needed)):
#         current_process = needed[i]
#         sum = 0
#         if needed[i] > available[i]:
#             continue
#         else:
#             # mark process as finished
#             completionArray = True # // complete
#             #then update the tabele
#             available[i] -= needed[i]
# 
# while False in completionArray:
#      avialable, needed = checkNeed(available, needed)
