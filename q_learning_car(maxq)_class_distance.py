import copy
import numpy as np
import random
import matplotlib.pyplot as plt
import time
import os

localtime = time.strftime("%Y-%m-%d %H%M%S", time.localtime())
path = './train-' + str(localtime)
alpha = 0.1
gamma = 0.8
epsilon = 0.1
training_times = 200
plt.ion()
img = plt.imread('parking_lot.jpg')
train_distance = []
Loss = []
Real_time = []
Step = []
Reward = []
# s有78个，目标车位为77
# a有上下左右4个
# 寻找P2车位
# R(s,a)
Re = np.array([
    # 上  下  左  右
    [-100, -1, -100, -1],  # 0
    [-100, -1, -1, -100],  # 1
    [-100, -1, -100, -100],  # 2
    [-100, -1, -100, -1],  # 3
    [-100, -1, -1, -100],  # 4
    [-1, -100, -100, -1],  # 5
    [-1, -1, -1, -1],  # 6
    [-100, -100, -1, -1],  # 7
    [-100, -100, -1, -1],  # 8
    [-100, -100, -1, -1],  # 9
    [-100, -100, -1, -1],  # 10
    [-100, -100, -1, -1],  # 11
    [-100, -100, -1, -1],  # 12
    [-100, -100, -1, -1],  # 13
    [-1, -1, -1, -1],  # 14
    [-100, -100, -1, -1],  # 15
    [-100, -100, -1, -1],  # 16
    [-100, -1, -1, -1],  # 17
    [-100, -100, -1, -1],  # 18
    [-100, -100, -1, -1],  # 19
    [-1, -1, -1, -1],  # 20
    [-1, -100, -1, -100],  # 21
    [-1, -1, -100, -100],  # 22
    [-1, -1, -100, -100],  # 23
    [-1, -1, -100, -100],  # 24
    [-1, -1, -100, -100],  # 25
    [-1, -1, -100, -100],  # 26
    [-1, -1, -100, -100],  # 27
    [-1, -1, -100, -100],  # 28
    [-1, -1, -100, -100],  # 29
    [-100, -100, -100, -1],  # 30
    [-1, -1, -1, -1],  # 31
    [-100, -100, -1, -1],  # 32
    [-100, -100, -1, -1],  # 33
    [-100, -100, -1, -1],  # 34
    [-100, -1, -1, -1],  # 35
    [-100, -100, -1, -1],  # 36
    [-100, -100, -1, -1],  # 37
    [-100, -100, -1, -1],  # 38
    [-1, -1, -1, -1],  # 39
    [-100, -100, -1, -1],  # 40
    [-100, -100, -1, -1],  # 41
    [-1, 10000, -1, -1],  # 42
    [-100, -100, -1, -1],  # 43
    [-100, -100, -1, -1],  # 44
    [-1, -1, -1, -1],  # 45
    [-100, -100, -1, -100],  # 46
    [-1, -1, -100, -100],  # 47
    [-1, -1, -100, -100],  # 48
    [-1, -1, -100, -100],  # 49
    [-1, -1, -100, -100],  # 50
    [-1, -1, -100, -100],  # 51
    [-1, -1, -100, -100],  # 52
    [-1, -1, -100, -100],  # 53
    [-1, -1, -100, -100],  # 54
    [-100, -1, -100, -1],  # 55
    [-1, -1, -1, -1],  # 56
    [-100, -100, -1, -1],  # 57
    [-100, -100, -1, -1],  # 58
    [-100, -100, -1, -1],  # 59
    [-1, -100, -1, -1],  # 60
    [-100, -100, -1, -1],  # 61
    [-100, -100, -1, -1],  # 62
    [-100, -100, -1, -1],  # 63
    [-1, -1, -1, -1],  # 64
    [-100, -100, -1, -1],  # 65
    [-100, -100, -1, -1],  # 66
    [-100, -100, -1, -1],  # 67
    [-100, -100, -1, -1],  # 68
    [-100, -100, -1, -1],  # 69
    [-1, -1, -1, -1],  # 70
    [-100, -1, -1, -100],  # 71
    [-1, -100, -100, -1],  # 72
    [-1, -100, -1, -100],  # 73
    [-1, -100, -100, -100],  # 74
    [-1, -100, -100, -1],  # 75
    [-1, -100, -1, -100],  # 76
    # 上  下  左  右
])
# Q(s,a)
Qt = np.zeros((78, 4))
# T(s,a)
Sn = np.array([
    # 上  下  左  右
    [-1, 5, -1, 1],  # 0
    [-1, 6, 0, -1],  # 1
    [-1, 14, -1, -1],  # 2
    [-1, 20, -1, 4],  # 3
    [-1, 21, 3, -1],  # 4
    [0, -1, -1, 6],  # 5
    [1, 22, 5, 7],  # 6
    [-1, -1, 6, 8],  # 7
    [-1, -1, 7, 9],  # 8
    [-1, -1, 8, 10],  # 9
    [-1, -1, 9, 11],  # 10
    [-1, -1, 10, 12],  # 11
    [-1, -1, 11, 13],  # 12
    [-1, -1, 12, 14],  # 13
    [2, 24, 13, 15],  # 14
    [-1, -1, 14, 16],  # 15
    [-1, -1, 15, 17],  # 16
    [-1, 26, 16, 18],  # 17
    [-1, -1, 17, 19],  # 18
    [-1, -1, 18, 20],  # 19
    [3, 28, 19, 21],  # 20
    [4, -1, 20, -1],  # 21
    [6, 23, -1, -1],  # 22
    [22, 31, -1, -1],  # 23
    [14, 25, -1, -1],  # 24
    [24, 39, -1, -1],  # 25
    [17, 27, -1, -1],  # 26
    [26, 42, -1, -1],  # 27
    [20, 29, -1, -1],  # 28
    [28, 45, -1, -1],  # 29
    [-1, -1, -1, 31],  # 30
    [23, 47, 30, 32],  # 31
    [-1, -1, 31, 33],  # 32
    [-1, -1, 32, 34],  # 33
    [-1, -1, 33, 35],  # 34
    [-1, 49, 34, 36],  # 35
    [-1, -1, 35, 37],  # 36
    [-1, -1, 36, 38],  # 37
    [-1, -1, 37, 39],  # 38
    [25, 51, 38, 40],  # 39
    [-1, -1, 39, 41],  # 40
    [-1, -1, 40, 42],  # 41
    [27, 77, 41, 43],  # 42
    [-1, -1, 42, 44],  # 43
    [-1, -1, 43, 45],  # 44
    [29, 53, 44, 46],  # 45
    [-1, -1, 45, -1],  # 46
    [31, 48, -1, -1],  # 47
    [47, 56, -1, -1],  # 48
    [35, 50, -1, -1],  # 49
    [49, 60, -1, -1],  # 50
    [39, 52, -1, -1],  # 51
    [51, 64, -1, -1],  # 52
    [45, 54, -1, -1],  # 53
    [53, 70, -1, -1],  # 54
    [-1, 72, -1, 56],  # 55
    [48, 73, 55, 57],  # 56
    [-1, -1, 56, 58],  # 57
    [-1, -1, 57, 59],  # 58
    [-1, -1, 58, 60],  # 59
    [50, -1, 59, 61],  # 60
    [-1, -1, 60, 62],  # 61
    [-1, -1, 61, 63],  # 62
    [-1, -1, 62, 64],  # 63
    [52, 74, 63, 65],  # 64
    [-1, -1, 64, 66],  # 65
    [-1, -1, 65, 67],  # 66
    [-1, -1, 66, 68],  # 67
    [-1, -1, 67, 69],  # 68
    [-1, -1, 68, 70],  # 69
    [54, 75, 69, 71],  # 70
    [-1, 76, 70, -1],  # 71
    [55, -1, -1, 73],  # 72
    [56, -1, 72, -1],  # 73
    [64, -1, -1, -1],  # 74
    [70, -1, -1, 76],  # 75
    [71, -1, 75, -1],  # 76
    # 上  下  左  右
])

a_set = np.array([
    # 上  下  左  右
    [1, 3],  # 0
    [1, 2],  # 1
    [1],  # 2
    [1, 3],  # 3
    [1, 2],  # 4
    [0, 3],  # 5
    [0, 1, 2, 3],  # 6
    [2, 3],  # 7
    [2, 3],  # 8
    [2, 3],  # 9
    [2, 3],  # 10
    [2, 3],  # 11
    [2, 3],  # 12
    [2, 3],  # 13
    [0, 1, 2, 3],  # 14
    [2, 3],  # 15
    [2, 3],  # 16
    [1, 2, 3],  # 17
    [2, 3],  # 18
    [2, 3],  # 19
    [0, 1, 2, 3],  # 20
    [0, 2],  # 21
    [0, 1],  # 22
    [0, 1],  # 23
    [0, 1],  # 24
    [0, 1],  # 25
    [0, 1],  # 26
    [0, 1],  # 27
    [0, 1],  # 28
    [0, 1],  # 29
    [3],  # 30
    [0, 1, 2, 3],  # 31
    [2, 3],  # 32
    [2, 3],  # 33
    [2, 3],  # 34
    [1, 2, 3],  # 35
    [2, 3],  # 36
    [2, 3],  # 37
    [2, 3],  # 38
    [0, 1, 2, 3],  # 39
    [2, 3],  # 40
    [2, 3],  # 41
    [0, 1, 2, 3],  # 42
    [2, 3],  # 43
    [2, 3],  # 44
    [0, 1, 2, 3],  # 45
    [2],  # 46
    [0, 1],  # 47
    [0, 1],  # 48
    [0, 1],  # 49
    [0, 1],  # 50
    [0, 1],  # 51
    [0, 1],  # 52
    [0, 1],  # 53
    [0, 1],  # 54
    [1, 3],  # 55
    [0, 1, 2, 3],  # 56
    [2, 3],  # 57
    [2, 3],  # 58
    [2, 3],  # 59
    [0, 2, 3],  # 60
    [2, 3],  # 61
    [2, 3],  # 62
    [2, 3],  # 63
    [0, 1, 2, 3],  # 64
    [2, 3],  # 65
    [2, 3],  # 66
    [2, 3],  # 67
    [2, 3],  # 68
    [2, 3],  # 69
    [0, 1, 2, 3],  # 70
    [1, 2],  # 71
    [0, 3],  # 72
    [0, 2],  # 73
    [0],  # 74
    [0, 3],  # 75
    [0, 2],  # 76
    # 上  下  左  右
])

cord = {
    0: (15, 20), 1: (45, 20), 2: (187, 20), 3: (307, 20), 4: (337, 20), 5: (15, 42), 6: (45, 48), 7: (67, 48),
    8: (82, 48), 9: (97, 48),
    10: (112, 48), 11: (127, 48), 12: (142, 48), 13: (157, 48), 14: (190, 48), 15: (216, 48), 16: (234, 48),
    17: (245, 48), 18: (261, 48), 19: (276, 48),
    20: (303, 48), 21: (338, 42), 22: (44, 76), 23: (44, 100), 24: (188, 76), 25: (188, 100), 26: (247, 76),
    27: (247, 100), 28: (306, 76), 29: (306, 100),
    30: (15, 127), 31: (42, 127), 32: (67, 127), 33: (82, 127), 34: (97, 127), 35: (112, 127), 36: (127, 127),
    37: (142, 127), 38: (157, 127), 39: (185, 127),
    40: (218, 127), 41: (233, 127), 42: (248, 127), 43: (263, 127), 44: (278, 127), 45: (303, 127), 46: (338, 127),
    47: (43, 155), 48: (43, 178), 49: (113.5, 155),
    50: (113.5, 178), 51: (187, 155), 52: (187, 178), 53: (303, 155), 54: (303, 178), 55: (15, 212), 56: (45, 206),
    57: (70, 206), 58: (85, 206), 59: (100, 206),
    60: (114, 206), 61: (128, 206), 62: (142, 206), 63: (156, 206), 64: (187, 206), 65: (218, 206), 66: (232, 206),
    67: (246, 206), 68: (262, 206), 69: (276, 206),
    70: (303, 206), 71: (339, 211), 72: (15, 233), 73: (45, 233), 74: (186, 233), 75: (303, 233), 76: (338, 233),
    77: (250, 152)
}


def cumulative(value):
    result = []
    label = 0
    for i in value:
        a = label + i
        result.append(a)
        label = a
    return result


def decomposition(value):
    print(value)
    for i in range(len(value))[::-1]:
        if i == 0:
            return value
        value[i] -= value[i - 1]


class QLearningAgent:
    def __init__(self, actions, learning_rate, discount_factor, epsilon, q_table):
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = q_table
        self.temp = abs(cord[0][0] - cord[77][0]) + abs(cord[0][1] - cord[77][1])

    # 采样 <s, a, r, s'>
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    # 从Q-table中选取动作
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # 贪婪策略随机探索动作
            action = np.random.choice(self.actions[state])
        else:
            # 从q表中选择
            max_q = -1000000
            for t in self.actions[state]:
                if max_q < self.q_table[state][t]:
                    max_q = self.q_table[state][t]
                    action = t
        return action

    def arg_max(self, state_action, state):
        max_index_list = []
        max_value = -10000
        for index in self.actions[state]:
            value = state_action[index]
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)

    # Manhattan distance
    def distance(self, s, next_state):
        distance = abs(cord[77][0] - cord[next_state][0]) + abs(cord[77][1] - cord[next_state][1])
        label_temp = self.temp
        self.temp = distance
        if distance == 0:
            return 10000
        if label_temp < distance:
            return -3
        elif label_temp == distance:
            return -2
        else:
            return -1

    def forward(self, state, s):
        next_state = Sn[s][state]
        # rew=Re[s][state]
        rew = self.distance(s, next_state)
        return next_state, rew


def make_file():
    if not os.path.exists(path):
        os.mkdir(path)


def init():
    s = 0
    states = []
    X = []
    Y = []
    reward = []
    states.append(0)
    X.append(cord[0][0])
    Y.append(cord[0][1])
    return s, states, X, Y, reward, time.time()


def main():
    make_file()
    agent = QLearningAgent(a_set, alpha, gamma, epsilon, Qt)

    for i in range(training_times):
        print('new episode begin')
        s, states, X, Y, reward, t1 = init()
        while True:
            # agent产生动作
            action = agent.get_action(s)
            next_state, rew = agent.forward(action, s)
            # 更新Q表
            agent.learn(s, action, rew, next_state)
            s = next_state
            reward.append(rew)
            states.append(s)
            X.append(cord[s][0])
            Y.append(cord[s][1])
            if s == 77:
                loss = abs((sum(reward) - 9976) / len(states))
                Loss.append(loss)
                Step.append(len(states))
                t2 = time.time()
                Reward.append(np.sum(reward)-10000)
                Real_time.append((t2 - t1) * 1e3)
                print('the ' + str(i) + ' training loss is:' + str(loss))
                break

        plt.imshow(img)
        # plt.plot(X, Y, 'g->')
        plt.plot(X, Y, c='r',linestyle='--',marker='o')
        train_distance.append(len(states))
        plt.title('time:' + str(len(states)))
        plt.savefig(path + '/' + str(i) + '.jpg')
        plt.close()


if __name__ == "__main__":
    main()
    plt.ioff()
    plt.plot(range(1, training_times + 1), train_distance, 'k-')
    plt.xlabel("training times")
    plt.ylabel('time')
    plt.savefig(path + '/' + 'training-times-curve' + '.jpg')
    plt.close()
    print("final Q:", Qt)

    plt.plot(Loss)
    plt.xlabel("training times")
    plt.ylabel('loss')
    plt.savefig(path + '/' + 'loss-curve' + '.jpg')
    plt.close()

    plt.plot(cumulative(Real_time))
    plt.xlabel("training times")
    plt.ylabel('time')
    plt.savefig(path + '/' + 'time-curve' + '.jpg')
    plt.close()

    plt.plot(Step)
    plt.xlabel("Number of iterations")
    plt.ylabel('step')
    plt.savefig(path + '/' + 'step-curve' + '.jpg')
    plt.close()

    plt.plot(Reward)
    plt.xlabel("Number of iterations")
    plt.ylabel('reward')
    plt.savefig(path + '/' + 'reward-curve' + '.jpg')
    plt.close()

