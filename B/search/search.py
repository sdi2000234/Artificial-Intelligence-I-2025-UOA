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
from util import Queue
from util import Stack
from util import PriorityQueue

from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    # Stoiva gia thn apothikefsi paths kai states.
    Path_State_stack = Stack()
    
    # empty path gia to arxiko state
    start_state = problem.getStartState()
    Path_State_stack.push((start_state, []))  # (state, path)
    
    # gia na gnwrizw poia nodes exw episkeftei
    visited = set()
    
    # Loop mexri na einai adeio to stack
    while not Path_State_stack.isEmpty():
        # vgale to state kai to path pou mas eftase mexri auto to state
        current_state, current_path = Path_State_stack.pop()
        
        # an to state pou eimaste twra den einai o stoxos mas, epestrepe to path
        if problem.isGoalState(current_state):
            return current_path
        
        # An den exoume paei se auto to path, prosthese to
        if current_state not in visited:
            visited.add(current_state)
            
            for successor, action, _ in problem.getSuccessors(current_state):
                # vazoume oles tis epituxies sto stack
                new_path = current_path + [action]
                Path_State_stack.push((successor, new_path))
    
    # an den vrw lush, epistrefw kenh lista
    return []


def breadthFirstSearch(problem):
    # Oura gia thn apothikefsi paths kai states.
    Oura = Queue()
    
    # empty path gia to arxiko state
    start_state = problem.getStartState()
    Oura.push((start_state, []))  # (state, path)
    
    # gia na gnwrizw poia nodes exw episkeftei
    visited = set()
    
    # Loop mexri na einai adeio to queue
    while not Oura.isEmpty():
        # vgale to state kai to path pou mas eftase se auto to state
        current_state, current_path = Oura.pop()
        
        # an to state lunei to provlima, epestrepse auto
        if problem.isGoalState(current_state):
            return current_path
        
        # An den exoume paei se auto to state prosthese to
        if current_state not in visited:
            visited.add(current_state)
            
            
            for successor, action, _ in problem.getSuccessors(current_state):
                # vazoume oles tis epituxies sto queue
                new_path = current_path + [action]
                Oura.push((successor, new_path))
    
    # an den vrw lush, epistrefw kenh lista
    return []

def uniformCostSearch(problem):
    # Priority queue gia apothikefsi twn states, me protaireothta to kostos
    PQueue = PriorityQueue()
    
    start_state = problem.getStartState()
    PQueue.push((start_state, [], 0), 0)  # (state, path, cost), priority = cost
    
    # dictionary gia na gnwrizoume to kalutero kostos gia na ftasoume kathe nod
    visitedNode = {}
    
    # Loop mexri to queue mas na einai keno
    while not PQueue.isEmpty():
        # vgale to state me to ligotero kostos
        current_state, current_path, current_cost = PQueue.pop()
        
        # an to state einai to kalytero dinato path, epestrepe to path
        if problem.isGoalState(current_state):
            return current_path
        
        # an den exoume paei h vrikame ftinotero path
        if current_state not in visitedNode or current_cost < visitedNode[current_state]:
            visitedNode[current_state] = current_cost  # vale to state me to neo pleon kostos
            
            # vres ola ta epituxeis path
            for successor, action, step_cost in problem.getSuccessors(current_state):
                # upologise to kostos gia na ftaseis sto swsto(successor)path
                new_cost = current_cost + step_cost
                new_path = current_path + [action]
                
                # prosthese to swsto path sto queue me to neo kostos,path
                PQueue.push((successor, new_path, new_cost), new_cost)
    
    # an den vrw lush, epistrefw kenh lista
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    # Priority queue gia apothikefsi twn states, me protaireothta to kostos
    PQueue = PriorityQueue()
    
    start_state = problem.getStartState()
    PQueue.push((start_state, [], 0), heuristic(start_state, problem))  # (state, path, cost), priority = g(n) + h(n)
    
    # dictionary gia na gnwrizoume to kalutero kostos gia na ftasoume kathe nod
    visited = {}
    
    # Loop until the priority queue is empty
    while not PQueue.isEmpty():
        # Dequeue the state with the lowest f(n) = g(n) + h(n)
        current_state, current_path, current_cost = PQueue.pop()
        
        # an to state einai o stoxos ams(veltisto path), epestrepe to path
        if problem.isGoalState(current_state):
            return current_path
        
        # an den exoume paei h vrikame ftinotero path
        if current_state not in visited or current_cost < visited[current_state]:
            visited[current_state] = current_cost  # Mark state with the new cost
            
            # vres ola ta epituxeis path
            for successor, action, step_cost in problem.getSuccessors(current_state):
                # upologise to kostos gia na ftaseis sto swsto(successor)path
                new_cost = current_cost + step_cost
                new_path = current_path + [action]
                
                # Calculate the total cost with the heuristic
                priority = new_cost + heuristic(successor, problem)
                
                # prosthese to swsto path sto queue me to neo kostos,path
                PQueue.push((successor, new_path, new_cost), priority)
    
    # If no solution is found, return an empty list
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
