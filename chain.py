
class Chain(object):
    def __init__(self):
        self.chain = {GENESIS.hash(): GENESIS}
        self.max_height = 0
    def AddHeader(self, h):
        if h.prev in self.chain:
            parent = self.chain[h.prev] 
            if h.height != parent.height+1:
                return self
            if not pow(h.hash(), BOUND):
                return self
            self.chain[h.hash()] = h
            self.max_height = max(h.height, self.max_height)
        return self
            
    def prune(self):
        pass
