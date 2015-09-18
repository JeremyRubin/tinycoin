
from base import *
import transaction
class BlockTX(object):
    def __init__(self, txs):
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
            b = BlockTX(map(TX.deserialize, v))
            
            return b
        else:
            raise ValueError("Malformed tx block")
class BlockHeader(object):
    def __init__(self, height, merkle_root, prev, nonce=None):
        self.nonce = nonce
        self.height = height
        self.merkle_root = merkle_root
        self.prev = prev
    def serialize(self):
        return str((self.nonce, self.height, self.merkle_root, self.prev))

    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and len(v) == 4:
            return BlockHeader(v[1], v[2], v[3], v[0])
        else:
            raise ValueError("Bad BlockHeader")
    def hash(self):
        return sha(self.serialize())
# mroot = block.hash()
# print BlockHeader.deserialize(BlockHeader(1,block.hash(),3,4).serialize())
# print BlockHeader(1,block.hash(),3,4).hash()

