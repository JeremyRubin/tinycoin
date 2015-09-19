
from base import *
import transaction as T
class BlockTX(object):
    def __init__(self, txs):
        """ List of transactions (TX)"""
        self.txs = txs
    def hash(self):
        sha(self.serialize())
    def serialize(self):
        return str([s.serialize() for s in self.txs])
    def spends(self):
        return [t.parent_tx for t in self.txs]
    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, list):
            b = BlockTX(map(T.TX.deserialize, v))
            return b
        else:
            raise ValueError("Malformed tx block")
class BlockHeader(object):
    def __init__(self, height, block_hash, prev, reward_address, nonce=None):
        self.nonce = nonce
        self.height = height
        self.block_hash = block_hash
        self.prev = prev
        self.reward_address = reward_address
    def serialize(self):
        return str((self.nonce, self.height, self.block_hash, self.prev, self.reward_address))
    

    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and len(v) == 5:
            return BlockHeader(v[1], v[2], v[3], v[4], v[0])
        else:
            raise ValueError("Bad BlockHeader")
    def hash(self):
        return sha(self.serialize())

