import numpy as np
import random


class SNG():
    def __init__(self, buyin, fee, nb, itm_nb, pay_list):
        self.buyin = buyin
        self.fee = fee
        self.itm_nb = itm_nb
        self.pay_list = pay_list
        if len(self.pay_list) == itm_nb:
            self.pay_list += [0] * (nb - itm_nb)
        self.reward = reward

    def ev(self):
        return self.buyin / (self.buyin + self.fee)

    def variance(self):
        return np.std(np.asarray(pay_list))
            

class Hunter():
    def __init__(self, buyin, fee, nb, itm_nb, pay_list, reward):
        self.buyin = buyin
        self.fee = fee
        self.nb = nb
        self.itm_nb = itm_nb
        self.pay_list = pay_list
        if len(self.pay_list) == itm_nb:
            self.pay_list += [0] * (nb - itm_nb)
        self.reward = reward

    def ev(self):
        return self.buyin / (self.buyin + self.fee)
    
    def simulate(self):
        # stack size p vs q, p > q, f(p) = 0.5 + 0.5 * f(2p-1) = p
        rank_order = [-1] * self.nb
        money = [0] * self.nb
        stack = [1] * self.nb
        survival_set = set([i for i in range(self.nb)])
        order_rev = 1
        while len(survival_set) != 1:
            p, q = random.sample(survival_set, 2)
            u = random.random()
            if u <= stack[p] / (stack[p] + stack[q]):
                stack[p] += stack[q]
                stack[q] = 0
                money[p] += self.reward
                rank_order[q] = self.nb - order_rev
                order_rev += 1
                survival_set.remove(q)
            else:
                stack[q] += stack[p]
                stack[p] = 0
                money[q] += self.reward
                rank_order[p] = self.nb - order_rev
                order_rev += 1
                survival_set.remove(p)
        all_money = [money[i] + self.pay_list[rank_order[i]] for i in range(self.nb)]
        return all_money

    def distribution(self, times=1000):
        pay = []
        for t in range(times):
            pay_t = -self.buyin - self.fee + self.simulate()[0]
            pay.append(pay_t)
        return pay

    def variance(self, times=1000):
        return np.std(np.asarray(self.distribution(times)))

    def distribution_over_n_games(self, n=10, times=10000):
        pay = self.distribution(n * times)
        pay = np.mean(np.reshape(np.asarray(pay), (n, -1)), 0)
        print(f"0.05 percentile:{np.percentile(pay, 5)}")
        print(f"0.25 percentile:{np.percentile(pay, 25)}")
        print(f"0.50 percentile:{np.percentile(pay, 50)}")
        print(f"0.75 percentile:{np.percentile(pay, 75)}")
        print(f"0.95 percentile:{np.percentile(pay, 95)}")
        return pay

    def count_distribution(self, times=10000):
        pay = self.distribution(times)
        pay_dict = dict()
        for i in range(len(pay)):
            if pay[i] in pay_dict:
                pay_dict[pay[i]] += 1
            else:
                pay_dict[pay[i]] = 1
        for key, value in pay_dict.items():
            pay_dict[key] = value / len(pay)
        pay_dict = [(k, pay_dict[k]) for k in sorted(pay_dict.keys())]
        return pay_dict

    def print_summary(self):
        print("Hunter Mtt.")
        print(self.distribution(times=20))
        print(self.variance(times=10000))
        self.distribution_over_n_games(n=1)
        print(self.count_distribution())

if __name__ == "__main__":
    new_structure = Hunter(10, 1, 20, 3, [75, 45, 30], 5)
    new_structure.print_summary()

