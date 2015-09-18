
GENESIS = BlockHeader(0,BlockTX([]).hash(), None, 0)
class UTXO(object):
    def __init__(self, owner, amount, parent, index):
        self.owner = owner
        self.amount = amount
        self.parent = parent
        self.index = index
    def hash(self):
        return sha(self.serialize())
    def serialize(self):
        return str((self.owner, self.amount, self.parent, self.index))
class TXSET(object):
    def __init__(self, tx):
        self.utxos = tx
    def process_block(self, block):
        used = set([])
        for tx in block.txs:
            if tx.parent in used:
                raise ValueError("Double Spend")
            if tx.parent not in utxos:
                raise ValueError("No Such TX")
            if not self.utxos[tx.parent].amount >= tx.amount_spent():
                raise ValueError("Too Much Spent")
            used.add(tx.parent)
        new_set = self.utxos.copy()
        for txid in used:
            del new_set[txid]
        for tx in block.txs:
            for index, (owner, amount) in enumerate(tx.to_amounts):
            u = UTXO(owner, amount, tx.parent, index)
            new_set[u.hash()] = u
        return TXSET(new_set)
                

            
class Chain(object):
    def __init__(self):
        self.chain = [{GENESIS.hash(): (GENESIS, BlockTX([]), TXSET({}) )}]
        self.max_height = 0
    def AddBlock(self, header, block):
        if self.max_height == header.height -1:
            self.max_height +=1
            self.chain.append({})
        if self.max_height >= header.height and header.prev in self.chain[header.height-1] and header.hash() not in self.chain[header.height]:
            parent_header, parent_block, parent_txset= self.chain[header.height-1][h.prev] 
            if header.height != parent_header.height+1:
                return self
            if not pow(header.hash(), BOUND):
                return self
            new_txset = parent_txset.process_block(block)
            self.chain[header.height][header.hash()] = (header, block, new_txset)
            self.max_height = max(h.height, self.max_height)
        return self
            
    def prune(self):
        pass
