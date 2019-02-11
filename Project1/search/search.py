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
    """
    
    # necessary structures/initialisations

    checked = []
    result = []
    stack = util.Stack() 

    xy = problem.getStartState()
    
    stack.push(xy)
    allPaths = util.Stack()
    temp = []
    allPaths.push(temp)

    # runs bfs algorithm using queue
    while (not stack.isEmpty()):
        xy = stack.pop()
        curr = allPaths.pop()
        if xy not in checked:       
            checked.append(xy)
            if problem.isGoalState(xy):
                result.extend(curr)
                break;
            # adds successurs according to algorithm
            for succ in problem.getSuccessors(xy):
                xySucc = succ[0]
                action = succ[1]
                stack.push(xySucc)
                ls2 = []
                ls2.extend(curr)
                ls2.append(action)
                allPaths.push(ls2)

    return result
    
    util.raiseNotDefined()



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # necessary structures/initialisations

    checked = []
    result = []
    queue = util.Queue()

    xy = problem.getStartState()
     
    queue.push(xy)
    checked.append(xy)

    allPaths = util.Queue()
    temp = []
    allPaths.push(temp)

    # runs bfs algorithm using queue
    while (not queue.isEmpty()):
        (xy) = queue.pop()
        curr = allPaths.pop()
        if problem.isGoalState(xy):
            result.extend(curr)
            break
        # adds successurs according to algorithm
        for succ in problem.getSuccessors(xy):
            xySucc = succ[0]
            action = succ[1]
            if (xySucc) not in checked:       
                checked.append((xySucc))
                queue.push((xySucc))
                ls2 = []
                ls2.extend(curr)
                ls2.append(action)
                allPaths.push(ls2)

    return result
    

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    # necessary structures/initialisations

    checked = []
    result = []
    queue = util.PriorityQueue()

    xy = problem.getStartState()
     
    queue.push(xy,0)

    allPaths = util.PriorityQueue()
    temp = []
    allPaths.push(temp,0)

    # runs the loop to get elements from pq
    # appends to checked, breaks if goal
    while (not queue.isEmpty()):
        xy = queue.pop()
        curr = allPaths.pop()
        if (xy) not in checked:       
            checked.append(xy)
            if problem.isGoalState(xy):
                result.extend(curr)
                break
            # puts successors in priority queue
            # depending on their cost
            for succ in problem.getSuccessors(xy):
                xySucc = succ[0]
                action = succ[1]
                ls2 = []
                ls2.extend(curr)
                ls2.append(action)
                cost = problem.getCostOfActions(ls2)
                queue.push(xySucc,cost)
                allPaths.push(ls2,cost)


    return result
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # necessary structures/initialisations

    checked = []
    result = []
    queue = util.PriorityQueue()

    xy = problem.getStartState()
     
    queue.push(xy,0+heuristic(xy,problem))

    allPaths = util.PriorityQueue()
    temp = []
    allPaths.push(temp,0+heuristic(xy,problem))

    # runs the loop to get elements from pq
    # appends to checked, breaks if goal
    while (not queue.isEmpty()):
        xy = queue.pop()
        curr = allPaths.pop()
        if (xy) not in checked:       
            checked.append(xy)
            if problem.isGoalState(xy):
                result.extend(curr)
                break
            # puts successors in priority queue depending on 
            # their cost + heuristic
            for succ in problem.getSuccessors(xy):
                xySucc = succ[0]
                action = succ[1]
                ls2 = []
                ls2.extend(curr)
                ls2.append(action)
                cost = problem.getCostOfActions(ls2)
                cost += heuristic(xySucc,problem)
                queue.push(xySucc,cost)
                allPaths.push(ls2,cost)


    return result


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
