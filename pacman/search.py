# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    start = problem.getStartState()
    explored = list()
    frontier = util.Stack()
    frontier.push((start, 'START', 0))
    paths = list()
    paths.append([(start, 'START', 0)])

    while True:

        if frontier.isEmpty():
            return False

        current_path = paths.pop()
        current_frontier = frontier.pop()
        current_node = current_frontier[0]
        if not current_node in explored:
            explored.append(current_node)

        if problem.isGoalState(current_node):
            return [x[1] for x in current_path[1:]]

        for successor in problem.getSuccessors(current_node):
            if not (successor[0] in explored):
                next_path = list(current_path) + [successor]
                paths.append(next_path)
                frontier.push(successor)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    start = problem.getStartState()
    explored = list()
    frontier = util.Queue()
    frontier.push((start, 'START', 0))
    paths = list()
    paths.append([(start, 'START', 0)])

    while True:

        if frontier.isEmpty():
            return False
        current_path = paths.pop(0)

        current_frontier = frontier.pop()
        current_node = current_frontier[0]
        if not current_node in explored:
            explored.append(current_node)

            if problem.isGoalState(current_node):
                return [x[1] for x in  current_path[1:]]

            for successor in problem.getSuccessors(current_node):
                if not (successor[0] in explored):
                    next_path = list(current_path) + [successor]
                    paths.append(next_path)
                    frontier.push(successor)



def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    start = problem.getStartState()
    explored = list()
    frontier = util.PriorityQueue()

    frontier.push(([(start, "START", 0)], 0), 0)

    while True:

        if frontier.isEmpty():
            return False

        current_frontier = frontier.pop()
        current_path = current_frontier[0]
        current_node = current_path[-1][0]
        current_cost = current_frontier[1]

        if not current_node in explored:
            explored.append(current_node)

            if problem.isGoalState(current_node):
                return([x[1] for x in current_path[1:]])

            for successor in problem.getSuccessors(current_node):
                if not (successor[0] in explored):
                    next_path = list(current_path) + [successor]
                    next_cost = current_cost + successor[2]
                    frontier.push((next_path, next_cost), next_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    start = problem.getStartState()
    explored = []
    frontier = util.PriorityQueue()

    frontier.push(([(start, "START", 0)], 0), 0)

    while True:

        if frontier.isEmpty():
            return False

        current_frontier = frontier.pop()

        current_path = current_frontier[0]
        current_node = current_path[-1][0]
        current_cost = current_frontier[1]



        if not current_node in explored:
            explored.append(current_node)

            if problem.isGoalState(current_node):
                return [x[1] for x in current_path[1:]]

            non_explored_states = filter(lambda next_successor: not next_successor[0] in explored,
                                        problem.getSuccessors(current_node))

            for successor in non_explored_states:
                if successor[0] not in explored:
                    next_cost = current_cost + successor[2]
                    next_path = (list(current_path)+[successor], next_cost)
                    frontier.push(next_path, next_cost + heuristic(successor[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
