from player import Ai

state = [((0, 0), (1, 0)),((0, 0), (0, 1)),((0, 1), (0, 2)),((0, 2), (1, 2)),((0, 2), (0, 3)),((0, 3), (0, 4)),
         ((0, 4), (1, 4)),((1, 3), (2, 3)),((1, 0), (2, 0)),((2, 2), (2, 0))]
shape = (5,5)
agent = Ai(shape)
decide = agent.decide(state)
print("decided: ",decide)
