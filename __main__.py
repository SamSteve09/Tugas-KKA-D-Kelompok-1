import numpy as np
from node import Node
from node import Puzzle
from node import Distance

# Function to count inversions in the given array
def get_inv_count(arr):
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            # Excluding the empty tile 0
            if arr[i] != 0 and arr[j] != 0 and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

# Function to check if the puzzle is solvable
def solvable(initial, goal):
    inv_count_initial = get_inv_count(initial)
    inv_count_goal = get_inv_count(goal)
    
    return (inv_count_initial % 2) == (inv_count_goal % 2)

# Function to get valid input (1 or 2)
def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input == '1' or user_input == '2':
            return user_input
        else:
            print("Invalid input. Please enter 1 or 2.")

# Ask for informed search method
informed = get_valid_input("Choose an Informed Search: \n 1. Greedy Best First Search \n 2. A* Algorithm \n")
# Ask for heuristic function that will be used
heuristic = get_valid_input("Choose a Heuristic: \n 1. Misplaced Tiles \n 2. Manhattan Distance \n")

heuristic = int(heuristic)
informed = int(informed)

# Define the initial and final board states as NumPy arrays

# Example Case 1
# initial_board = [2, 8, 3, 1, 6, 4, 7, 0, 5]

# Example Case 2 (Heuristic function affect how many nodes that will be expanded resulting to the 2time complexity)
# initial_board = [2, 3, 4, 1, 6, 8, 7, 0, 5]

# Example Case 3 (Greedy much better in time complexity, but A* give the optimal solution)
initial_board = [5, 1, 4, 6, 7, 3, 2, 0, 8]

final_board = [1, 2, 3, 8, 0, 4, 7, 6, 5]

# Check if the initial board is solvable
if not solvable(initial_board, final_board):
    print("The puzzle is not solvable.")
else:
    # Initialize nodes for the start and goal states
    initial_node = Node(initial_board)
    final_node = Node(final_board)
    explored_nodes = []
    fringe = [initial_node]

    # Calculate the initial heuristic distance
    distance = Distance.distance(initial_node.get_current_state(), final_node.get_current_state(), heuristic)
    initial_node.update_hn(distance)

    count = 1

    print("8 puzzle problem Start State: \n")
    Puzzle.print_state(initial_node, informed)

    print("8 puzzle goal: \n")
    Puzzle.print_state(final_node, informed)

    print("------------------Printing Solution Path------------------\n \n")

    while fringe:
        minimum_fn_index = Puzzle.least_fn(fringe, informed)  # Use the informed flag
        current_node = fringe.pop(minimum_fn_index)
        g = current_node.get_gn() + 1
        goal_node = np.asarray(final_node.get_current_state())

        # Goal reached
        if np.array_equal(np.asarray(current_node.get_current_state()), goal_node):
            distance = Distance.distance(np.asarray(current_node.get_current_state()), goal_node, heuristic)
            explored_nodes.append(current_node)
            Puzzle.goal_reached(explored_nodes, count, informed)
            fringe = []
        else:
            zero = np.where(np.asarray(current_node.get_current_state()) == 0)[0][0]
            count = Node.expand_node(fringe, explored_nodes, current_node, goal_node, zero, g, count, heuristic)
