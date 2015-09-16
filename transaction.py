
from ecdsa import SigningKey, VerifyingKey
import base

class TX(object):
    def __init__(self, _from, to, amount, sig=None):
        self._from = _from
        self.to = to
        self.amount = amount
        self.sig = sig
        self.tx = (self._from, self.to, self.amount)
    def sign(self, sk):
        if self.sig == None:
            if sk.get_verifying_key().to_string() == self._from:
                self.sig = sk.sign_deterministic(str(self.tx))
        return self
    def verifySig(self):
        vk = VerifyingKey.from_string(self._from)
        return vk.verify(self.sig, str(self.tx))
            
    def hash(self):
        sha(self.serialize())
    def serialize(self):
        return str( (self.sig, (self._from, self.to, self.amount)))
    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and isinstance(v[1], tuple) and len(v) == 2 and len(v[1]) == 3:
            t = TX(v[1][0], v[1][1], v[1][2], v[0])
            t.verifySig()
            return t
        else:
            raise ValueError("Malformed tx")

