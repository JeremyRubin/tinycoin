
from ecdsa import SigningKey, VerifyingKey
import base

class TX(object):
    def __init__(self, parent_tx, _from, to_amounts, sig=None):
        self.parent_tx = parent_tx
        self._from = _from
        self.to_amounts = to_amounts
        self.sig = sig
        self.tx = (self._from, self.to_amounts, self.parent_tx)
    def amount_spent(self):
        return sum(a for (_, a) in self.to_amounts)
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
        return str( (self.sig, self.tx))
    @staticmethod
    def deserialize(s):
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and isinstance(v[1], tuple) and len(v) == 2 and len(v[1]) == 3:
            t = TX(v[1][-1], v[1][0], v[1][1],  v[0])
            t.verifySig()
            if any(amount < 0 for (to, amount) in t.to_amounts):
                raise ValueError("No Negative Values legal")
            return t
        else:
            raise ValueError("Malformed tx")

