import numpy as np
import math
import sys
from tabulate import tabulate


def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    return 0


def InsertionSort(arr):
    if len(arr) <= 1:
        return arr
    for i in range(1, len(arr + 1), 1):
        j = i
        while j > 0:
            if arr[j] > arr[j - 1]:
                j -= 1
                swap(arr, j, j + 1)
            else:
                j -= 1

    return arr


class ShannonCoding:
    # Take 2 as complement = using bit (base is 2)
    def __init__(self, symbols, p, complement=2, dim=1):

        p = np.array(p)
        symbols = np.array(symbols)
        n = len(p)

        if len(symbols) != n:
            print('Not Match!')
            sys.exit(1)

        # Sort as probability order
        p = InsertionSort(p)
        symbols = InsertionSort(symbols)

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
            prob = cum_p[i]
            for j in range(length[i]):
                prob = prob * complement
                prob, whole = math.modf(prob)
                single_code += str(int(whole))
            code.append(single_code)

        # Entropy Average length Efficiency
        hx = np.sum((-1) * np.log2(p) * p)
        i = np.sum(np.array(length) * p) * math.log2(complement) / dim
        k = hx / i

        self.complement = complement  # In binary
        self.dim = dim  # Dimensional
        self.N = n  # Number of signals
        self.RGB = symbols  # List of symbols
        self.P = p  # p(symbol)
        self.cumulative_p = cum_p  # cumulative probability
        self.L = length  # Code length
        self.code = code  # Code list
        self.H = hx  # Entropy
        self.I = i  # average code length
        self.K = k  # Coding effiency

    def encode(self, img, path='code.txt'):
        """ Encode to txt file"""
        f = open(path, 'w')
        c = ''
        for point in list(img.flatten()):
            for i in range(self.N):
                if self.RGB[i] == point:
                    f.write(self.code[i] + " ")
                    c += self.code[i]
        f.close()
        return c

    def decode(self, c):
        """ decode long string """
        a = []
        s = ''
        loc = 0
        while c != '':
            s += c[loc]
            loc += 1
            if len(s) >= self.L[0]:
                for i in range(self.N):
                    if self.code[i] == s:
                        a.append(self.RGB[i])
                        c = c[loc:]
                        loc = 0
                        s = ''
                        break
        return np.array(a)

    def print_format(self):

        print('Coding Efficiency：%.2f \nEntropy of image:%.2f \n Average Code Length:%.2f' % (self.K, self.H, self.I))
        print('-' * 100)
        print(tabulate(['RGB', 'Probability', 'Code Length', 'Code'], self.RGB, self.P, self.L, self.code, ))
        print('-' * 100)
        print('\n\n')
