import numpy as np
from node import Node
from node import Puzzle
from node import Distance

# Input for heuristics and informed search
heuristic = input("Choose a Heuristic: \n 1. Misplaced Tiles \n 2. Manhattan Distance \n")
informed = input("Choose an Informed Search: \n 1. Greedy Best First Search \n 2. A* Algorithm \n")
heuristic = int(heuristic)
informed = int(informed)

initial_board = [2, 8, 3, 1, 6, 4, 7, 0, 5]
final_board = [1, 2, 3, 8, 0, 4, 7, 6, 5]

# Initialize nodes for the start and goal states
initial_board = Node(initial_board)
final_board = Node(final_board)
explored_nodes = []
fringe = [initial_board]

# Calculate the initial heuristic distance
distance = Distance.distance(initial_board.get_current_state(), final_board.get_current_state(), heuristic)
initial_board.update_hn(distance)

count = 1

print("8 puzzle problem Start State: \n")
Puzzle.print_state(initial_board, informed)

print("8 puzzle goal: \n")
Puzzle.print_state(final_board, informed)

print("---------------Printing Solution Path---------------\n \n")

while fringe:
    minimum_fn_index = Puzzle.least_fn(fringe, informed)  # Use the informed flag
    current_node = fringe.pop(minimum_fn_index)
    g = current_node.get_gn() + 1
    goal_node = np.asarray(final_board.get_current_state())

    # Goal reached
    if np.array_equal(np.asarray(current_node.get_current_state()), goal_node):
        distance = Distance.distance(np.asarray(current_node.get_current_state()), goal_node, heuristic)
        explored_nodes.append(current_node)
        Puzzle.goal_reached(explored_nodes, count, informed)
        fringe = []
        
    else:
        zero = np.where(np.asarray(current_node.get_current_state()) == 0)[0][0]
        count = Node.expand_node(fringe, explored_nodes, current_node, goal_node, zero, g, count, heuristic)



