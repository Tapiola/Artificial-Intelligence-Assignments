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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFoods = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhosts = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        evalFunc = 0
        minFudDis = 10000

        #evaluation function calculation dependent on food distance,
    	#scared times, distance to the ghosts, currentscore

        if not action == 'Stop':
        	for fud in newFoods:
        		dis = manhattanDistance(newPos,fud)
        		if dis <= minFudDis:
        			minFudDis = dis
        else: minFudDis = 0

        for ghost in newGhostStates:
        	if not ghost.scaredTimer == 0:
        		evalFunc = evalFunc - 0.4 * manhattanDistance(newPos,ghost.getPosition())
        	else: 
        		if manhattanDistance(newPos,ghost.getPosition()) < 5:
        			evalFunc = evalFunc + 0.3 * manhattanDistance(newPos,ghost.getPosition())

        if not minFudDis == 0:
        	evalFunc = evalFunc + 1/minFudDis

        evalFunc = evalFunc + 0.2*successorGameState.getScore()
        
        return evalFunc



def scoreEvaluationFunction(currentGameState):
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

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        v = -100000
        act = ''
        #final maximisation in the minimax algorithm
        #returns the result
        for action in gameState.getLegalActions(0):
        	succ = gameState.generateSuccessor(0, action)
        	if self.min_max(succ,action,self.depth,1) > v:
        		v = self.min_max(succ,action,self.depth,1)
        		act = action
        return act

    """
		Main logic of minimax algorithm
    """
    def min_max(self,gameState,act,depth,i):
    	if depth == 0:
    		return self.evaluationFunction(gameState)
    	if len(gameState.getLegalActions(i))==0:
    		return self.evaluationFunction(gameState)
    	#if the agent is pacman, maximise
    	if i == 0:
    		v = -1000
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.min_max(succGameState,action,depth,1) == None:
        			mm = self.min_max(succGameState,action,depth,1)
        		else: mm = v
        		if mm > v:
        			v = mm     		
        	return v
        #if the agent is ghost, minimise
        #if the agent is last ghost, go deeper in depth
        else:
        	if not i == gameState.getNumAgents()-1:
        		nn = i+1
        	else: 
        		depth = depth - 1
        		nn = 0
    		v = 1000
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.min_max(succGameState,action,depth,nn) == None:
        			mm = self.min_max(succGameState,action,depth,nn)
        		else: mm = v
        		if mm < v:
        			v = mm
        	return v




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        v = -100000
        act = ''
        a = -1000
        b = 1000
        #final maximisation with alpha beta pruning in the minimax algorithm
        #returns the result
        for action in gameState.getLegalActions(0):
        	succ = gameState.generateSuccessor(0, action)
        	if self.min_max(succ,action,self.depth,a,b,1) > v:
        		v = self.min_max(succ,action,self.depth,a,b,1)
        		a = max (a, v)
        		act = action
        return act

    """
		Main logic of alpha beta pruning minimax algorithm
    """
    def min_max(self,gameState,act,depth,a,b,i):
    	if depth == 0:
    		return self.evaluationFunction(gameState)
    	if len(gameState.getLegalActions(i))==0:
    		return self.evaluationFunction(gameState)
    	#if the agent is pacman, maximise
    	#apply alpha-beta pruning
    	if i == 0:
    		v = -1000
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.min_max(succGameState,action,depth,a,b,1) == None:
        			mm = self.min_max(succGameState,action,depth,a,b,1)
        		else: mm = v
        		if mm > v:
        			v = mm
        		a = max (a, v) 
        		if b < a:
        			return v
        	return v
        #if the agent is ghost, minimise
        #if the agent is last ghost, go deeper in depth
        #apply alpha-beta pruning
        else:
        	if not i == gameState.getNumAgents()-1:
        		nn = i+1
        	else: 
        		depth = depth - 1
        		nn = 0
    		v = 1000
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.min_max(succGameState,action,depth,a,b,nn) == None:
        			mm = self.min_max(succGameState,action,depth,a,b,nn)
        		else: mm = v
        		if mm < v:
        			v = mm
        		b = min (b, v)
        		if b < a:
        			return v
        	return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        
        v = -100000
        act = ''
        #final maximisation in the expectimax algorithm
        #returns the result
        for action in gameState.getLegalActions(0):
        	succ = gameState.generateSuccessor(0, action)
        	if self.ex_max(succ,action,self.depth,1) > v:
        		v = self.ex_max(succ,action,self.depth,1)
        		act = action
        return act

    """
		Main logic of expectimax algorithm
    """
    def ex_max(self,gameState,act,depth,i):
    	if depth == 0:
    		return self.evaluationFunction(gameState)
    	if len(gameState.getLegalActions(i))==0:
    		return self.evaluationFunction(gameState)
    	#if the agent is pacman, maximise
    	if i == 0:
    		v = -1000
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.ex_max(succGameState,action,depth,1) == None:
        			mm = self.ex_max(succGameState,action,depth,1)
        		else: mm = v
        		if mm > v:
        			v = mm       		
        	return v
        #if the agent is ghost, calculate expected utilities
        #if the agent is last ghost, go deeper in depth
        else:
        	if not i == gameState.getNumAgents()-1:
        		nn = i+1
        	else: 
        		depth = depth - 1
        		nn = 0
    		v = 0
    		for action in gameState.getLegalActions(i):
        		succGameState = gameState.generateSuccessor(i, action)
        		if not self.ex_max(succGameState,action,depth,nn) == None:
        			mm = self.ex_max(succGameState,action,depth,nn)
        		else: mm = v
        		p = mm/len(gameState.getLegalActions(i))
        		v = v + p
        	return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    evalFunc = 0
    minFudDis = 10000
    minGhostDis = 10000

    #evaluation function calculation dependent on food distance,
    #scared times, distance to the ghosts, currentscore

    for fud in foods:
    	dis = manhattanDistance(pos,fud)
    	if dis <= minFudDis:
    		minFudDis = dis

    for ghost in ghostStates:
    	if not ghost.scaredTimer == 0:
    		evalFunc = evalFunc - 2.4 * manhattanDistance(pos,ghost.getPosition())
    	else:
    		if manhattanDistance(pos,ghost.getPosition()) < 4:
    			evalFunc = evalFunc + 1.2 * manhattanDistance(pos,ghost.getPosition())
    		else:
    			evalFunc = evalFunc - 0.2 * manhattanDistance(pos,ghost.getPosition())

    if not minFudDis == 0:
    	evalFunc = evalFunc + 1/minFudDis

    evalFunc = evalFunc + 0.2*currentGameState.getScore()

    return evalFunc


# Abbreviation
better = betterEvaluationFunction

