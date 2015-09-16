
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key()
print VerifyingKey.from_string(vk.to_string())
signature = sk.sign("message")
print vk.verify(signature, "message")

tx = TX(vk.to_string(), "", 10).sign(sk)
tx.verifySig()

tx2 = TX(vk.to_string(), "", 10).sign(sk)

example("TX Determinism", tx.serialize() == tx2.serialize())

block  = BlockTX([TX(vk.to_string(), "", random.random()).sign(sk) for i in xrange(10)])

example("Serialization/Deserialization inv",
BlockTX.deserialize(block.serialize()).hash() == block.hash())

        
print Chain().AddHeader(BlockHeader(1, sha("1"), GENESIS.hash(),  1)).chain
    # def mine(self, time):
    #     if self.nonce == None:
    #         self.nonce = 0
    #         while True:
    #             if pow(self.serialize(), BOUND):
    #                 return
