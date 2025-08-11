# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
import random
from game import Directions
from util import manhattanDistance

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide. You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        """
    
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()  # nea thesi
        newFood = successorGameState.getFood()  # fagito pou den exoume vrei
        newGhostStates = successorGameState.getGhostStates()  # katastasi extrwn
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  # Scared timeout

        # ksekiname me to arxiko score
        score = successorGameState.getScore()

        foodList = newFood.asList()  # foodgrid = theseis ston xarth
        if foodList:  # elegxos an yparxei faghto
            foodDistances = [manhattanDistance(newPos, food) for food in foodList]
            closestFoodDist = min(foodDistances)
            if closestFoodDist > 0:  # gia na mhn diairesw me to 0 
                score += 10.0 / closestFoodDist  # ++score an eimaste konta sto faghto

        # apostash apo to kontinotero fantasma
        ghostDistances = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
        for i, ghostDist in enumerate(ghostDistances):
            if ghostDist > 0:  # gia na mhn diairesw me to 0 
                if newScaredTimes[i] > 0:  # an to fantasma einai scared
                    score += 10.0 / ghostDist  # ++ sto score an to fame
                else:
                    score -= 20.0 / ghostDist  # afairesh apo to score an eisai konta se fantasma

        # elegxos gia to fagito pou ksemine
        score -= len(foodList) * 4  # afairesh apo to score gia faghto pou ksemine

        capsules = currentGameState.getCapsules()
        if capsules:  # an exoun meinei capsules, proteraiothta sto na tis parei
            capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in capsules]
            closestCapsuleDist = min(capsuleDistances)
            if closestCapsuleDist > 0:  # gia na mhn diairesw me to 0 
                score += 5.0 / closestCapsuleDist  # ++score an eimaste konta se capsule

        return score




def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        def minimax(agentIndex, depth, gameState):
            # an ftasoume sto max depth h an fame olo to fagito
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # an o agent einai o pacman If the agent is Pacman (Maximizer)
            if agentIndex == 0:
                return maxValue(agentIndex, depth, gameState)

            # an o agent eina fantasma (Minimizer)
            else:
                return minValue(agentIndex, depth, gameState)

        def maxValue(agentIndex, depth, gameState):
            # diathesimes kinhseis tou pacman
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  # den exw kati na kanw
                return self.evaluationFunction(gameState)

            # eksetase kathe kinissi kai epetrepse thn max timh 
            return max(minimax(1, depth, gameState.generateSuccessor(agentIndex, action)) for action in legalMoves)

        def minValue(agentIndex, depth, gameState):
            # diathesimes kinhsseis gia ta fantasmata
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  # an den exei kapoia kinhsh
                return self.evaluationFunction(gameState)

            # gia nakatalavw an o epomenos agent einai o pacman h to fantasma
            nextAgent = agentIndex + 1
            if nextAgent == gameState.getNumAgents():  # pacman
                nextAgent = 0
                depth += 1  # auksisi vathous afou exoun kinhthei ola ta fantasmata

            # aksiologisi kathe kinisiss, eepistrefw thn mikroterh timh
            return min(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in legalMoves)

        # kinhsh me thn megaluterh minimax timh gia ton pacman 
        legalMoves = gameState.getLegalActions(0)
        scores = [minimax(1, 0, gameState.generateSuccessor(0, action)) for action in legalMoves]
        bestScore = max(scores)

        # epistrefw thn kinhsh me to kalutero score 
        bestIndices = [index for index, score in enumerate(scores) if score == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your alpha-beta pruning agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the best action using alpha-beta pruning.
        """
        def alphaBeta(agentIndex, depth, gameState, alpha, beta):
            # Terminal state or depth reached
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # otan o pacman einai o agent(maximizer)
            if agentIndex == 0:
                return maxValue(agentIndex, depth, gameState, alpha, beta)

            # alliws otan einai to fantasma (minimizer)
            else:
                return minValue(agentIndex, depth, gameState, alpha, beta)

        def maxValue(agentIndex, depth, gameState, alpha, beta):
            # epitrepomenes kinhseis
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  # den mporei na kinhthei
                return self.evaluationFunction(gameState)

            v = float('-inf')  # arxikopoihssh me arnhtiko apeiro(logikh alpha beta prune)
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v, alphaBeta(1, depth, successor, alpha, beta))
                if v > beta:  # prune an
                    return v
                alpha = max(alpha, v)  # enhmerwsee to a alpha
            return v

        def minValue(agentIndex, depth, gameState, alpha, beta):
            # kinhseis fantasmatos
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  # an den mporei na kounithei
                return self.evaluationFunction(gameState)

            v = float('inf')  #  arxikoppoihsh +apeiro
            nextAgent = agentIndex + 1
            if nextAgent == gameState.getNumAgents():  # an to teleytaio einai fantasma, phgainei ston papcman
                nextAgent = 0
                depth += 1  # afou exoun kinithei oloi, aukssise to vathos

            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v, alphaBeta(nextAgent, depth, successor, alpha, beta))
                if v < alpha:  # prune
                    return v
                beta = min(beta, v)  
            return v

        # arxikopoihsh
        alpha = float('-inf')
        beta = float('inf')

        #  h kaluterh kinhsh gia ton pacman
        legalMoves = gameState.getLegalActions(0)
        bestAction = None
        bestValue = float('-inf')

        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            value = alphaBeta(1, 0, successor, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)

        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the best action using the Expectimax algorithm.
        """

        def expectimax(agentIndex, depth, gameState):
            # telikh kinhsh(h alliws max depth)
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # pacman (Maximizer)
            if agentIndex == 0:
                return maxValue(agentIndex, depth, gameState)

            # fantasma  (expectedValue(agentIndex, depth, gameState))

            else:
                return expectedValue(agentIndex, depth, gameState)

        def maxValue(agentIndex, depth, gameState):
            # kinhseis pacman
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  # den mporeei na kinhthe
                return self.evaluationFunction(gameState)

            v = float('-inf')  #  arxikopoihsh me arnhtiko apeiro
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v, expectimax(1, depth, successor))  # epomenos agent, fantasma
            return v

        def expectedValue(agentIndex, depth, gameState):
            # kinhseis fantasmatos
            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:  
                return self.evaluationFunction(gameState)

            v = 0  # exppected value
            prob = 1.0 / len(legalMoves)  # kathe kinhsh exei idia pithanothta 
            nextAgent = agentIndex + 1
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                depth += 1  # aukshsh vathous afou exoun kinhhei oloi oi agents

            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                v += prob * expectimax(nextAgent, depth, successor)  # upologismos ektimwmenhs timhs
            return v
        legalMoves = gameState.getLegalActions(0)
        bestAction = None
        bestValue = float('-inf')
        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            value = expectimax(1, 0, successor)  # o epomenos agent tha einai to prwto fantasma
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme Pacman evaluation function (question 5).
    """
    pacmanPos = currentGameState.getPacmanPosition()  # thesi pacman
    foodGrid = currentGameState.getFood()  # fagito pou den exw ftasei
    foodList = foodGrid.asList()  # thesi fagitou
    ghostStates = currentGameState.getGhostStates()  # scared or not scared fantasma
    capsules = currentGameState.getCapsules()  # thesi superfood
    score = currentGameState.getScore()  # game score

    evaluationScore = score

    if foodList:
        foodDistances = [manhattanDistance(pacmanPos, food) for food in foodList]
        closestFoodDist = min(foodDistances)
        evaluationScore += 10.0 / closestFoodDist  

    if capsules:
        capsuleDistances = [manhattanDistance(pacmanPos, capsule) for capsule in capsules]
        closestCapsuleDist = min(capsuleDistances)
        evaluationScore += 15.0 / closestCapsuleDist  

    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDist = manhattanDistance(pacmanPos, ghostPos)
        if ghostDist > 0:  # gia na mhn diairw me to 0
            if ghostState.scaredTimer > 0:  # Scared ghosts
                evaluationScore += 20.0 / ghostDist  # ++pontoi an kinigaei ta fantasmata pou einai scared
            else:  # Active ghost
                evaluationScore -= 25.0 / ghostDist  # afairesh vathmwn gia kathe fora pou einai konta se fantasma

    
    evaluationScore -= 4 * len(foodList)  # afairesh vathmwn gia fagito pou ksemine

    evaluationScore -= 3 * len(capsules)  # afairesh vathmwn gia superfood(capsules) pou kseminan

    return evaluationScore

better = betterEvaluationFunction
