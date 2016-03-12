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

        # Get nearest pipe to right of player
        (smallestD, bestK) = (-1000, 0)
        
        for k in xrange(len(self.lowerPipes)):
            d = self.playerX - self.lowerPipes[k]['x']
            if d > smallestD and d < 50:
                smallestD = d
                bestK = k

        # Assume x distance to next pipe is the same for upper/lower
        distanceToNextPipeX = self.playerX - min(self.lowerPipes[bestK]['x'], self.upperPipes[bestK]['x'])
        distanceToBottomY = self.playerY - self.lowerPipes[bestK]['y']

        return (distanceToNextPipeX, distanceToBottomY, self.playerVelY)

    def GetMarkovStateActionRep(self, action):
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
        #INTERVAL_X_START = np.concatenate((np.array([-float('inf')]), np.arange(-120.0, 10.0, 5.0)))
        #INTERVAL_X_END = np.concatenate((np.arange(-120.0, 10.0, 5.0), np.array([float('inf')])))

        INTERVAL_X_START = np.array([-float('inf')])
        INTERVAL_X_END = np.array([float('inf')])
        
        INTERVAL_Y_BOTTOM_PIPE_START = np.concatenate((np.array([-float('inf')]), np.arange(-150.0, 150.0, 4.0)))
        INTERVAL_Y_BOTTOM_PIPE_END = np.concatenate((np.arange(-150.0, 150.0, 4.0), np.array([float('inf')])))

        VELOCITY_Y_START = np.concatenate((np.array([-float('inf')]), np.arange(-10, 10, 2)))
        VELOCITY_Y_END = np.concatenate((np.arange(-10, 10, 2), np.array([float('inf')])))

        INTERVAL_X = zip(INTERVAL_X_START, INTERVAL_X_END)
        INTERVAL_Y_BOTTOM_PIPE = zip(INTERVAL_Y_BOTTOM_PIPE_START, INTERVAL_Y_BOTTOM_PIPE_END)
        VELOCITY_Y = zip(VELOCITY_Y_START, VELOCITY_Y_END)
        ACTIONS = [False, True]
        
        FB_GS.COARSE_STATES_ACTION = list(itertools.product(INTERVAL_X, INTERVAL_Y_BOTTOM_PIPE, VELOCITY_Y, ACTIONS))
        FB_GS.COARSE_STATES = list(itertools.product(INTERVAL_X, INTERVAL_Y_BOTTOM_PIPE, VELOCITY_Y))

        #FB_GS.STATE_CACHE = dict()
        #FB_GS.STATE_ACTION_CACHE = dict()

    def GetMarkovCoarseStateRep(self):
        
        vec = np.zeros((len(FB_GS.COARSE_STATES),))

        (distanceToNextPipeX, distanceToBottomY, playerVelY) = self.GetCondensedRep()
        #if (distanceToNextPipeX, distanceToBottomY, playerVelY) in FB_GS.STATE_CACHE:
        #    print "OK"
        #    return FB_GS.STATE_CACHE[(distanceToNextPipeX, distanceToBottomY, playerVelY)]

        for (i, (INTV_X, INTV_Y_BOT_PIPE, INTV_VEL_Y)) in enumerate(FB_GS.COARSE_STATES):
            if (distanceToBottomY <= INTV_Y_BOT_PIPE[1]) and (distanceToBottomY > INTV_Y_BOT_PIPE[0]) \
            and (playerVelY <= INTV_VEL_Y[1]) and (playerVelY > INTV_VEL_Y[0]) \
            and (distanceToNextPipeX <= INTV_X[1]) and (distanceToNextPipeX > INTV_X[0]):
                vec[i] = 1.0
        #print np.sum(vec)
        vec = vec/np.sum(vec)
       
        #FB_GS.STATE_CACHE[(distanceToNextPipeX, distanceToBottomY, playerVelY)] = vec
        #print len(FB_GS.STATE_CACHE)
        return vec
    
    def GetMarkovCoarseStateActionRep(self, action):
        '''
        Coarse (overlapping) representation. 
        
        Regular intervals in the x and y directions, with some overlaps. 
        Action is entirely separate dimension on the hypercube, no overlaps obviously
        '''

        vec = np.zeros((len(FB_GS.COARSE_STATES_ACTION),))

        (distanceToNextPipeX, distanceToBottomY, playerVelY) = self.GetCondensedRep()
        #if (distanceToNextPipeX, distanceToBottomY, playerVelY, action) in FB_GS.STATE_ACTION_CACHE:
        #    print "OK"
        #    return FB_GS.STATE_ACTION_CACHE[(distanceToNextPipeX, distanceToBottomY, playerVelY, action)]        

        for (i, (INTV_X, INTV_Y_BOT_PIPE, INTV_VEL_Y, ACTION)) in enumerate(FB_GS.COARSE_STATES_ACTION):
            if (distanceToBottomY <= INTV_Y_BOT_PIPE[1]) and (distanceToBottomY > INTV_Y_BOT_PIPE[0]) \
            and (playerVelY <= INTV_VEL_Y[1]) and (playerVelY > INTV_VEL_Y[0]) \
            and (distanceToNextPipeX <= INTV_X[1]) and (distanceToNextPipeX > INTV_X[0]) \
            and (action == ACTION):
                vec[i] = 1.0
        
        print (distanceToNextPipeX, distanceToBottomY, playerVelY) 

        vec = vec/np.sum(vec)

        #FB_GS.STATE_ACTION_CACHE[(distanceToNextPipeX, distanceToBottomY, playerVelY, action)] = vec
        #print len(FB_GS.STATE_ACTION_CACHE)
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

    def __init__(self, fnEpsilon, lamb, gamma, fnAlpha, fnMarkovStateActionRep, fnMarkovStateRep, fnUpdateModel=None):
        # Serve 
        self.fnEpsilon = fnEpsilon
        self.lamb = lamb
        self.gamma = gamma 
        self.fnAlpha = fnAlpha
        self.GetMarkovStateActionRep = fnMarkovStateActionRep
        self.GetMarkovStateRep = fnMarkovStateRep
        self.UpdateModel = fnUpdateModel
        self.RestartEpisode()
    
    def MakeMove(self, gs):
        if random.random() < self.fnEpsilon(self, gs):
            if random.randint(1,2) == 1: actionChosen = True
            else: actionChosen = False
        else:
            # Select best action according to q values
            bestAction, bestQVal = max(enumerate([self.GetMarkovStateActionRep(gs,action) for action in [0,1]]), key=lambda p: np.dot(self.weights, p[1]))
            # bestStateAction = markovState + (bestAction == 1, )
            actionChosen = (bestAction == 1)
        return actionChosen
    
    def Reinforce(self, prev_gs, action, next_gs, feedback):
        # Receive the next state and reward feeback
     
        # Current state action pair
        prevMarkovStateAction = self.GetMarkovStateActionRep(prev_gs, action) 
        # Update eligibility trace   
        self.eligibilityTrace = self.gamma * self.lamb * self.eligibilityTrace +  prevMarkovStateAction        

        # Update counts/models if needed
        if self.UpdateModel: self.UpdateModel(self, prev_gs, action)

        if next_gs == 'TERMINAL' or next_gs == 0:
            predictedNextQ = 0
        else:
            # Compute epsilon greedy move
            nextAction = self.MakeMove(next_gs)
            nextMarkovStateAction = self.GetMarkovStateActionRep(next_gs, nextAction)
            predictedNextQ = np.dot(self.weights, nextMarkovStateAction)

        # Compute error signal
        delta = feedback + self.gamma * predictedNextQ - np.dot(self.weights, prevMarkovStateAction)
        
        # Update weights according to learning rate
        self.weights += delta * self.eligibilityTrace * self.fnAlpha(self, prev_gs, next_gs, action)

    def RestartEpisode(self):
        # Inform agent that the current episode is over and to start a new one
        self.eligibilityTrace = np.zeros(self.weights.shape)

    def QueryQAction(self, gs, action):
        stateAction = self.GetMarkovStateActionRep(gs, action)
        return np.dot(self.weights, stateAction)

    def QueryQBestAction(self, gs):
        return max(self.QueryQAction(gs, False), self.QueryQAction(gs, True))        

class FB_SimpleMarkovAI(FB_MarkovAIBase):
    def __init__(self, epsilon, lamb, gamma, alpha):
        self.weights = np.zeros(4+1)
        FB_MarkovAIBase.__init__(self, lambda ai,gs: epsilon, lamb, gamma, lambda ai, state, next_state, action: alpha, FB_GS.GetMarkovStateActionRep)

class FB_SimpleCoarseMarkovAI(FB_MarkovAIBase):
    def __init__(self, epsilon, lamb, gamma, alpha, initQ = 1000.0):
        if not hasattr(FB_SimpleCoarseMarkovAI, 'initialized'):
            FB_GS.InitCoarseRep()
            FB_SimpleCoarseMarkovAI.initialized = True
        self.weights = initQ * np.ones(len(FB_GS.COARSE_STATES_ACTION))
        FB_MarkovAIBase.__init__(self, lambda ai,gs: epsilon, lamb, gamma, lambda ai, state, next_state, action: alpha, FB_GS.GetMarkovCoarseStateActionRep, FB_GS.GetMarkovCoarseStateRep)

class FB_SimpleCoarseMarkovDecayE(FB_MarkovAIBase):
    def __init__(self, lamb, gamma, alpha, initQ = 1000.0, N0 = 10.0):
        if not FB_SimpleCoarseMarkovDecayE.initialized:
            FB_GS.InitCoarseRep()
            FB_SimpleCoarseMarkovDecayE.initialized = True
        self.weights = initQ * np.ones(len(FB_GS.COARSE_STATES_ACTION))
        self.visitCountState = np.zeros(len(FB_GS.COARSE_STATES))
        self.visitCountStateAction = np.zeros(len(FB_GS.COARSE_STATES_ACTION))
        self.N0 = N0
        FB_MarkovAIBase.__init__(self, FB_SimpleCoarseMarkovDecayE.GetEpsilon, lamb, gamma, lambda ai, state, next_state, action: alpha, FB_GS.GetMarkovCoarseStateActionRep, FB_GS.GetMarkovCoarseStateRep, FB_SimpleCoarseMarkovDecayE.UpdateCount)
    
    def GetEpsilon(self, gs):
        count = np.sum(self.visitCountState * self.GetMarkovStateRep(gs))
        eps = self.N0/(self.N0+count)
        print eps
        return self.N0/(self.N0+count)

    def UpdateCount(self, gs, action): 
        self.visitCountState += self.GetMarkovStateRep(gs)
        self.visitCountStateAction += self.GetMarkovStateActionRep(gs, action)

class FB_SimpleCoarseMarkovDecayEA(FB_MarkovAIBase):
    def __init__(self, lamb, gamma, initQ = 1000.0, N0 = 200.0, N1 = 0.001, A0 = 5.0, A1 = 0.001):
        if not hasattr(FB_SimpleCoarseMarkovDecayEA, 'initialized'):
            FB_GS.InitCoarseRep()
            FB_SimpleCoarseMarkovDecayEA.initialized = True
        self.weights = initQ * np.ones(len(FB_GS.COARSE_STATES_ACTION))
        self.visitCountState = np.zeros(len(FB_GS.COARSE_STATES))
        self.visitCountStateAction = np.zeros(len(FB_GS.COARSE_STATES_ACTION))
        self.N0 = N0
        self.A0 = A0
        self.A1 = A1
        self.N1 = N1
        FB_MarkovAIBase.__init__(self, FB_SimpleCoarseMarkovDecayEA.GetEpsilon, lamb, gamma, FB_SimpleCoarseMarkovDecayEA.GetAlpha, FB_GS.GetMarkovCoarseStateActionRep, FB_GS.GetMarkovCoarseStateRep, FB_SimpleCoarseMarkovDecayEA.UpdateCount)
    
    def GetAlpha(self, state, next_state,action):
        count = np.sum(self.visitCountStateAction * self.GetMarkovStateActionRep(state, action))
        alpha = 1.0/(self.A0+count*self.A1)
        print 'alpha', alpha
        return alpha        

    def GetEpsilon(self, gs):
        count = np.sum(self.visitCountState * self.GetMarkovStateRep(gs))
        eps = 1.0/(self.N0+self.N1*count)
        print 'eps', eps
        return eps

    def UpdateCount(self, gs, action): 
        self.visitCountState += self.GetMarkovStateRep(gs)
        self.visitCountStateAction += self.GetMarkovStateActionRep(gs, action)


if __name__ == '__main__':
    FB_GS.InitCoarseRep()
