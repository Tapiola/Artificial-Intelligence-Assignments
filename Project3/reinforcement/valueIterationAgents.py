# valueIterationAgents.py
# -----------------------
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
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 
        temp = util.Counter()

        #value iteration for k
        for k in range(0,iterations):
        	temp = self.values.copy()
        	for state in mdp.getStates():
        		actions = mdp.getPossibleActions(state)
        		#temporary dictionary for storing q-values
        		tempAct = util.Counter()
        		for action in actions:
        			states_transitions = mdp.getTransitionStatesAndProbs(state, action)
        			sumForAct = 0;
        			for a in states_transitions:
        				nextState = a[0]
        				transition = a[1]
        				reward = mdp.getReward(state, action, nextState)
        				#calculates q-value and maximises it later and assigns it to the value
        				sumForAct = sumForAct + transition*(reward + discount * temp[nextState])
        			tempAct[action] = sumForAct
        		self.values[state] = tempAct[tempAct.argMax()]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        
        #computes q-value for given state and action
        states_transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        sumForAct = 0;
        for a in states_transitions:
        	nextState = a[0]
        	transition = a[1]
        	reward = self.mdp.getReward(state, action, nextState)
        	sumForAct = sumForAct + transition*(reward + self.discount * self.getValue(nextState))
        return sumForAct

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        
        #computes the best policy for this state
        actions = self.mdp.getPossibleActions(state)
        temp = util.Counter()
        #tries every action and sums values for the states each brings us to
        for action in actions:
        	states_transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        	sumForAct = 0;
        	for a in states_transitions:
        		nextState = a[0]
        		transition = a[1]
        		reward = self.mdp.getReward(state, action, nextState)
        		sumForAct = sumForAct + transition*(reward + self.discount * self.getValue(nextState))
        	temp[action] = sumForAct;
        #gets the action for which the value is the largest
        return temp.argMax()




    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
