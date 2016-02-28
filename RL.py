import numpy as np
import random 

class FB_GS:
    def __init__(self, playerX, playerY, velX, playerVelY, upperPipes, lowerPipes):
        self.playerX = playerX
        self.playerY = playerY
        self.velX = velX
        self.playerVelY = playerVelY
        self.upperPipes = list(upperPipes)
        self.lowerPipes = list(lowerPipes)

    def GetMarkovRep(self):
        '''
        Only cares about the location of immediate next pipe, and not those that follow

        ADDITIONAL ASSUMPTIONS:
        velX is assumed to be temporally constant
        Pipe gap size is assumed to be temporally constant 
        
        NOTES
        This representation is not expected to perform well - it only tries to cross the immediate next pipe        
        Also, using of relative position reduces |S| but does not prepare well for next position
        '''

        # Assume x distance to next pipe is the same for upper/lower
        distanceToNextPipeX = self.playerX - min(self.lowerPipes[0]['x'], self.upperPipes[0]['x'])
        distanceToTopY = self.playerY - self.upperPipes[0]['y']

        return (distanceToNextPipeX, distanceToTopY, self.playerVelY)
        
class FB_AI:
    def __init__(self):

        # Initialize your RL code here      

        pass

    def MakeMove(self, gs):
        # Return agent's move based on whether he has flapped or not 
        pass

    def Reinforce(self, prev_gs, action,  next_gs, feedback):
        
        # Recieve the next state and reward feeback

        pass

class FB_Random_AI:
    def __init__(self, flapChance):

        # Initialize your RL code here      
        self.flapChance = flapChance

    def MakeMove(self, gs):
    
        # Return agent's move based on whether he has flapped or not 
        
        if random.random() <= self.flapChance:
            return True

        return False

    def Reinforce(self, prev_gs, action,  next_gs, feedback):
        
        # Recieve the next state and reward feeback

        pass


class FB_SimpleMarkovAI:
    # Selects actions by pure epsilon optimal
    def __init__(self):
        
        # Serve 

        pass
    
    def MakeMove(self, gs):
        
                

        pass
    
    def Reinforce(self, prev_gs, action,  next_gs, feedback):
        # Recieve the next state and reward feeback
        pass


