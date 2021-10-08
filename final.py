import random

class gameEnvironment:
    def __init__(self):
        self.representation = [[1,0,0,0,0],
                              [0,0,0,0,0],
                              [0,0,0,0,0],
                              [0,0,0,0,0],
                              [0,0,0,0,0]]

        self.rewardTable = [[0, 0,  0,  0,  0],
                            [20, 0,  0,  0,  0],
                            [30, 0,  0,  0,  0],
                            [50, 60, 70, 80, 90],
                            [40, 50,  0,   90,  100]]

    def setLocationToZero(self):
        for y in range(5):
            for x in range(5):
                if self.representation[y][x] == 1:
                    self.representation[y][x] = 0
        self.representation[0][0] = 1

    def changeLocation(self, length, width):
        for y in range(5):
            for x in range(5):
                if self.representation[y][x] == 1:
                    self.representation[y][x] = 0
        self.representation[length][width] = 1

    def checkFinal(self):
        if self.representation[4][4] == 1:
            return True
        else:
            return False

    def giveReward(self, length, width):
        return self.rewardTable[length][width]
        

class Agent:
    def __init__(self):
        self.reward = 0.0
        self.action = ['Up', 'Down', 'Left', 'Right']
        self.discountFactor = 0.8
        self.x = 0
        self.y = 0
        self.policy_table = [ [[0,0.5,0,0.5],   [0,1/3,1/3,1/3],     [0,1/3,1/3,1/3],        [0,1/3,1/3,1/3],        [0,0.5,0.5,0] ],
                            [ [1/3,1/3,0,1/3], [1/3,0,1/3,1/3],       [1/3,0,1/3,1/3],       [1/3,0,1/3,1/3],       [0.5,0,0.5,0] ],
                            [ [0.5,0.5,0,0],   [0,0,0,0],             [0,0,0,0],             [0,0,0,0],             [0,0,0,0]     ],
                            [ [1/3,1/3,0,1/3], [0,1/3,1/3,1/3],       [0,0,0.5,0.5],         [0,1/3,1/3,1/3],        [0,0.5,0.5,0] ],
                            [ [0.5,0,0,0.5],   [0.5,0,0.5,0],         [0,0,0,0],             [0.5,0,0,0.5],         [0,0,0,0] ]]
        self.locationXTable = []
        self.locationYTable = []
        self.rewardTable = []
        self.actionTable = []

    def reward(self):
        return self.reward

    def resetReward(self):
        self.reward = 0.0

    def resetLocationXTable(self):
        self.locationXTable = []

    def resetLocationYTable(self):
        self.locationYTable = []

    def resetRewardTable(self):
        self.rewardTable = []

    def resetActionTable(self):
        self.actionTable = []

    def start(self):
        self.x = 0
        self.y = 0

    def getLocation(self):
        return self.y, self.x

    def move(self, action, env: gameEnvironment):
        if action == "Up":
            self.y = self.y - 1
        elif action == "Down":
            self.y = self.y + 1
        elif action == "Left":
            self.x = self.x - 1
        elif action == "Right":
            self.x = self.x + 1
        env.changeLocation(self.y, self.x)

    def makeDecision(self):
        choice = random.choices(self.action, weights = self.policy_table[self.y][self.x], k = 1)
        return choice[0]

    def getReward(self, env: gameEnvironment):
        x = self.reward
        self.reward = self.discountFactor * (self.reward + env.giveReward(self.y,self.x))

    def observe(self):
        action = self.actionTable[0]
        actionIndex = 0
        if action == "Up":
            actionIndex = 0
        elif action == "Down":
            actionIndex = 1
        elif action == "Left":
            actionIndex = 2
        elif action == "Right":
            actionIndex = 3
        current_reward = self.rewardTable[0]
        if current_reward > 0:
            if self.policy_table[0][0][actionIndex] <= 0.98:
                self.policy_table[0][0][actionIndex] = self.policy_table[0][0][actionIndex] + 0.02
            a = 0
            count = 0
            for a in range(4):
                if (a != actionIndex and self.policy_table[0][0][a] >= 0.02):
                    count = count + 1
            for a in range(4):
                if (a != actionIndex and self.policy_table[0][0][a] >= 0.02):
                    self.policy_table[0][0][a] = self.policy_table[0][0][a] - float(0.02/count)
        j = 1
        for j in range(1, len(self.rewardTable)):
            action = self.actionTable[j]
            actionIndex = 0
            if action == "Up":
                actionIndex = 0
            elif action == "Down":
                actionIndex = 1
            elif action == "Left":
                actionIndex = 2
            elif action == "Right":
                actionIndex = 3
            current_reward = self.rewardTable[j] - self.rewardTable[j-1]
            if current_reward > 0:
                if self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][actionIndex] <= 0.98:
                    self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][actionIndex] = self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][actionIndex] + 0.02
                a = 0
                count = 0
                for a in range(4):
                    if (a != actionIndex and self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][a] >= 0.02):
                        count = count + 1
                for a in range(4):
                    if (a != actionIndex and self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][a] >= 0.02):
                        self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][a] = self.policy_table[self.locationYTable[j-1]][self.locationXTable[j-1]][a] - float(0.02/count)
            j = j + 1   
if __name__=="__main__":

    environment = gameEnvironment()
    agent = Agent()
    steps = []
    count = 0

    for i in range(50):
        while(not environment.checkFinal()):
            choice = agent.makeDecision()
            agent.move(choice,environment)
            print("Agent is at location " + str(agent.y) + str(agent.x))
            agent.getReward(environment)
            count = count + 1
            agent.rewardTable.append(agent.reward)
            agent.actionTable.append(choice)
            agent.locationXTable.append(agent.x)
            agent.locationYTable.append(agent.y)
        agent.observe()
        print(agent.actionTable)
        print(agent.locationXTable)
        print(agent.locationYTable)
        print(agent.rewardTable)
        agent.resetReward()
        agent.resetRewardTable()
        agent.resetActionTable()
        agent.resetLocationXTable()
        agent.resetLocationYTable()
        agent.start()
        environment.setLocationToZero()
        steps.append(count)
        count = 0


print()
print()
print("THE NUMBER OF STEPS")
print(steps)
print()

print(agent.policy_table[0])
print()
print(agent.policy_table[1])
print()
print(agent.policy_table[2])
print()
print(agent.policy_table[3])
print()
print(agent.policy_table[4])
