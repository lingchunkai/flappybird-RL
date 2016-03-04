import numpy as np
import math
import random 
import itertools

class FB_GS:
    def __init__(self, playerX, playerY, velX, playerVelY, upperPipes, lowerPipes):
        self.playerX = playerX
        self.playerY = playerY
        self.velX = velX
        self.playerVelY = playerVelY
        self.upperPipes = list(upperPipes)
        self.lowerPipes = list(lowerPipes)

    def GetCondensedRep(self):
        '''
        Only cares about the location of immediate next pipe, and not those that follow

        ADDITIONAL ASSUMPTIONS:
        velX is assumed to be temporally constant
        Pipe gap size is assumed to be temporally constant 
        '''

        # Assume x distance to next pipe is the same for upper/lower
        distanceToNextPipeX = self.playerX - min(self.lowerPipes[0]['x'], self.upperPipes[0]['x'])
        distanceToTopY = self.playerY - self.upperPipes[0]['y']
        distanceToGround = self.playerY

        return (distanceToNextPipeX, distanceToTopY, distanceToGround, self.playerVelY)

    def GetMarkovRep(self, action):
        '''
        NOTES
        This representation is not expected to perform well - it only tries to cross the immediate next pipe        
        Also, using of relative position reduces |S| but does not prepare well for next position
        '''
        
        return self.GetCondensedRep() + (1 if action == True else 0, )
   
    @staticmethod
    def InitCoarseRep():
        '''
        '''    
        # INTERVAL_X_START = np.concatenate((np.array([-float('inf')]), np.arange(-100.0, 10.0, 20.0)))
        # INTERVAL_X_END = np.concatenate((np.arange(-55.0, 55.0, 20.0), np.array([float('inf')])))

        INTERVAL_Y_TOP_PIPE_START = np.concatenate((np.array([-float('inf')]), np.arange(-150.0, 10.0, 20.0)))
        INTERVAL_Y_TOP_PIPE_END = np.concatenate((np.arange(-105.0, 55.0, 20.0), np.array([float('inf')])))
 
        INTERVAL_Y_GROUND_START = np.concatenate((np.array([-float('inf')]), np.arange(0.0, 200.0, 20.0)))
        INTERVAL_Y_GROUND_END = np.concatenate((np.arange(45.0, 245.0, 20.0), np.array([float('inf')])))
       
        VELOCITY_Y_START = np.concatenate((np.array([-float('inf')]), np.arange(-10, 8, 1)))
        VELOCITY_Y_END = np.concatenate((np.arange(-7, 11, 1), np.array([float('inf')])))

        # INTERVAL_X = zip(INTERVAL_X_START, INTERVAL_X_END)
        # INTERVAL_Y_TOP = zip(INTERVAL_Y_TOP_PIPE_START, INTERVAL_Y_TOP_PIPE_START)
        INTERVAL_Y_GROUND = zip(INTERVAL_Y_GROUND_START, INTERVAL_Y_GROUND_END)
        VELOCITY_Y = zip(VELOCITY_Y_START, VELOCITY_Y_END)
        ACTIONS = [False, True]
        
        # FB_GS.COARSE_STATES = list(itertools.product(INTERVAL_X, INTERVAL_Y_TOP, INTERVAL_Y_GROUND, VELOCITY_Y, ACTIONS))
        FB_GS.COARSE_STATES = list(itertools.product(INTERVAL_Y_GROUND, VELOCITY_Y, ACTIONS))
        # for i in COARSE_STATES: print i
        # print len(COARSE_STATES) 
   
    def GetMarkovCoarseRep(self, action):
        '''
        Coarse (overlapping) representation. 
        
        Regular intervals in the x and y directions, with some overlaps. 
        Action is entirely separate dimension on the hypercube, no overlaps obviously
        '''

        vec = np.zeros((len(FB_GS.COARSE_STATES),))

        (distanceToNextPipeX, distanceToTopY, distanceToGround, playerVelY) = self.GetCondensedRep()
        
        # for (i, (INTV_X, INTV_Y_TOP, iNTV_Y_GROUND, INTV_VEL_Y, ACTION)) in enumerate(FB_GS.COARSE_STATES):
        #    if (distanceToNextPipeX <= INTV_X[1]) and (distanceToNextPipeX > INTV_X[0]) \
        #    and (distanceToTopY <= INTV_Y_TOP[1]) and (distanceToTopY > INTV_Y_TOP[0]) \
        #    and (distanceToGround <= INTV_Y_GROUND[1]) and (distanceToGround > INTV_Y_GROUND[0]) \
        #    and (playerVelY <= INTV_VEL_Y[1]) and (playerVelY > INTV_VEL_Y[0]) \
        #    and (action == ACTION):
        #        vec[i] = 1.0
         
        
        #for (i, (INTV_X, INTV_Y_TOP, iNTV_Y_GROUND, INTV_VEL_Y, ACTION)) in enumerate(FB_GS.COARSE_STATES):
        
        for (i, (INTV_Y_GROUND, INTV_VEL_Y, ACTION)) in enumerate(FB_GS.COARSE_STATES):
            if (distanceToGround <= INTV_Y_GROUND[1]) and (distanceToGround > INTV_Y_GROUND[0]) \
            and (playerVelY <= INTV_VEL_Y[1]) and (playerVelY > INTV_VEL_Y[0]) \
            and (action == ACTION):
                vec[i] = 1.0
      
        # vec = vec/np.sum(vec)
        return vec

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

    def RestartEpisode(self):
        # Inform agent that the current episode is over
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

    def RestartEpisode(self):
        # Inform agent that the current episode is over
        pass

class FB_MarkovAIBase:
    # Selects actions by pure epsilon optimal linear value function approximation
    # Markov state is formed by (distanceToNextPipeX, distanceToTopY, self.playerVelY)
    # i.e. the state action space is given by [Markov State, action]

    def __init__(self, epsilon, lamb, gamma, alpha, fnMarkovRep):
        # Serve 
        self.epsilon = epsilon
        self.lamb = lamb
        self.gamma = gamma 
        self.alpha = alpha
        self.GetMarkovRep = fnMarkovRep
        self.RestartEpisode()
    
    def MakeMove(self, gs):
        if random.random() < self.epsilon:
            if random.randint(1,2) == 1: actionChosen = True
            else: actionChosen = False
        else:
            # Select best action according to q values
            bestAction, bestQVal = max(enumerate([self.GetMarkovRep(gs,action) for action in [0,1]]), key=lambda p: np.dot(self.weights, p[1]))
            # bestStateAction = markovState + (bestAction == 1, )
            actionChosen = (bestAction == 1)
        return actionChosen
    
    def Reinforce(self, prev_gs, action, next_gs, feedback):
        # Receive the next state and reward feeback
     
        # Current state action pair
        prevMarkovStateAction = self.GetMarkovRep(prev_gs, action) 
        # Update eligibility trace   
        self.eligibilityTrace = self.gamma * self.lamb * self.eligibilityTrace +  prevMarkovStateAction

        # Compute epsilon greedy move
        nextAction = self.MakeMove(next_gs)
        nextMarkovStateAction = self.GetMarkovRep(next_gs, action)        
        
        # Compute error signal
        delta = feedback + self.gamma * (np.dot(self.weights, nextMarkovStateAction)) - np.dot(self.weights, prevMarkovStateAction)
        
        # Update weights according to learning rate
        self.weights += delta * self.eligibilityTrace * self.alpha

        #print delta, self.eligibilityTrace, self.weights
        # raw_input()
        
    def RestartEpisode(self):
        # Inform agent that the current episode is over and to start a new one
        self.eligibilityTrace = np.zeros(self.weights.shape)
        pass

class FB_SimpleMarkovAI(FB_MarkovAIBase):
    def __init__(self, epsilon, lamb, gamma, alpha):
        self.weights = np.zeros(4+1)
        FB_MarkovAIBase.__init__(self, epsilon, lamb, gamma, alpha, FB_GS.GetMarkovRep)

class FB_SimpleCoarseMarkovAI(FB_MarkovAIBase):
    def __init__(self, epsilon, lamb, gamma, alpha):
        FB_GS.InitCoarseRep()
        self.weights = np.zeros(len(FB_GS.COARSE_STATES))
        FB_MarkovAIBase.__init__(self, epsilon, lamb, gamma, alpha, FB_GS.GetMarkovCoarseRep)

if __name__ == '__main__':
    FB_GS.InitCoarseRep()
