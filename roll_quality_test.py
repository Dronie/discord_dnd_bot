class SumFinder:
    def __init__(self, base, depth):
        self.base = base
        self.depth = self.itStart = depth
        self.count = 0
        self.n = depth - 1
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.base * self.depth:
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

a = SumFinder(9, 3)
b = {}
for i in a:
    if str(i) not in b:
        b[str(i)] = 1
    else:
        b[str(i)] += 1

print(b)