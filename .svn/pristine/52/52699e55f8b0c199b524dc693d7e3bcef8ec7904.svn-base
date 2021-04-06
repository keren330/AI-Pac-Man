# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    iter = 0
    while iter < iterations:
      # maxQ = -float("inf")
      values = util.Counter()
      states = mdp.getStates()      
      for one_state in states:
        qList = []
        actions = mdp.getPossibleActions(one_state)
        for one_action in actions:
          Q = self.getQValue(one_state, one_action)
          qList.append(Q)
        if len(qList) != 0:
          values[one_state] = max(qList)
      
      self.values = values
      iter += 1

    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    Q = 0
    # qState returns list of (nextState, prob) pairs
    qState = self.mdp.getTransitionStatesAndProbs(state, action)
    for nextState, prob in qState:
      rewards = self.mdp.getReward(state, action, nextState)
      discount = self.discount
      nextValue = self.values[nextState]
      Q = Q + prob * (rewards + discount * nextValue)
    return Q


  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    if self.mdp.isTerminal(state) == True:
      return None

    maxQ = -float('inf')
    actions = self.mdp.getPossibleActions(state)
    for one_action in actions:
      qValue = self.getQValue(state, one_action)
      if qValue > maxQ:
        maxQ = qValue
        best_action = one_action

    return best_action

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
