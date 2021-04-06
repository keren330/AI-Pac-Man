# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    
    # checked: the node has been seen, which is a list
    # fringe: unexpanded nodes, which are stack
    checked = []
    fringe = util.Stack()
    actions = []
    start_node = problem.getStartState()
    # Initialize
    # get the start state and actions
    fringe.push((start_node, actions)) 

    # start state has been checked
    # checked.append(problem.getStartState())

    while fringe.isEmpty() == False:
        current_node, actions = fringe.pop()

        # If current node is goal state, then stop and return path.
        if problem.isGoalState(current_node):
            return actions

        if current_node not in checked:
            # get successor, and expand is a tuple: (successor, action, stepCost)
            expand = problem.getSuccessors(current_node)
            # once expanded, the current_node is checked
            checked.append(current_node)

            for child in expand:
                next_node = child[0] 
                next_move = child[1] 
                
                if next_node not in checked:
                    new_actions = actions+ [next_move]
                    fringe.push((next_node, new_actions))
    return []

    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"

    start_node = problem.getStartState()
    checked = []
    actions = []
    fringe = util.Queue()

    fringe.push( (start_node, actions) )

    while fringe.isEmpty() == False:
        current_node, actions = fringe.pop()
        if problem.isGoalState(current_node):
            return actions
        if current_node not in checked:
            expand = problem.getSuccessors(current_node)
            checked.append(current_node)
            for next_node, next_move, next_costs in expand:
                if next_node not in checked:
                    new_actions = actions + [next_move]
                    fringe.push((next_node, new_actions))
    return []
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    start_node = problem.getStartState()
    checked = []
    actions = []
    fringe = util.PriorityQueue()
    fringe.push( (start_node, actions, 0), 0 )


    while fringe.isEmpty() == False:
        current_node, actions, costs = fringe.pop()
        if problem.isGoalState(current_node):
            return actions

        if current_node not in checked:
            expand = problem.getSuccessors(current_node)
            checked.append(current_node)
            for next_node, next_move, next_cost in expand:
                new_actions = actions + [next_move]
                new_costs = costs + next_cost
                if next_node not in checked:
                    fringe.push((next_node, new_actions, new_costs), new_costs)
    return []
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    
    # checked: the node has been seen, which is a list
    # fringe: unexpanded nodes, which are priority queue
    start_node = problem.getStartState()
    fringe = util.PriorityQueue()
    checked = []
    actions = []
    # fringe is a priority queue, priority.push(item, priority)
    # item is a tuple(node, action, cost), and priority is f(n)
    # everytime take the smallest one out
    # at start state, g = 0 and h = heuristic(start_node, problem), so f = g + h
    fringe.push((start_node, actions, 0), 0 + int(heuristic(start_node, problem)))

    while fringe.isEmpty() == False:
        # pop() only return item, not include priority
        current_node, actions, costs = fringe.pop() 

        if problem.isGoalState(current_node):
            return actions
        
        if current_node not in checked:
            expand = problem.getSuccessors(current_node)
            checked.append(current_node)
            for next_node, next_move, next_cost in expand:
                if next_node not in checked:
                    new_actions = actions + [next_move]
                    new_costs = costs + next_cost
                    f = new_costs + heuristic(next_node, problem)
                    fringe.push((next_node, new_actions, new_costs), f)
    return []

    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
