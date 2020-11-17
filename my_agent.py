from agent import Agent

class MyAgent(Agent):
    def act(self):
        Agent.act(self)
        print('my acted')