import matplotlib.pyplot as plt
import math

font = {
    'family' : 'normal',
    'size' : 6}

plt.rc('font', **font)

class SumFinder:
    ''' Class that implements a method for finding all the
        possible total values you can get from an arbitrary
        number of n-sided dice.

        Attributes
        ----------
        base : the number of sides of the dice
        depth : the number of dice to be thrown
    
    '''
    def __init__(self, base, depth):
        self.base = base
        self.depth = self.itStart = depth
        self.count = 0
        self.n = depth - 1
    
    def __iter__(self):
        return self

    def __next__(self):
        # raise a generic exception if sum is gt highest possible sum
        if self.n > self.base * self.depth:
            raise Exception

        # stop incrementation when we reach the highest possible sum
        if self.n == self.base * self.depth:
            raise StopIteration
        
        elif self.n == (self.base - 1) * (self.depth - 1) + self.itStart:
            self.itStart = self.itStart + 1
            self.n = self.itStart
            self.count = 0

        elif self.count == self.base:
            self.count = 0
            self.n = self.n - (self.base - 2)

        else:
            self.n += 1
        
        self.count += 1
        return self.n

def get_dist(base, depth):

    a = SumFinder(base, depth)
    b = {}
    for i in a:
        if str(i) not in b:
            b[str(i)] = 1
        else:
            b[str(i)] += 1
    
    return b

def no_of_buckets(base, depth):
    return depth * (base - 1) + 1

def median(no_of_buckets):
    return int(math.ceil((no_of_buckets+1)/2))

def get_std(b, base, depth):
    frequencies = list(b.values())
    buckets = list(b.keys())
    size = sum(frequencies)
    med = int(buckets[median(no_of_buckets(base, depth))-1])
    sqaured_differences = [(i - med) ** 2 for i in frequencies]

    std = (sum(sqaured_differences) / size) ** (0.5)

    return std, med

def get_quality(roll, base, depth):
    std, med = get_std(get_dist(base, depth), base, depth)

    quality = 0

    if roll > depth:
        quality += 1
    if roll > med - (2.698*std):
        quality += 1
    if roll > med - (0.6745*std):
        quality += 1
    if roll > med + (0.6745*std):
        quality += 1
    if roll > med + (2.698*std):
        quality += 1
    
    return quality

print(f'{get_quality(31, 6, 6)}')




'''
degree = 10

fig, axs = plt.subplots(degree, degree)
fig.set_size_inches(200,60)

fig.set_tight_layout(True)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.11, wspace=0.2, hspace=0.2)
for i in range(1, degree+1):
    for j in range(1, degree+1):
        
        a = get_dist(i, j)
        axs[i-1, j-1].bar(*zip(*a.items()))
        axs[i-1, j-1].set_title(f'base {i}, depth {j}')
        
plt.savefig(fname='dice_plot.jpg')
'''
