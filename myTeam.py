from pacai.agents.capture.capture import CaptureAgent

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = DefensiveAgent
    secondAgent = OffensiveAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

# Copied over from pacai/agents/capture/dummy.py
class OffensiveAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.
        self.food = self.getFood(gameState).asList()
    
    def getSuccessor(self, gameState, action):
        return gameState.generateSuccessor(self.index, action)

    def evaluateState(self, successor, action):
        """
        Evaluates a state based on proximity to food and ghosts.
        """
        myPos = successor.getAgentState(self.index).getPosition()
        foodList = self.getFood(successor).asList()
        ghostStates = self.getOpponents(successor)
        ghostPositions = [successor.getAgentState(ghost).getPosition()
                          for ghost in ghostStates if not successor.getAgentState(ghost).isPacman]

        # Nearest food
        foodDist = min([self.getMazeDistance(myPos, food) for food in foodList], default=1)
        # Nearest ghost
        ghostDist = min([self.getMazeDistance(myPos, ghost)
                         for ghost in ghostPositions], default=float('inf'))

        # Heuristics:
        # Penalty if staying still
        stayPenalty = -5 if action == 'Stop' else 0

        # prioritize food + avoid ghosts + penalty
        return -foodDist + (5 if ghostDist > 3 else -20) + stayPenalty

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        bestAction = None
        maxScore = float('-inf')

        foodList = self.getFood(gameState).asList()

        # Prioritize consuming food if adjacent
        for action in actions:
            successor = self.getSuccessor(gameState, action)
            successorPos = successor.getAgentState(self.index).getPosition()

            if successorPos in foodList:  # Immediate food consumption
                return action

        # Otherwise, evaluate states as usual
        for action in actions:
            successor = self.getSuccessor(gameState, action)
            score = self.evaluateState(successor, action)
            if score > maxScore:
                maxScore = score
                bestAction = action

        return bestAction

# Copied over from pacai/agents/capture/dummy.py
class DefensiveAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.
        self.food = self.getFood(gameState).asList()
    
    def getSuccessor(self, gameState, action):
        return gameState.generateSuccessor(self.index, action)

    def evaluateState(self, successor):
        """
        Evaluates the state based on proximity to opponents and food.
        """
        myPos = successor.getAgentState(self.index).getPosition()
        opponentStates = [successor.getAgentState(opponent)
                          for opponent in self.getOpponents(successor)]
        pacmanPositions = [opponent.getPosition()
                           for opponent in opponentStates
                           if opponent.isPacman and opponent.getPosition()]

        # Chase enemy Pacman
        if pacmanPositions:
            pacmanDist = min([self.getMazeDistance(myPos, pacman)
                              for pacman in pacmanPositions], default=1)
            return -1.5 * pacmanDist

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        bestAction = None
        maxScore = float('-inf')

        opponents = [gameState.getAgentState(opponent) for opponent in self.getOpponents(gameState)]
        pacmanPositions = [opponent.getPosition()
                           for opponent in opponents
                           if opponent.isPacman and opponent.getPosition()]

        # Prioritize capturing enemy Pacman if adjacent
        for action in actions:
            successor = self.getSuccessor(gameState, action)
            successorPos = successor.getAgentState(self.index).getPosition()

            if successorPos in pacmanPositions:  # Immediate capture
                return action

        # Otherwise, evaluate states as usual
        for action in actions:
            successor = self.getSuccessor(gameState, action)
            score = self.evaluateState(successor)
            if score > maxScore:
                maxScore = score
                bestAction = action

        return bestAction