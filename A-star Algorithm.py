import heapq
import numpy as np
from queue import PriorityQueue
from heapq import heapify, heappush, heappop
from copy import deepcopy


class eightpuzzleusingastar:
    #Intializing Object
    def __init__(self, initial_state=None):
        self.state_node = initial_state
        self.puzzle_matrix_grid = 3
        self.heuristic_h = 0
        self.path_cost_g = 0
        self.total_cost_f = 0
        self.parent = None
        self.id = self.state_id()
    # Finding Id of a node
    def state_id(self):
        return ''.join(str(item) for innerlist in self.state_node for item in innerlist)
    # comparing the total cost of a nodes
    def __lt__(self, next):
        return self.total_cost_f < next.total_cost_f

    def is_equal(self, state1, state2):
        state1_value = "".join(str(item) for innerlist in state1 for item in innerlist)
        state2_value = "".join(str(item) for innerlist in state2 for item in innerlist)
        return state1_value == state2_value
    # To Print the Path
    def printPath(self, node):
        print('**************************************************************************************************')
        print('Path ')
        pathcost = node.path_cost_g
        path = []
        while node:
            path.append(node.state_node)
            node = node.parent
        for node in reversed(path):
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in node:
                for j in i:
                    print(j, end=" ")
                print("")
        print("Goal is found at depth ", pathcost)
    #Get the heuristic cost by mis-placed tiles
    def get_heuristic_cost_hamming(self, current, goal):
        hamming_cost = 0;
        for i in range(self.puzzle_matrix_grid):
            for j in range(self.puzzle_matrix_grid):
                if current[i][j] != goal[i][j] and current[i][j] != 0:
                    hamming_cost = hamming_cost + 1
        return hamming_cost;

    # Get the heuristic cost by manhanttan distance
    def get_heuristic_cost_manhattan(self, current, goal):
        cost = 0
        element_position = {}
        # FINDING THE EXACT POSTION OF A ELEMENT
        for i in range(self.puzzle_matrix_grid):
            for j in range(self.puzzle_matrix_grid):
                element_position[current[i][j]] = (i, j)

        # FINDING THE COST FOR THE NODE BY COMPARING WITH THE GOAL NODE
        for i in range(self.puzzle_matrix_grid):
            for j in range(self.puzzle_matrix_grid):
                if current[i][j] != goal[i][j] and current[i][j] != 0:
                    index = element_position[goal[i][j]]
                    cost = cost + abs(i - index[0]) + \
                           abs(j - index[1])
        return cost

    def zero_index(self, intial):
        for i in range(0, self.puzzle_matrix_grid):
            for j in range(0, self.puzzle_matrix_grid):
                if intial[i][j] == 0:
                    return (i, j)
    #To generate successors by moving empty space UP,left,right,down direction where applicable
    def move_node(self, node, row, col, direction):
        if (direction == "up"):
            child_up = deepcopy(node)
            current_number = child_up[row][col]
            child_up[row][col] = child_up[row + 1][col]
            child_up[row + 1][col] = current_number
            return child_up
        elif (direction == "down"):
            child_down = deepcopy(node)
            current_number = child_down[row][col]
            child_down[row][col] = child_down[row - 1][col]
            child_down[row - 1][col] = current_number
            return child_down
        elif (direction == "left"):
            child_left = deepcopy(node)
            current_number = child_left[row][col]
            child_left[row][col] = child_left[row][col + 1]
            child_left[row][col + 1] = current_number
            return child_left
        elif (direction == "right"):
            child_right = deepcopy(node)
            current_number = child_right[row][col]
            child_right[row][col] = child_right[row][col - 1]
            child_right[row][col - 1] = current_number
            return child_right

    def open_current_node(self, node):
        (row, col) = self.zero_index(node)
        current_number = 0
        possibility_list = []
        if row + 1 < self.puzzle_matrix_grid:
            possibility_list.append(
                self.move_node(node, row, col, "up"))
        if row - 1 >= 0:
            possibility_list.append(
                self.move_node(node, row, col, "down"))
        if col + 1 < self.puzzle_matrix_grid:
            possibility_list.append(
                self.move_node(node, row, col, "left"))
        if col - 1 >= 0:
            possibility_list.append(
                self.move_node(node, row, col, "right"))
        return possibility_list
    # Astar algorithm performing to find the solution
    def Astar(self, method_type, intial, goal):
        Vistied_node_list = []
        nodelists = []
        visited_nodes_set = set()
        opened_nodes = set()
        visted_node_counts = 0
        generated_nodes_total = 0

        if self.is_equal(intial.state_node, goal.state_node):
            print("Puzzle solved")
            print("Total Expanded Nodes are :" + str(visted_node_counts))
            print("Total Generated Nodes are :" + str(generated_nodes_total))
            self.printPath(intial)
            return intial.state_node
        if (method_type == "hamming"):
            intial.heuristic_h = self.get_heuristic_cost_hamming(intial.state_node, goal.state_node)
        if (method_type == "manhattan"):
            intial.heuristic_h = self.get_heuristic_cost_manhattan(intial.state_node, goal.state_node)

        intial.total_cost_f = intial.heuristic_h + intial.path_cost_g
        heappush(nodelists, intial)
        opened_nodes.add(intial.id)

        print("Solving Puzzle with " + str(
            method_type) + " distance Using A-star Algorithm with.........................")

        while len(nodelists):
            current_node = heappop(nodelists)
            Vistied_node_list.append(current_node)
            visited_nodes_set.add(current_node.id)
            visted_node_counts = visted_node_counts + 1
            successor_nodes = self.open_current_node(current_node.state_node)
            for childnode in successor_nodes:
                child = eightpuzzleusingastar(childnode)
                if method_type == "hamming":
                    child.heuristic_h = self.get_heuristic_cost_hamming(child.state_node, goal.state_node)
                if method_type == "manhattan":
                    child.heuristic_h = self.get_heuristic_cost_manhattan(child.state_node, goal.state_node)
                child.path_cost_g = current_node.path_cost_g + 1
                child.total_cost_f = child.heuristic_h + child.path_cost_g
                child.parent = current_node
                generated_nodes_total = generated_nodes_total + 1
                if self.is_equal(child.state_node, goal.state_node):
                    print("Puzzle solved")
                    self.printPath(child)
                    print("Total Expanded Nodes are :" + str(visted_node_counts))
                    print("Total Generated Nodes are :" + str(generated_nodes_total))
                    return child.state_node
                if child.id not in opened_nodes:
                    if child.id not in visited_nodes_set:
                        heappush(nodelists, child)
                        nodelists.append(child)
                        opened_nodes.add(child.id)
                elif child.id not in visited_nodes_set:
                    for i in range(0,len(nodelists)):
                        if nodelists[i].id == child.id and nodelists[i].total_cost_f > child.total_cost_f:
                            heappush(nodelists, child)
                            opened_nodes.add(child.id)
        return nodelists

#Getting User Input for Intial State, Goal State and Heuristic function
def get_userinputdata():
    intial = []
    goal = []
    for i in (0, 1):
        states_type = ["Intial", 'Goal'];
        print("Taking " + states_type[i] + " State Inputs' entries rowwise:-\n Consider Zero as a Empty Space");
        if i == 0:
            for i in range(0, 3, 1):
                startmatrixdata = []
                for j in range(0, 3, 1):
                    startmatrixdata.append(int(input()))
                intial.append(startmatrixdata)
        else:
            for i in range(0, 3, 1):
                goalmatrixdata = []
                for j in range(0, 3, 1):
                    goalmatrixdata.append(int(input()))
                goal.append(goalmatrixdata)
    print("Intial State:")
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):
            print(intial[i][j], end=" ")
        print()
    print("Goal State:")
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):
            print(goal[i][j], end=" ")
        print()

    print("Enter the Herustic Function:")
    print("1. Manhanttan-distance Herustic ")
    print("2. Mis-placed tiles herustic")
    try:
        heuristic_function = int(input('Heurstic Function: '))
        if heuristic_function < 1 or heuristic_function > 2:
            raise ValueError  # this will send it to the print message and back to the input option
        if (heuristic_function):
            if heuristic_function == 1:
                heuristic_val = "manhattan"
            else:
                heuristic_val = "hamming"
    except ValueError:
        print("Invalid integer. The number must be in the range of 1-10.")

    return intial, goal, heuristic_val;

#main function
if __name__ == '__main__':
    intial, goal, heuristic_val = get_userinputdata()
    intial_puzzle = eightpuzzleusingastar(intial)
    goal_puzzle = eightpuzzleusingastar(goal)
    intial_puzzle.Astar(heuristic_val, intial_puzzle, goal_puzzle)

