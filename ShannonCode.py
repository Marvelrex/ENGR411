import numpy as np
import math
import sys


class ShannonCoding:
    # Take 2 as complement = using bit (base is 2)
    def __init__(self, symbols, p, complement=2, dim=1):
        p = np.array(p)
        n = len(p)

        if len(symbols) != n:
            print('Not Match!')
            sys.exit(1)

        # Sort as probability order
        for i in range(n):
            for j in range(n - i - 1):
                if p[j] <= p[j + 1]:
                    p[j], p[j + 1] = p[j + 1], p[j]
                    symbols[j], symbols[j + 1] = symbols[j + 1], symbols[j]

        # Calculate Cumulative probability
        cum_p = []
        for i in range(n):
            cum_p.append(0) if i == 0 else cum_p.append(cum_p[i - 1] + p[i - 1])
        cum_p = np.array(cum_p)

        # calculate code length
        length = [int(math.ceil(-math.log(p[i], complement))) for i in range(n)]

        # Coding change to binary
        code = []
        for i in range(n):
            single_code = ''
            t = cum_p[i]
            for j in range(length[i]):
                t = t * complement
                t, z = math.modf(t)
                single_code += str(int(z))
            code.append(single_code)

        # H(x)
        hx = np.sum((-1) * np.log2(p) * p)
        i = np.sum(np.array(length) * p) * math.log2(complement) / dim
        k = hx / i

        self.complement = complement  # In binary
        self.dim = dim  # Dimensional
        self.N = n  # Number of signals
        self.symbols = symbols  # List of symbols
        self.P = p  # p(symbol)
        self.cumulative_p = cum_p  # cumulative probability
        self.L = length  # Code length
        self.code = code  # Code list
        self.H = hx  # Entropy
        self.I = i  # average code length
        self.K = k  # Coding effiency
        print(i)
    def encode(self, img, path='code.txt'):
        """ Encode to txt file"""
        f = open(path, 'w')
        c = ''
        for point in list(img.flatten()):
            for i in range(self.N):
                if self.symbols[i] == point:
                    f.write(self.code[i] + " ")
                    c += self.code[i]
        f.close()
        return c

    def decode(self, c):
        """ decode from file """

        a = []
        s = ''
        loc = 0
        while c != '':
            s += c[loc]
            loc += 1
            if len(s) >= self.L[0]:
                for i in range(self.N):
                    if self.code[i] == s:
                        a.append(self.symbols[i])
                        c = c[loc:]
                        loc = 0
                        s = ''
                        break
        return np.array(a)

    def print_format(self, describe='Symbols'):

        print('{:<10}\t{:<20}\t{:<25}\t{:<10}\t{}'.
              format(describe, 'Probability', 'Cumulative Probability', 'Length', 'Code'))
        print('-' * 100)
        if self.N > 15:
            for i in range(5):
                print('{:<10}\t{:<20}\t{:<25}\t{:<10}\t{}'.
                      format(self.symbols[i], self.P[i], self.cumulative_p[i], self.L[i], self.code[i]))
            print('{:<10}\t{:<20}\t{:<25}\t{:<10}\t{}'.
                  format(' ...', ' ...', ' ...', ' ...', ' ...'))
            for i in range(5):
                print('{:<10}\t{:<20}\t{:<25}\t{:<10}\t{}'.
                      format(self.symbols[i - 5], self.P[i - 5], self.cumulative_p[i - 5], self.L[i - 5],
                             self.code[i - 5]))
        else:
            for i in range(self.N):
                print('{:<10}\t{:<20}\t{:<25}\t{:<10}\t{}'.
                      format(self.symbols[i], self.P[i], self.cumulative_p[i], self.L[i], self.code[i]))
        print('-' * 100)
        print('Coding Efficiency:\t', self.K)
        print('\n\n')
