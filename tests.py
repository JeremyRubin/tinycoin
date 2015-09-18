from base import *
from node import *
from transaction import *

import unittest
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key()
#print VerifyingKey.from_string(vk.to_string())
#signature = sk.sign("message")
#print vk.verify(signature, "message")
#
#tx = TX(vk.to_string(), "", 10).sign(sk)
#tx.verifySig()
#
#tx2 = TX(vk.to_string(), "", 10).sign(sk)
#
#example("TX Determinism", tx.serialize() == tx2.serialize())
#
#block  = BlockTX([TX(vk.to_string(), "", random.random()).sign(sk) for i in xrange(10)])
#
#example("Serialization/Deserialization inv",
#BlockTX.deserialize(block.serialize()).hash() == block.hash())

# mroot = block.hash()
# print BlockHeader.deserialize(BlockHeader(1,block.hash(),3,4).serialize())
# print BlockHeader(1,block.hash(),3,4).hash()

        
#print Chain().AddHeader(BlockHeader(1, sha("1"), GENESIS.hash(),  1)).chain
    # def mine(self, time):
    #     if self.nonce == None:
    #         self.nonce = 0
    #         while True:
    #             if pow(self.serialize(), BOUND):
    #                 return
class Tests(unittest.TestCase):
    def test_tx(self):
        tx = TX("", vk.to_string(), [("", 2)]).sign(sk)
        tx.verifySig()

    def test_tx_sig_bad(self):
        tx = TX("", vk.to_string(), [("", 2)])
        with self.assertRaises(ValueError):
            tx.verifySig()
    def test_tx2(self):
        tx = TX("", vk.to_string(), [("", 2)]).sign(sk)
        TX.deserialize(tx.serialize())

if __name__ == '__main__':
    unittest.main()
