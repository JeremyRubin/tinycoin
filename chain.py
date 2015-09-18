import block as B
GENESIS_BLOCK = B.BlockTX([])
GENESIS_HEADER = B.BlockHeader(0, GENESIS_BLOCK.hash(), None,"me", 0)

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
class UTXOSET(object):
    def __init__(self, tx):
        self.utxos = tx
    def process_block(self, block, reward_address):
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
        # This is where babies come from
        reward_tx = UTXO(reward_address, BLOCK_REWARD, "", 0)
        new_set[reward_tx.hash()] = reward_tx
        return UTXOSET(new_set)

class ChainNode(object):
    def __init__(self, header, transactions, utxoset):
        self.header = header
        self.transactions = transactions
        self.utxoset = utxoset 
# Add ASCII Data Structure
class Chain(object):
    def __init__(self):
        self.chain = [{GENESIS_HEADER.hash(): ChainNode(GENESIS_HEADER,
                                                        GENESIS_BLOCK,
                                                        UTXOSET({}))}]
        self.max_height = 0
    @staticmethod
    def make_new_utxo_set(parent, child, header):
        if not pow(header.hash(), BOUND):
            raise ValueError("Not enough Proof of Work")
        return parent.process_block(block, header.reward_address)
    def add_block(self, header, block):
        # Refactor to do this after (important for correctness)
        if self.max_height == header.height -1:
            self.max_height +=1
            self.chain.append({})
        if header.hash() in self.chain[header.height]:
            return self
        if self.max_height >= header.height:
            return self #TODO: Out of order block, deal with later elegantly
        if header.prev in self.chain[header.height-1]:
            parent = self.chain[header.height-1][h.prev]
            if header.height != parent.header.height+1:
                raise ValueError("Invalid Block Height for Parent (Internal Error)")
            try:
                new_utxoset = Chain.make_new_utxo_set(parent.utxoset, block, header)
            except ValueError as e:
                print e, "Bad Block, rejected!"
            finally:
                self.chain[header.height][header.hash()] = ChainNode(header, block, new_utxoset)
                self.max_height = max(h.height, self.max_height)
        return self

    def add_tx(self, tx):
        pass
    def get_work(self):
        """ Returns a header just for mining"""
        pass
    def lookup_tx(self, txid):
        """ Returns data on a utxo"""
        return "{'error':-1}"
    def prune(self):
        """ Can remove old forks/UTXO sets over time"""
        pass
