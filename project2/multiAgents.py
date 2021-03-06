# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    newFood_list = successorGameState.getFood().asList()
    lowest_distance = float("inf")
    for food in newFood_list:
      lowest_distance = min(lowest_distance, manhattanDistance(newPos, food))
      #successorGameState.getScore() = successorGameState.getScore() + 1.0/lowest_distance
    newGhostPositions = successorGameState.getGhostPositions()
    die = -float("inf")
    for ghost in newGhostPositions:
      #closet_distance = min(closet_distance, manhattanDistance(newPos,ghost))
      if (manhattanDistance(newPos, ghost) < 2):
        return die
         # successorGameState.getScore() = successorGameState.getScore() + 1.0/closet_distance
    return successorGameState.getScore() + 1.0/lowest_distance


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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def value(gameState, agentIndex, depth):
      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)
      if agentIndex == 0:
        depth = depth + 1
        return maxValue(gameState, agentIndex, depth)
      elif agentIndex >= 1:
        return minValue(gameState, agentIndex, depth)

    def maxValue(gameState, agentIndex, depth):
      depth = depth + 1
      value = float('-inf')
      agentIndex = 0 # pacman is moving

      # check the current state is win or lose or the depth is reaching the input depth
      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(agentIndex)      
      for n in actions:
        nextSuccessor = gameState.generateSuccessor(agentIndex, n) # generatePacmanSuccessor will return a state
        minV = minValue(nextSuccessor, agentIndex + 1,  depth)
        value = max(value, minV)
      return value
      
    # check states of every ghost
    def minValue(gameState, agentIndex, depth):

      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState) 

      value = float('inf')
      
      for n in gameState.getLegalActions(agentIndex):
        numAgents = gameState.getNumAgents()
        # if agent is ghost
        if agentIndex < numAgents - 1:
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          nextMinV = minValue(nextSuccessor, agentIndex + 1, depth)
          value = min(value, nextMinV)
        # pacman is the last one to move: if numAgents is 1, it is the pacman
        elif agentIndex == numAgents - 1:
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          maxV = maxValue(nextSuccessor, agentIndex, depth)
          value = min(value, maxV)
      return value

    agentIndex = 0 # pacman
    actions = gameState.getLegalActions(agentIndex)
    value = float("-inf")
    for n in actions:
      depth = 0
      nextSuccessor = gameState.generateSuccessor(agentIndex, n)
      score = minValue(nextSuccessor, agentIndex + 1, depth)
      if score > value:
        value = score
        bestAction = n
    return bestAction

    # util.raiseNotDefined()
    
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    alpha = float("-inf")
    beta = float("inf")

    def maxValue(gameState, agentIndex, depth, alpha, beta):
      value = float("-inf")
      agentIndex = 0
      depth = depth + 1

      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)

      for n in actions:
        nextSuccessor = gameState.generateSuccessor(agentIndex, n)
        minV = minValue(nextSuccessor, agentIndex + 1, depth, alpha, beta)
        value = max(value, minV)
        alpha = max(alpha, value)
        if alpha >= beta: 
          return value
      return value

    def minValue(gameState, agentIndex, depth, alpha, beta):
      value = float("inf")

      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)

      for n in gameState.getLegalActions(agentIndex):
        
        numAgents = gameState.getNumAgents()
        if agentIndex == numAgents - 1:
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          maxV = maxValue(nextSuccessor, agentIndex, depth, alpha, beta)
          value = min(value, maxV)
          beta = min(beta, value)
          if alpha >= beta:
            return value
        else:
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          minV = minValue(nextSuccessor, agentIndex + 1, depth, alpha, beta)
          value = min(value, minV)
          beta = min(beta, value)
          if alpha >= beta:
            return value
      return value
    
    value = float('-inf')
    agentIndex = 0
    actions = gameState.getLegalActions(agentIndex)
    for n in actions:
      depth = 0
      nextSuccessor = gameState.generateSuccessor(agentIndex, n)
      score = minValue(nextSuccessor, agentIndex + 1, depth, alpha, beta)
      if score > value:
        value = score
        bestAction = n
    return bestAction

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
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    def value(gameState, agentIndex, depth):
      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)
      if agentIndex == 0:
        depth = depth + 1
        return maxValue(gameState, agentIndex, depth)
      elif agentIndex >= 1:
        return expValue(gameState, agentIndex, depth)

    def maxValue(gameState, agentIndex, depth):
      depth = depth + 1
      value = float('-inf')
      agentIndex = 0 # pacman is moving

      # check the current state is win or lose or the depth is reaching the input depth
      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(agentIndex)      
      for n in actions:
        nextSuccessor = gameState.generateSuccessor(agentIndex, n) # generatePacmanSuccessor will return a state
        minV = expValue(nextSuccessor, agentIndex + 1,  depth)
        value = max(value, minV)
      return value
      
    # check states of every ghost
    def expValue(gameState, agentIndex, depth):

      if depth == self.depth or gameState.isWin() == True or gameState.isLose() == True:
        return self.evaluationFunction(gameState) 

      value = 0     
      for n in gameState.getLegalActions(agentIndex):
        numAgents = gameState.getNumAgents()
        p = 1.0/len(n)
        # if agent is ghost
        if agentIndex < numAgents - 1:         
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          expV = expValue(nextSuccessor, agentIndex + 1, depth)
          value = value + p * expV
        # pacman is the last one to move: if numAgents is 1, it is the pacman
        elif agentIndex == numAgents - 1:
          nextSuccessor = gameState.generateSuccessor(agentIndex, n)
          maxV = maxValue(nextSuccessor, agentIndex, depth)
          value = value + p * maxV
      return value

    agentIndex = 0 # pacman
    bestAction = " "
    actions = gameState.getLegalActions(agentIndex)
    value = float("-inf")
    for n in actions:
      depth = 0
      nextSuccessor = gameState.generateSuccessor(agentIndex, n)
      score = expValue(nextSuccessor, agentIndex + 1, depth)
      if score > value:
        value = score
        bestAction = n
    return bestAction
    



import math
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  # util.raiseNotDefined()
  newPos = currentGameState.getPacmanPosition()
  newFood_List = currentGameState.getFood().asList()

  lowest_distance = float('inf')
  for food in newFood_List:
    lowest_distance  = min(lowest_distance, manhattanDistance(newPos, food))

  ghostDist = 0
  die = -float("inf")
  newGhostPositions = currentGameState.getGhostPositions()
  for ghost in newGhostPositions:
    ghostDist = manhattanDistance(newPos, ghost)
    if (ghostDist < 2):
      return die

  food_numbers = currentGameState.getNumFood()
  caps_numbers = len(currentGameState.getCapsules())

  additionalscore = 0
  if currentGameState.isLose():
    additionalscore -= 50000
  elif currentGameState.isWin():
      additionalscore += 50000

  try:
    next
  except Exception:
    pass
  return 1.0/(food_numbers + 1) * 95005 + ghostDist + \
           1.0/(lowest_distance + 1) * 95 + \
           1.0/(caps_numbers + 1) * 1000 + additionalscore

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

