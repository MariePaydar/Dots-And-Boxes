from collections import deque
from copy import deepcopy
import random 

class Ai:

    def __init__(self, shape):
        self.num = 0
        self.shape = shape
        self.X = shape[0]
        self.Y = shape[1]
        self.depth = 3

    def generateVectors(self,connectedVectors):
        vectors = deque()
        for x in range(self.X):
            for y in range(self.Y):
                if x < self.X - 1 and ((x, y), (x + 1, y)) not in connectedVectors:
                    vectors.append(((x, y), (x + 1, y)))
                if y < self.Y - 1 and ((x, y), (x, y + 1)) not in connectedVectors:
                    vectors.append(((x, y), (x, y + 1)))
        return vectors
                

    def evaluationFunction(self,state, move):
        if move == None:
            return 0
        h = 0
        L,R = move
        if L[1] == R[1]:
            if (L,(L[0],L[1]+1)) in state.connectedVectors or ((L[0],L[1]+1),L) in state.connectedVectors:
                if (R,(R[0],R[1]+1)) in state.connectedVectors or ((R[0],R[1]+1),R) in state.connectedVectors:
                    if ((L[0],L[1]+1),(R[0],R[1]+1)) in state.connectedVectors or ((R[0],R[1]+1),(L[0],L[1]+1)) in state.connectedVectors:
                        h = h + 1
            if (L,(L[0],L[1]-1)) in state.connectedVectors or ((L[0],L[1]-1),L) in state.connectedVectors:
                if (R,(R[0],R[1]-1)) in state.connectedVectors or ((R[0],R[1]-1),R) in state.connectedVectors:
                    if ((L[0],L[1]-1),(R[0],R[1]-1)) in state.connectedVectors or ((R[0],R[1]-1),(L[0],L[1]-1)) in state.connectedVectors:
                        h = h + 1
        else:
            if (L,(L[0]+1,L[1])) in state.connectedVectors or ((L[0]+1,L[1]),L) in state.connectedVectors:
                if (R,(R[0]+1,R[1])) in state.connectedVectors or ((R[0]+1,R[1]),R) in state.connectedVectors:
                    if ((L[0]+1,L[1]),(R[0]+1,R[1])) in state.connectedVectors or ((R[0]+1,R[1]),(L[0]+1,L[1])) in state.connectedVectors:
                        h = h + 1
            if (L,(L[0]-1,L[1])) in state.connectedVectors or ((L[0]-1,L[1]),L) in state.connectedVectors:
                if (R,(R[0]-1,R[1])) in state.connectedVectors or ((R[0]-1,R[1]),R) in state.connectedVectors:
                    if ((L[0]-1,L[1]),(R[0]-1,R[1])) in state.connectedVectors or ((R[0]-1,R[1]),(L[0]-1,L[1])) in state.connectedVectors:
                        h = h + 1
        return h
    
    def minimax(self, state, depth, ai_term):

        bestMove = (0,None)

        if depth == 0 or len(state.openVectors) == 0:
            h = self.evaluationFunction(state,None)
            return (h, None)
        
        for i in range(len(state.openVectors)):

            move = state.openVectors.pop()

            stateCopy = deepcopy(state)
            stateCopy.move(move)

            state.openVectors.appendleft(move)

            h = self.evaluationFunction(stateCopy,move)
            
            if ai_term:
                stateCopy.aiScore = stateCopy.aiScore + h
            else:
                stateCopy.playerScore = stateCopy.playerScore + h

            if(h>0):
                nextMove = self.minimax(stateCopy, depth - 1, ai_term)
                if ai_term:
                    stateCopy.aiScore = nextMove[0] + stateCopy.aiScore
                else:
                    stateCopy.playerScore = nextMove[0] + stateCopy.playerScore
            else:
                nextMove = self.minimax(stateCopy, depth - 1, not ai_term)
                if ai_term:
                    stateCopy.aiScore = stateCopy.aiScore - nextMove[0]
                else:
                    stateCopy.playerScore = stateCopy.playerScore - nextMove[0] 

            if ai_term:
                if stateCopy.aiScore >= bestMove[0]:
                    bestMove = (stateCopy.aiScore, move)
                if stateCopy.aiScore >= depth:
                    bestMove = (stateCopy.aiScore, move)
                    break
            else:
                if stateCopy.playerScore >= bestMove[0]:
                    bestMove = (stateCopy.playerScore, move)
                if stateCopy.playerScore >= depth:
                    bestMove = (stateCopy.playerScore, move)
                    break

        return bestMove
        
    def decide(self, connectedVectors):
            
        openVectors = self.generateVectors(connectedVectors)

        state = State(connectedVectors, openVectors, self.X, self.Y)
        
        _ , move = self.minimax(state, self.depth, True)

        if move == None:
            return random.choice(openVectors)
        return move

class State:
    def __init__(self, connectedV, openV, x, y):
        self.playerScore = 0
        self.aiScore = 0
        self.x = x
        self.y = y
        self.openVectors = openV
        self.connectedVectors = connectedV
    
    def move(self, vector):
        self.connectedVectors.append(vector)
        